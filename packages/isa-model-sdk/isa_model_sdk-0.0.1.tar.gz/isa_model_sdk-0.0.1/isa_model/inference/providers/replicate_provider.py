from isa_model.inference.providers.base_provider import BaseProvider
from isa_model.inference.base import ModelType, Capability
from typing import Dict, List, Any
import logging
import os

logger = logging.getLogger(__name__)

class ReplicateProvider(BaseProvider):
    """Provider for Replicate API"""
    
    def __init__(self, config=None):
        """
        Initialize the Replicate Provider
        
        Args:
            config (dict, optional): Configuration for the provider
                - api_token: Replicate API token (can be passed here or via environment variable)
                - timeout: Timeout for API calls in seconds
        """
        default_config = {
            "api_token": "",  # Will be set from config or environment
            "timeout": 60,
            "stream": True,
            "max_tokens": 1024
        }
        
        # Merge default config with provided config
        merged_config = {**default_config, **(config or {})}
        
        # Set API token from config first, then fallback to environment variable
        if not merged_config["api_token"]:
            merged_config["api_token"] = os.environ.get("REPLICATE_API_TOKEN", "")
        
        super().__init__(config=merged_config)
        self.name = "replicate"
        
        logger.info(f"Initialized ReplicateProvider")
        
        # Only warn if no API token is provided at all
        if not self.config["api_token"]:
            logger.info("Replicate API token not provided. You can set it via REPLICATE_API_TOKEN environment variable or pass it in the config when creating services.")
    
    def set_api_token(self, api_token: str):
        """
        Set the API token after initialization
        
        Args:
            api_token: Replicate API token
        """
        self.config["api_token"] = api_token
        logger.info("Replicate API token updated")
    
    def get_capabilities(self) -> Dict[ModelType, List[Capability]]:
        """Get provider capabilities by model type"""
        return {
            ModelType.LLM: [
                Capability.CHAT, 
                Capability.COMPLETION
            ],
            ModelType.VISION: [
                Capability.IMAGE_GENERATION,
                Capability.MULTIMODAL_UNDERSTANDING
            ],
            ModelType.AUDIO: [
                Capability.SPEECH_TO_TEXT,
                Capability.TEXT_TO_SPEECH
            ]
        }
    
    def get_models(self, model_type: ModelType) -> List[str]:
        """Get available models for given type"""
        if model_type == ModelType.LLM:
            return [
                "meta/llama-3-70b-instruct",
                "meta/llama-3-8b-instruct",
                "anthropic/claude-3-opus-20240229",
                "anthropic/claude-3-sonnet-20240229"
            ]
        elif model_type == ModelType.VISION:
            return [
                "stability-ai/sdxl",
                "stability-ai/stable-diffusion-3-medium",
                "meta/llama-3-70b-vision",
                "anthropic/claude-3-opus-20240229",
                "anthropic/claude-3-sonnet-20240229"
            ]
        elif model_type == ModelType.AUDIO:
            return [
                "openai/whisper",
                "suno-ai/bark"
            ]
        else:
            return []
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        # Return a copy without sensitive information
        config_copy = self.config.copy()
        if "api_token" in config_copy:
            config_copy["api_token"] = "***" if config_copy["api_token"] else ""
        return config_copy
    
    def is_reasoning_model(self, model_name: str) -> bool:
        """Check if the model is optimized for reasoning tasks"""
        reasoning_models = ["llama-3-70b", "claude-3-opus", "claude-3-sonnet"]
        return any(rm in model_name.lower() for rm in reasoning_models) 