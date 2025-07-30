from typing import Optional, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel

from ..callbacks.token_tracker import TokenTrackingCallback
from ..core.logger import UsageLogger


class LLMProvider:
    """Provider for LangChain LLM models with token tracking."""

    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        log_to_mongo: bool = True,
        mongo_uri: Optional[str] = None,
        mongo_db: str = "langchain_usage",
        mongo_collection: str = "usage_logs",
        log_dir: Optional[str] = None,
        log_to_file: bool = False,
        logger: Optional[bool] = False,
        callbacks: Optional[List[Any]] = None,
        operation_type: str = "chat",
        **kwargs: Any,
    ):
        """Initialize the LLM provider.

        Args:
            model_name: Name of the model to use
            temperature: Temperature for generation
            logger: Optional usage logger
            callbacks: Additional callbacks to use
            operation_type: Type of operation being performed (e.g., "chat", "agent")
            **kwargs: Additional arguments to pass to the model
        """
        self.model_name = model_name
        self.temperature = temperature
        self.logger = logger
        self.kwargs = kwargs
        self.operation_type = operation_type

        # Initialize callbacks
        self.callbacks = callbacks or []
        if logger:
            self.usage_logger = UsageLogger(
                log_to_mongo=log_to_mongo,
                mongo_uri=mongo_uri,
                mongo_db=mongo_db,
                mongo_collection=mongo_collection,
                log_dir=log_dir,
                log_to_file=log_to_file,
            )

    def get_chat_model(self) -> BaseChatModel:
        """Get a chat model instance with configured callbacks.

        Returns:
            BaseChatModel: Configured chat model instance
        """
        if self.logger:
            self.callbacks.append(
                TokenTrackingCallback(
                    logger=self.usage_logger,
                    operation_type=self.operation_type,
                    metadata={"model_name": self.model_name, "temperature": self.temperature},
                )
            )
        return ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
            callbacks=self.callbacks,
            **self.kwargs,
        )

    async def aget_chat_model(self) -> BaseChatModel:
        """Get an async chat model instance with configured callbacks.

        Returns:
            BaseChatModel: Configured async chat model instance
        """
        if self.logger:
            self.callbacks.append(
                TokenTrackingCallback(
                    logger=self.usage_logger,
                    operation_type=self.operation_type,
                    metadata={"model_name": self.model_name, "temperature": self.temperature},
                )
            )
        return ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
            callbacks=self.callbacks,
            streaming=True,  # Enable streaming for async
            stream_usage=True,  # Enable token usage tracking
            **self.kwargs,
        )

    def get_embedding_model(self):
        """Get an embedding model instance.

        Returns:
            Embedding model instance
        """
        # TODO: Implement embedding model provider
        raise NotImplementedError("Embedding model provider not implemented yet")

    def get_completion_model(self):
        """Get a completion model instance.

        Returns:
            Completion model instance
        """
        # TODO: Implement completion model provider
        raise NotImplementedError("Completion model provider not implemented yet") 