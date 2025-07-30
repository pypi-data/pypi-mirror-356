from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from ..interfaces.embedding_provider import EmbeddingProvider
from ..core.logger import UsageLogger
from abs_exception_core.exceptions import GenericHttpError
from ..callbacks.token_tracker import TokenTrackingCallback
from abs_utils.logger import setup_logger
from langchain.callbacks.manager import CallbackManager

logger = setup_logger(__name__)


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider implementation."""

    def __init__(
        self,
        model_name: str = "text-embedding-3-small",
        log_to_mongo: bool = True,
        mongo_uri: Optional[str] = None,
        mongo_db: str = "langchain_usage",
        mongo_collection: str = "usage_logs",
        log_dir: Optional[str] = None,
        log_to_file: bool = False,
        enable_logging: bool = False,
        **kwargs
    ):
        """Initialize the OpenAI embedding provider.
        
        Args:
            model_name: Name of the OpenAI embedding model to use
            enable_logging: Whether to enable usage logging
            **kwargs: Additional arguments to pass to OpenAIEmbeddings
            
        Raises:
            EmbeddingError: If initialization fails
        """
        self._model_name = model_name
        self._callbacks = []
        self._kwargs = kwargs  # Store kwargs for later use
        
        try:
            if enable_logging:
                self.usage_logger = UsageLogger(
                    log_to_mongo=log_to_mongo,
                    mongo_uri=mongo_uri,
                    mongo_db=mongo_db,
                    mongo_collection=mongo_collection,
                    log_dir=log_dir,
                    log_to_file=log_to_file,
                )
                token_callback = TokenTrackingCallback(
                    logger=self.usage_logger,
                    operation_type="embedding",
                    metadata={"model_name": self.model_name},
                )
                self._callbacks = [token_callback]
                callback_manager = CallbackManager(self._callbacks)
                logger.info(f"Initialized callbacks: {self._callbacks}")
            
            # Remove callbacks and logger from kwargs to prevent passing to underlying client
            client_kwargs = {k: v for k, v in kwargs.items() if k not in ['callbacks', 'logger']}
            self._embeddings = OpenAIEmbeddings(
                model=self.model_name,
                tiktoken_enabled=True,
                tiktoken_model_name=self.model_name,
                **client_kwargs
            )
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI provider: {str(e)}")
            raise GenericHttpError(f"Failed to initialize OpenAI provider: {str(e)}")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using OpenAI.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings
            
        Raises:
            EmbeddingError: If embedding fails
        """
        try:
            return self._embeddings.embed_documents(texts)
        except Exception as e:
            logger.error(f"Failed to embed documents: {str(e)}")
            raise GenericHttpError(f"Failed to embed documents: {str(e)}")

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query text using OpenAI.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding as a list of floats
            
        Raises:
            EmbeddingError: If embedding fails
        """
        try:
            return self._embeddings.embed_query(text)
        except Exception as e:
            logger.error(f"Failed to embed query: {str(e)}")
            raise GenericHttpError(f"Failed to embed query: {str(e)}")

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Asynchronously embed a list of documents using OpenAI.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings
            
        Raises:
            EmbeddingError: If embedding fails
        """
        try:
            # Create a new instance without callbacks and logger for async operations
            async_embeddings = OpenAIEmbeddings(
                model=self.model_name,
                **{k: v for k, v in self._kwargs.items() if k not in ['callbacks', 'logger']}
            )
            return await async_embeddings.aembed_documents(texts)
        except Exception as e:
            logger.error(f"Failed to embed documents asynchronously: {str(e)}")
            raise GenericHttpError(f"Failed to embed documents asynchronously: {str(e)}")

    async def aembed_query(self, text: str) -> List[float]:
        """Asynchronously embed a single query text using OpenAI.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding as a list of floats
            
        Raises:
            EmbeddingError: If embedding fails
        """
        try:
            # Create a new instance without callbacks and logger for async operations
            async_embeddings = OpenAIEmbeddings(
                model=self.model_name,
                **{k: v for k, v in self._kwargs.items() if k not in ['callbacks', 'logger']}
            )
            embedding = await self._embeddings.aembed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Failed to embed query asynchronously: {str(e)}")
            raise GenericHttpError(f"Failed to embed query asynchronously: {str(e)}")

    @property
    def embedding_dimensions(self) -> int:
        """Get the dimensions of the OpenAI embeddings.
        
        Returns:
            Number of dimensions in the embedding vectors
        """
        # OpenAI's text-embedding-3-small has 1536 dimensions
        # text-embedding-3-large has 3072 dimensions
        return 1536 if "small" in self.model_name else 3072

    @property
    def model_name(self) -> str:
        """Get the name of the embedding model.
        
        Returns:
            Name of the model being used
        """
        return self._model_name 