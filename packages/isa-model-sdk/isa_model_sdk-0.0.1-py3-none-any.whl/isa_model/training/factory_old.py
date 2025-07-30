"""
Unified Training Factory for ISA Model Framework

This factory provides a single interface for all training operations:
- LLM fine-tuning (SFT, DPO, RLHF)
- Image model training (Flux, LoRA)
- Model evaluation and benchmarking
"""

import os
import logging
from typing import Optional, Dict, Any, Union, List
from pathlib import Path
import datetime

from .engine.llama_factory import LlamaFactory, TrainingStrategy, DatasetFormat
from .engine.llama_factory.config import SFTConfig, RLConfig, DPOConfig

logger = logging.getLogger(__name__)


class TrainingFactory:
    """
    Unified factory for all AI model training operations.
    
    This class provides simplified interfaces for:
    - LLM training using LlamaFactory
    - Image model training using Flux/LoRA
    - Model evaluation and benchmarking
    
    Example usage for fine-tuning Gemma 3:4B:
        ```python
        from isa_model.training import TrainingFactory
        
        factory = TrainingFactory()
        
        # Fine-tune with your dataset
        model_path = factory.finetune_llm(
            model_name="google/gemma-2-4b-it",
            dataset_path="path/to/your/data.json",
            training_type="sft",
            use_lora=True,
            num_epochs=3,
            batch_size=4,
            learning_rate=2e-5
        )
        
        # Train with DPO for preference optimization
        dpo_model = factory.train_with_preferences(
            model_path=model_path,
            preference_data="path/to/preferences.json",
            beta=0.1
        )
        ```
    """
    
    def __init__(self, base_output_dir: Optional[str] = None):
        """
        Initialize the training factory.
        
        Args:
            base_output_dir: Base directory for all training outputs
        """
        self.base_output_dir = base_output_dir or os.path.join(os.getcwd(), "training_outputs")
        os.makedirs(self.base_output_dir, exist_ok=True)
        
        # Initialize sub-factories
        self.llm_factory = LlamaFactory(base_output_dir=os.path.join(self.base_output_dir, "llm"))
        
        logger.info(f"TrainingFactory initialized with output dir: {self.base_output_dir}")
    
    def _get_output_dir(self, model_name: str, training_type: str) -> str:
        """Generate timestamped output directory."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_model_name = model_name.replace("/", "_").replace(":", "_")
        return os.path.join(self.base_output_dir, f"{safe_model_name}_{training_type}_{timestamp}")
    
    # =================
    # LLM Training Methods
    # =================
    
    def finetune_llm(
        self,
        model_name: str,
        dataset_path: str,
        training_type: str = "sft",
        output_dir: Optional[str] = None,
        dataset_format: str = "alpaca",
        use_lora: bool = True,
        batch_size: int = 4,
        num_epochs: int = 3,
        learning_rate: float = 2e-5,
        max_length: int = 1024,
        lora_rank: int = 8,
        lora_alpha: int = 16,
        val_dataset_path: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Fine-tune an LLM model.
        
        Args:
            model_name: Model identifier (e.g., "google/gemma-2-4b-it", "meta-llama/Llama-2-7b-hf")
            dataset_path: Path to training dataset
            training_type: Type of training ("sft", "dpo", "rlhf")
            output_dir: Custom output directory
            dataset_format: Dataset format ("alpaca", "sharegpt", "custom")
            use_lora: Whether to use LoRA for efficient training
            batch_size: Training batch size
            num_epochs: Number of training epochs
            learning_rate: Learning rate
            max_length: Maximum sequence length
            lora_rank: LoRA rank parameter
            lora_alpha: LoRA alpha parameter
            val_dataset_path: Path to validation dataset (optional)
            **kwargs: Additional training parameters
            
        Returns:
            Path to the trained model
            
        Example:
            ```python
            # Fine-tune Gemma 3:4B with your dataset
            model_path = factory.finetune_llm(
                model_name="google/gemma-2-4b-it",
                dataset_path="my_training_data.json",
                training_type="sft",
                use_lora=True,
                num_epochs=3,
                batch_size=4
            )
            ```
        """
        if not output_dir:
            output_dir = self._get_output_dir(model_name, training_type)
        
        # Convert format string to enum
        format_map = {
            "alpaca": DatasetFormat.ALPACA,
            "sharegpt": DatasetFormat.SHAREGPT,
            "custom": DatasetFormat.CUSTOM
        }
        dataset_format_enum = format_map.get(dataset_format, DatasetFormat.ALPACA)
        
        if training_type.lower() == "sft":
            return self.llm_factory.finetune(
                model_path=model_name,
                train_data=dataset_path,
                val_data=val_dataset_path,
                output_dir=output_dir,
                dataset_format=dataset_format_enum,
                use_lora=use_lora,
                batch_size=batch_size,
                num_epochs=num_epochs,
                learning_rate=learning_rate,
                max_length=max_length,
                lora_rank=lora_rank,
                lora_alpha=lora_alpha,
                **kwargs
            )
        else:
            raise ValueError(f"Training type '{training_type}' not supported yet. Use 'sft' for now.")
    
    def train_with_preferences(
        self,
        model_path: str,
        preference_data: str,
        output_dir: Optional[str] = None,
        reference_model: Optional[str] = None,
        beta: float = 0.1,
        use_lora: bool = True,
        batch_size: int = 4,
        num_epochs: int = 3,
        learning_rate: float = 5e-6,
        val_data: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Train model with preference data using DPO.
        
        Args:
            model_path: Path to the base model
            preference_data: Path to preference dataset
            output_dir: Custom output directory
            reference_model: Reference model for DPO (optional)
            beta: DPO beta parameter
            use_lora: Whether to use LoRA
            batch_size: Training batch size
            num_epochs: Number of epochs
            learning_rate: Learning rate
            val_data: Validation data path
            **kwargs: Additional parameters
            
        Returns:
            Path to the trained model
        """
        if not output_dir:
            model_name = os.path.basename(model_path)
            output_dir = self._get_output_dir(model_name, "dpo")
        
        return self.llm_factory.dpo(
            model_path=model_path,
            train_data=preference_data,
            val_data=val_data,
            reference_model=reference_model,
            output_dir=output_dir,
            use_lora=use_lora,
            batch_size=batch_size,
            num_epochs=num_epochs,
            learning_rate=learning_rate,
            beta=beta,
            **kwargs
        )
    
    def train_reward_model(
        self,
        model_path: str,
        reward_data: str,
        output_dir: Optional[str] = None,
        use_lora: bool = True,
        batch_size: int = 8,
        num_epochs: int = 3,
        learning_rate: float = 1e-5,
        val_data: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Train a reward model for RLHF.
        
        Args:
            model_path: Base model path
            reward_data: Reward training data
            output_dir: Output directory
            use_lora: Whether to use LoRA
            batch_size: Batch size
            num_epochs: Number of epochs
            learning_rate: Learning rate
            val_data: Validation data
            **kwargs: Additional parameters
            
        Returns:
            Path to trained reward model
        """
        if not output_dir:
            model_name = os.path.basename(model_path)
            output_dir = self._get_output_dir(model_name, "reward")
        
        return self.llm_factory.train_reward_model(
            model_path=model_path,
            train_data=reward_data,
            val_data=val_data,
            output_dir=output_dir,
            use_lora=use_lora,
            batch_size=batch_size,
            num_epochs=num_epochs,
            learning_rate=learning_rate,
            **kwargs
        )
    
    # =================
    # Image Model Training Methods
    # =================
    
    def train_image_model(
        self,
        model_type: str = "flux",
        training_images_dir: str = "",
        output_dir: Optional[str] = None,
        use_lora: bool = True,
        num_epochs: int = 1000,
        batch_size: int = 1,
        learning_rate: float = 1e-4,
        **kwargs
    ) -> str:
        """
        Train an image generation model.
        
        Args:
            model_type: Type of model ("flux", "lora")
            training_images_dir: Directory containing training images
            output_dir: Output directory
            use_lora: Whether to use LoRA
            num_epochs: Training epochs
            batch_size: Batch size
            learning_rate: Learning rate
            **kwargs: Additional parameters
            
        Returns:
            Path to trained model
        """
        if not output_dir:
            output_dir = self._get_output_dir("image_model", model_type)
        
        # TODO: Implement image model training
        logger.warning("Image model training not fully implemented yet")
        return output_dir
    
    # =================
    # Utility Methods
    # =================
    
    def get_training_status(self, output_dir: str) -> Dict[str, Any]:
        """
        Get training status from output directory.
        
        Args:
            output_dir: Training output directory
            
        Returns:
            Dictionary with training status information
        """
        status = {
            "output_dir": output_dir,
            "exists": os.path.exists(output_dir),
            "files": []
        }
        
        if status["exists"]:
            status["files"] = os.listdir(output_dir)
            
        return status
    
    def list_trained_models(self) -> List[Dict[str, Any]]:
        """
        List all trained models in the output directory.
        
        Returns:
            List of model information dictionaries
        """
        models = []
        
        if os.path.exists(self.base_output_dir):
            for item in os.listdir(self.base_output_dir):
                item_path = os.path.join(self.base_output_dir, item)
                if os.path.isdir(item_path):
                    models.append({
                        "name": item,
                        "path": item_path,
                        "created": datetime.datetime.fromtimestamp(
                            os.path.getctime(item_path)
                        ).isoformat()
                    })
        
        return sorted(models, key=lambda x: x["created"], reverse=True)

    def finetune_on_runpod(
        self,
        model_name: str,
        dataset_path: str,
        runpod_config: Dict[str, Any],
        storage_config: Optional[Dict[str, Any]] = None,
        training_params: Optional[Dict[str, Any]] = None,
        job_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fine-tune a model on RunPod cloud infrastructure.
        
        Args:
            model_name: Model identifier (e.g., "google/gemma-2-4b-it")
            dataset_path: Dataset path or HuggingFace dataset name
            runpod_config: RunPod configuration dictionary
            storage_config: Optional cloud storage configuration
            training_params: Training configuration parameters
            job_name: Optional job name for identification
            
        Returns:
            Training results with job ID and model paths
            
        Example:
            ```python
            # Configure RunPod
            runpod_config = {
                "api_key": "your-runpod-api-key",
                "template_id": "your-template-id",
                "gpu_type": "NVIDIA RTX A6000",
                "gpu_count": 1
            }
            
            # Configure storage (optional)
            storage_config = {
                "provider": "s3",
                "bucket_name": "my-training-bucket",
                "region": "us-west-2",
                "access_key": "your-access-key",
                "secret_key": "your-secret-key"
            }
            
            # Start training
            result = factory.finetune_on_runpod(
                model_name="google/gemma-2-4b-it",
                dataset_path="tatsu-lab/alpaca",
                runpod_config=runpod_config,
                storage_config=storage_config,
                training_params={
                    "num_epochs": 3,
                    "batch_size": 4,
                    "use_lora": True
                }
            )
            ```
        """
        try:
            from .cloud import RunPodConfig, StorageConfig, TrainingJobOrchestrator, JobConfig
        except ImportError:
            raise ImportError(
                "Cloud training dependencies not installed. "
                "Install with: pip install runpod boto3 google-cloud-storage"
            )
        
        if training_params is None:
            training_params = {}
        
        # Create RunPod configuration
        runpod_cfg = RunPodConfig(**runpod_config)
        
        # Create storage configuration if provided
        storage_cfg = None
        if storage_config:
            storage_cfg = StorageConfig(**storage_config)
        
        # Create job configuration
        job_cfg = JobConfig(
            model_name=model_name,
            dataset_source=dataset_path,
            job_name=job_name,
            **training_params
        )
        
        # Initialize orchestrator and execute training
        orchestrator = TrainingJobOrchestrator(
            runpod_config=runpod_cfg,
            storage_config=storage_cfg
        )
        
        logger.info(f"Starting RunPod training for {model_name}")
        result = orchestrator.execute_training_workflow(job_cfg)
        
        return result


# Convenience functions for quick access
def finetune_gemma(
    dataset_path: str,
    model_size: str = "4b",
    output_dir: Optional[str] = None,
    **kwargs
) -> str:
    """
    Quick function to fine-tune Gemma models.
    
    Args:
        dataset_path: Path to training dataset
        model_size: Model size ("2b", "4b", "7b")
        output_dir: Output directory
        **kwargs: Additional training parameters
        
    Returns:
        Path to fine-tuned model
        
    Example:
        ```python
        from isa_model.training import finetune_gemma
        
        model_path = finetune_gemma(
            dataset_path="my_data.json",
            model_size="4b",
            num_epochs=3,
            batch_size=4
        )
        ```
    """
    factory = TrainingFactory()
    
    model_map = {
        "2b": "google/gemma-2-2b-it",
        "4b": "google/gemma-2-4b-it", 
        "7b": "google/gemma-2-7b-it"
    }
    
    model_name = model_map.get(model_size, "google/gemma-2-4b-it")
    
    return factory.finetune_llm(
        model_name=model_name,
        dataset_path=dataset_path,
        output_dir=output_dir,
        **kwargs
    ) 