"""
Core Training Classes

Provides base training functionality using HuggingFace Transformers directly.
"""

import os
import json
import logging
from typing import Optional, Dict, Any, Union
from pathlib import Path
import torch
from abc import ABC, abstractmethod

from .config import TrainingConfig, LoRAConfig, DatasetConfig

logger = logging.getLogger(__name__)


class BaseTrainer(ABC):
    """Base trainer class for all training operations."""
    
    def __init__(self, config: TrainingConfig):
        """
        Initialize the trainer.
        
        Args:
            config: Training configuration
        """
        self.config = config
        self.model = None
        self.tokenizer = None
        self.train_dataset = None
        self.eval_dataset = None
        
        # Set up output directory
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized {self.__class__.__name__} with output dir: {self.output_dir}")
    
    @abstractmethod
    def load_model(self) -> None:
        """Load the model and tokenizer."""
        pass
    
    @abstractmethod
    def prepare_datasets(self) -> None:
        """Prepare training and validation datasets."""
        pass
    
    @abstractmethod
    def train(self) -> str:
        """Execute the training process."""
        pass
    
    def save_config(self) -> None:
        """Save training configuration."""
        config_path = self.output_dir / "training_config.json"
        with open(config_path, 'w') as f:
            json.dump(self.config.to_dict(), f, indent=2)
        logger.info(f"Training config saved to: {config_path}")
    
    def get_device(self) -> torch.device:
        """Get the appropriate device for training."""
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")


class SFTTrainer(BaseTrainer):
    """Supervised Fine-Tuning trainer."""
    
    def __init__(self, config: TrainingConfig):
        """Initialize SFT trainer."""
        super().__init__(config)
        self.trainer = None
        
    def load_model(self) -> None:
        """Load model and tokenizer for SFT."""
        try:
            from transformers import (
                AutoModelForCausalLM, 
                AutoTokenizer,
                BitsAndBytesConfig
            )
            from peft import get_peft_model, LoraConfig, TaskType
            
            logger.info(f"Loading model: {self.config.model_name}")
            
            # Configure quantization if using LoRA
            quantization_config = None
            if self.config.lora_config and self.config.lora_config.use_lora:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                )
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                trust_remote_code=True,
                padding_side="right"
            )
            
            # Add pad token if missing
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                quantization_config=quantization_config,
                device_map="auto" if torch.cuda.is_available() else None,
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.config.fp16 else torch.float32
            )
            
            # Apply LoRA if configured
            if self.config.lora_config and self.config.lora_config.use_lora:
                peft_config = LoraConfig(
                    task_type=TaskType.CAUSAL_LM,
                    inference_mode=False,
                    r=self.config.lora_config.lora_rank,
                    lora_alpha=self.config.lora_config.lora_alpha,
                    lora_dropout=self.config.lora_config.lora_dropout,
                    target_modules=self.config.lora_config.lora_target_modules
                )
                self.model = get_peft_model(self.model, peft_config)
                logger.info("LoRA configuration applied to model")
            
            logger.info("Model and tokenizer loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def prepare_datasets(self) -> None:
        """Prepare datasets for training."""
        try:
            from datasets import load_dataset, Dataset
            from .dataset import DatasetManager
            
            if not self.config.dataset_config:
                raise ValueError("Dataset configuration is required")
            
            logger.info(f"Loading dataset: {self.config.dataset_config.dataset_path}")
            
            # Use DatasetManager to handle different dataset formats
            dataset_manager = DatasetManager(
                self.tokenizer,
                max_length=self.config.dataset_config.max_length
            )
            
            # Load and prepare datasets
            self.train_dataset, self.eval_dataset = dataset_manager.prepare_dataset(
                self.config.dataset_config.dataset_path,
                dataset_format=self.config.dataset_config.dataset_format,
                validation_split=self.config.dataset_config.validation_split
            )
            
            logger.info(f"Training dataset size: {len(self.train_dataset)}")
            if self.eval_dataset:
                logger.info(f"Evaluation dataset size: {len(self.eval_dataset)}")
            
        except Exception as e:
            logger.error(f"Failed to prepare datasets: {e}")
            raise
    
    def train(self) -> str:
        """Execute SFT training."""
        try:
            from transformers import (
                Trainer,
                TrainingArguments,
                DataCollatorForLanguageModeling
            )
            
            logger.info("Starting SFT training...")
            
            # Prepare model and datasets
            self.load_model()
            self.prepare_datasets()
            
            # Configure training arguments
            training_args = TrainingArguments(
                output_dir=str(self.output_dir),
                num_train_epochs=self.config.num_epochs,
                per_device_train_batch_size=self.config.batch_size,
                per_device_eval_batch_size=self.config.batch_size,
                gradient_accumulation_steps=self.config.gradient_accumulation_steps,
                warmup_steps=self.config.warmup_steps,
                weight_decay=self.config.weight_decay,
                learning_rate=self.config.learning_rate,
                fp16=self.config.fp16,
                bf16=self.config.bf16,
                gradient_checkpointing=self.config.gradient_checkpointing,
                max_grad_norm=self.config.max_grad_norm,
                logging_steps=self.config.logging_steps,
                save_steps=self.config.save_steps,
                eval_steps=self.config.eval_steps if self.eval_dataset else None,
                evaluation_strategy="steps" if self.eval_dataset else "no",
                save_total_limit=self.config.save_total_limit,
                load_best_model_at_end=True if self.eval_dataset else False,
                report_to=None,  # Disable wandb/tensorboard for now
                remove_unused_columns=False,
            )
            
            # Data collator
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False,
            )
            
            # Initialize trainer
            self.trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=self.train_dataset,
                eval_dataset=self.eval_dataset,
                data_collator=data_collator,
            )
            
            # Save configuration
            self.save_config()
            
            # Start training
            logger.info("Training started...")
            train_result = self.trainer.train()
            
            # Save final model
            logger.info("Saving final model...")
            self.trainer.save_model()
            self.tokenizer.save_pretrained(self.output_dir)
            
            # Save training metrics
            metrics_path = self.output_dir / "training_metrics.json"
            with open(metrics_path, 'w') as f:
                json.dump(train_result.metrics, f, indent=2)
            
            logger.info(f"Training completed successfully! Model saved to: {self.output_dir}")
            return str(self.output_dir)
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise
    
    def upload_to_huggingface(self, hf_model_name: str, token: Optional[str] = None) -> str:
        """Upload trained model to HuggingFace Hub."""
        try:
            from huggingface_hub import HfApi, create_repo
            
            logger.info(f"Uploading model to HuggingFace: {hf_model_name}")
            
            # Create repository
            api = HfApi(token=token)
            try:
                create_repo(hf_model_name, token=token, exist_ok=True)
                logger.info(f"Repository created/verified: {hf_model_name}")
            except Exception as e:
                logger.warning(f"Repository creation warning: {e}")
            
            # Upload model files
            api.upload_folder(
                folder_path=str(self.output_dir),
                repo_id=hf_model_name,
                token=token
            )
            
            model_url = f"https://huggingface.co/{hf_model_name}"
            logger.info(f"Model uploaded successfully: {model_url}")
            return model_url
            
        except Exception as e:
            logger.error(f"Failed to upload to HuggingFace: {e}")
            raise 