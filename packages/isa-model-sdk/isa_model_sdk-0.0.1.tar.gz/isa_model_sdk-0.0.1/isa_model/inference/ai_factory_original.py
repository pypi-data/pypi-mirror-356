from typing import Dict, Type, Any, Optional, Tuple
import logging
from isa_model.inference.providers.base_provider import BaseProvider
from isa_model.inference.services.base_service import BaseService
from isa_model.inference.base import ModelType
import os

# 设置基本的日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIFactory:
    """
    Factory for creating AI services based on the Single Model pattern.
    """
    
    _instance = None
    _is_initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the AI Factory."""
        self.triton_url = os.environ.get("TRITON_URL", "http://localhost:8000")
        
        # Cache for services (singleton pattern)
        self._llm_services = {}
        self._embedding_services = {}
        self._speech_services = {}
        
        if not self._is_initialized:
            self._providers: Dict[str, Type[BaseProvider]] = {}
            self._services: Dict[Tuple[str, ModelType], Type[BaseService]] = {}
            self._cached_services: Dict[str, BaseService] = {}
            self._initialize_defaults()
            AIFactory._is_initialized = True
    
    def _initialize_defaults(self):
        """Initialize default providers and services"""
        try:
            # Import providers and services
            from isa_model.inference.providers.ollama_provider import OllamaProvider
            from isa_model.inference.services.embedding.ollama_embed_service import OllamaEmbedService
            from isa_model.inference.services.llm.ollama_llm_service import OllamaLLMService
            
            # Register Ollama provider and services
            self.register_provider('ollama', OllamaProvider)
            self.register_service('ollama', ModelType.EMBEDDING, OllamaEmbedService)
            self.register_service('ollama', ModelType.LLM, OllamaLLMService)
            
            # Register Ollama vision service
            try:
                from isa_model.inference.services.vision.ollama_vision_service import OllamaVisionService
                self.register_service('ollama', ModelType.VISION, OllamaVisionService)
                logger.info("Ollama vision service registered successfully")
            except ImportError as e:
                logger.warning(f"Ollama vision service not available: {e}")
            
            # Register OpenAI provider and services
            try:
                from isa_model.inference.providers.openai_provider import OpenAIProvider
                from isa_model.inference.services.llm.openai_llm_service import OpenAILLMService
                
                self.register_provider('openai', OpenAIProvider)
                self.register_service('openai', ModelType.LLM, OpenAILLMService)
                logger.info("OpenAI services registered successfully")
            except ImportError as e:
                logger.warning(f"OpenAI services not available: {e}")
            
            # Register Replicate provider and services
            try:
                from isa_model.inference.providers.replicate_provider import ReplicateProvider
                from isa_model.inference.services.vision.replicate_image_gen_service import ReplicateVisionService
                
                self.register_provider('replicate', ReplicateProvider)
                self.register_service('replicate', ModelType.VISION, ReplicateVisionService)
                logger.info("Replicate provider and vision service registered successfully")
            except ImportError as e:
                logger.warning(f"Replicate services not available: {e}")
            except Exception as e:
                logger.warning(f"Error registering Replicate services: {e}")
            
            # Try to register Triton services
            try:
                from isa_model.inference.providers.triton_provider import TritonProvider
                
                self.register_provider('triton', TritonProvider)
                logger.info("Triton provider registered successfully")
                
            except ImportError as e:
                logger.warning(f"Triton provider not available: {e}")
            
            logger.info("Default AI providers and services initialized with backend architecture")
        except Exception as e:
            logger.error(f"Error initializing default providers and services: {e}")
            # Don't raise - allow factory to work even if some services fail to load
            logger.warning("Some services may not be available due to import errors")
    
    def register_provider(self, name: str, provider_class: Type[BaseProvider]) -> None:
        """Register an AI provider"""
        self._providers[name] = provider_class
    
    def register_service(self, provider_name: str, model_type: ModelType, 
                        service_class: Type[BaseService]) -> None:
        """Register a service type with its provider"""
        self._services[(provider_name, model_type)] = service_class
    
    def create_service(self, provider_name: str, model_type: ModelType, 
                      model_name: str, config: Optional[Dict[str, Any]] = None) -> BaseService:
        """Create a service instance"""
        try:
            cache_key = f"{provider_name}_{model_type}_{model_name}"
            
            if cache_key in self._cached_services:
                return self._cached_services[cache_key]
            
            # 基础配置
            base_config = {
                "log_level": "INFO"
            }
            
            # 合并配置
            service_config = {**base_config, **(config or {})}
            
            # 创建 provider 和 service
            provider_class = self._providers[provider_name]
            service_class = self._services.get((provider_name, model_type))
            
            if not service_class:
                raise ValueError(
                    f"No service registered for provider {provider_name} and model type {model_type}"
                )
            
            provider = provider_class(config=service_config)
            service = service_class(provider=provider, model_name=model_name)
            
            self._cached_services[cache_key] = service
            return service
            
        except Exception as e:
            logger.error(f"Error creating service: {e}")
            raise
    
    # Convenient methods for common services
    def get_llm(self, model_name: str = "llama3.1", provider: str = "ollama",
                config: Optional[Dict[str, Any]] = None, api_key: Optional[str] = None) -> BaseService:
        """
        Get a LLM service instance
        
        Args:
            model_name: Name of the model to use
            provider: Provider name ('ollama', 'openai', 'replicate', etc.)
            config: Optional configuration dictionary
            api_key: Optional API key for the provider (OpenAI, Replicate, etc.)
            
        Returns:
            LLM service instance
            
        Example:
            # Using with API key directly
            llm = AIFactory.get_instance().get_llm(
                model_name="gpt-4o-mini", 
                provider="openai", 
                api_key="your-api-key-here"
            )
            
            # Using without API key (will use environment variable)
            llm = AIFactory.get_instance().get_llm(
                model_name="gpt-4o-mini", 
                provider="openai"
            )
        """
        
        # Special case for DeepSeek service
        if model_name.lower() in ["deepseek", "deepseek-r1", "qwen3-8b"]:
            if "deepseek" in self._cached_services:
                return self._cached_services["deepseek"]
        
        # Special case for Llama3-8B direct service
        if model_name.lower() in ["llama3", "llama3-8b", "meta-llama-3"]:
            if "llama3" in self._cached_services:
                return self._cached_services["llama3"]
        
        basic_config: Dict[str, Any] = {
            "temperature": 0
        }
        
        # Add API key to config if provided
        if api_key:
            if provider == "openai":
                basic_config["api_key"] = api_key
            elif provider == "replicate":
                basic_config["api_token"] = api_key
            else:
                logger.warning(f"API key provided but provider '{provider}' may not support it")
        
        if config:
            basic_config.update(config)
        return self.create_service(provider, ModelType.LLM, model_name, basic_config)
    
    def get_vision_model(self, model_name: str = "gemma3-4b", provider: str = "triton",
                       config: Optional[Dict[str, Any]] = None, api_key: Optional[str] = None) -> BaseService:
        """
        Get a vision model service instance
        
        Args:
            model_name: Name of the model to use
            provider: Provider name ('openai', 'replicate', 'triton', etc.)
            config: Optional configuration dictionary
            api_key: Optional API key for the provider (OpenAI, Replicate, etc.)
            
        Returns:
            Vision service instance
            
        Example:
            # Using with API key directly
            vision = AIFactory.get_instance().get_vision_model(
                model_name="gpt-4o", 
                provider="openai", 
                api_key="your-api-key-here"
            )
            
            # Using Replicate for image generation
            image_gen = AIFactory.get_instance().get_vision_model(
                model_name="stability-ai/sdxl", 
                provider="replicate", 
                api_key="your-replicate-token"
            )
        """
        
        # Special case for Gemma3-4B direct service
        if model_name.lower() in ["gemma3", "gemma3-4b", "gemma3-vision"]:
            if "gemma3" in self._cached_services:
                return self._cached_services["gemma3"]
        
        # Special case for Replicate's image generation models
        if provider == "replicate" and "/" in model_name:
            replicate_config: Dict[str, Any] = {
                "guidance_scale": 7.5,
                "num_inference_steps": 30
            }
            
            # Add API key if provided
            if api_key:
                replicate_config["api_token"] = api_key
            
            if config:
                replicate_config.update(config)
            return self.create_service(provider, ModelType.VISION, model_name, replicate_config)
        
        basic_config: Dict[str, Any] = {
            "temperature": 0.7,
            "max_new_tokens": 512
        }
        
        # Add API key to config if provided
        if api_key:
            if provider == "openai":
                basic_config["api_key"] = api_key
            elif provider == "replicate":
                basic_config["api_token"] = api_key
            else:
                logger.warning(f"API key provided but provider '{provider}' may not support it")
        
        if config:
            basic_config.update(config)
        return self.create_service(provider, ModelType.VISION, model_name, basic_config)
    
    def get_embedding(self, model_name: str = "bge-m3", provider: str = "ollama",
                     config: Optional[Dict[str, Any]] = None) -> BaseService:
        """Get an embedding service instance"""
        return self.create_service(provider, ModelType.EMBEDDING, model_name, config)
    
    def get_rerank(self, model_name: str = "bge-m3", provider: str = "ollama",
                   config: Optional[Dict[str, Any]] = None) -> BaseService:
        """Get a rerank service instance"""
        return self.create_service(provider, ModelType.RERANK, model_name, config)
    
    def get_embed_service(self, model_name: str = "bge-m3", provider: str = "ollama",
                         config: Optional[Dict[str, Any]] = None) -> BaseService:
        """Get an embedding service instance"""
        return self.get_embedding(model_name, provider, config)
    
    def get_speech_model(self, model_name: str = "whisper_tiny", provider: str = "triton",
                       config: Optional[Dict[str, Any]] = None) -> BaseService:
        """Get a speech-to-text model service instance"""
        
        # Special case for Whisper Tiny direct service
        if model_name.lower() in ["whisper", "whisper_tiny", "whisper-tiny"]:
            if "whisper" in self._cached_services:
                return self._cached_services["whisper"]
        
        basic_config = {
            "language": "en",
            "task": "transcribe"
        }
        if config:
            basic_config.update(config)
        return self.create_service(provider, ModelType.AUDIO, model_name, basic_config)
    
    async def get_embedding_service(self, model_name: str) -> Any:
        """
        Get an embedding service for the specified model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Embedding service instance
        """
        if model_name in self._embedding_services:
            return self._embedding_services[model_name]
        
        else:
            raise ValueError(f"Unsupported embedding model: {model_name}")
    
    async def get_speech_service(self, model_name: str) -> Any:
        """
        Get a speech service for the specified model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Speech service instance
        """
        if model_name in self._speech_services:
            return self._speech_services[model_name]
        
    
    def get_model_info(self, model_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about available models.
        
        Args:
            model_type: Optional filter for model type
            
        Returns:
            Dict of model information
        """
        models = {
            "llm": [
                {"name": "deepseek", "description": "DeepSeek-R1-0528-Qwen3-8B language model"},
                {"name": "llama", "description": "Llama3-8B language model"},
                {"name": "gemma", "description": "Gemma3-4B language model"}
            ],
            "embedding": [
                {"name": "bge_embed", "description": "BGE-M3 text embedding model"}
            ],
            "speech": [
                {"name": "whisper", "description": "Whisper-tiny speech-to-text model"}
            ]
        }
        
        if model_type:
            return {model_type: models.get(model_type, [])}
        return models
    
    @classmethod
    def get_instance(cls) -> 'AIFactory':
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance