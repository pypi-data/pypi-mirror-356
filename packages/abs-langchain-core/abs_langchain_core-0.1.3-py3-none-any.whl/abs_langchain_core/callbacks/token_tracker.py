from typing import Any, Dict, List, Optional
from uuid import uuid4
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

from ..models.usage import TokenUsage, UsageLog
from ..core.logger import UsageLogger

from abs_utils.logger import setup_logger
import asyncio
logger = setup_logger(__name__) 

class TokenTrackingCallback(BaseCallbackHandler):
    """Callback handler for tracking token usage in LangChain operations."""

    def __init__(
        self,
        logger: UsageLogger,
        operation_type: str,
        provider: str = "openai",
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the token tracking callback.

        Args:
            logger: UsageLogger instance for storing usage data
            operation_type: Type of operation (chat, rag, agent)
            user_id: Optional user ID for tracking
            metadata: Optional metadata to include in the usage log
        """
        self.logger = logger
        self.operation_type = operation_type
        self.provider = provider
        self.user_id = user_id
        self.metadata = metadata or {}
        self.request_id = str(uuid4())
        self._current_usage = TokenUsage(
            model_name=self.metadata.get("model_name", ""),
            metadata=self.metadata
        )

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts."""
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends generating."""
        if not response.usage_metadata:
            return

        # Extract token usage from the response
        usage = response.usage_metadata
        if not usage:
            return

        # Update current usage
        self._current_usage.prompt_tokens = usage.get("input_tokens", 0)
        self._current_usage.completion_tokens = usage.get("output_tokens", 0)
        self._current_usage.total_tokens = usage.get("total_tokens", 0)
        self._current_usage.model_name = response.llm_output.get("model_name", "")

        # Calculate cost using pricing service - local import to avoid circular dependency
        from ..services.pricing import PricingService
        self._current_usage.cost_usd = PricingService.calculate_cost(
            model_name=self.metadata.get("model_name", ""),
            input_tokens=self._current_usage.prompt_tokens,
            output_tokens=self._current_usage.completion_tokens,
        )
        logger.info(f"Cost: {self._current_usage.cost_usd}")

        # Create and store usage log
        usage_log = UsageLog(
            user_id=self.user_id,
            request_id=self.request_id,
            usage=self._current_usage,
            operation_type=self.operation_type,
            provider=self.provider,
        )
        self.logger.log_usage(usage_log)

    def on_embedding_end(self, response: Dict[str, Any], **kwargs: Any) -> None:
        """Run when embedding ends."""
        logger.info(f"Embedding end: {response}")
        
        # Extract token usage from the response
        usage = response.get("usage", {})
        if not usage:
            return

        # Update current usage
        self._current_usage.prompt_tokens = usage.get("prompt_tokens", 0)
        self._current_usage.completion_tokens = 0  # Embeddings don't have completion tokens
        self._current_usage.total_tokens = usage.get("total_tokens", 0)
        self._current_usage.model_name = self.metadata.get("model_name", "")

        # Calculate cost using pricing service - local import to avoid circular dependency
        from ..services.pricing import PricingService
        self._current_usage.cost_usd = PricingService.calculate_cost(
            model_name=self.metadata.get("model_name", ""),
            input_tokens=self._current_usage.prompt_tokens,
            output_tokens=self._current_usage.completion_tokens,
        )
        # Create and store usage log
        usage_log = UsageLog(
            user_id=self.user_id,
            request_id=self.request_id,
            usage=self._current_usage,
            operation_type=self.operation_type,
            provider=self.provider,
        )
        self.logger.log_usage(usage_log)

    def _extract_usage(self, response: LLMResult) -> Optional[Dict[str, Any]]:
        try:
            first_chunk = response.generations[0][0].message
            usage = getattr(first_chunk, "usage_metadata", None)
            model_name = getattr(first_chunk, "response_metadata", {}).get("model_name", "")
            return usage, model_name
        except Exception:
            return None, ""

    def _finalize_usage(self, usage: Dict[str, Any], model_name: str):
        self._current_usage.prompt_tokens = usage.get("input_tokens", 0)
        self._current_usage.completion_tokens = usage.get("output_tokens", 0)
        self._current_usage.total_tokens = usage.get("total_tokens", 0)
        self._current_usage.model_name = model_name
        
        # Calculate cost using pricing service - local import to avoid circular dependency
        from ..services.pricing import PricingService
        self._current_usage.cost_usd = PricingService.calculate_cost(
            model_name=self.metadata.get("model_name", ""),
            input_tokens=self._current_usage.prompt_tokens,
            output_tokens=self._current_usage.completion_tokens,
        )

        usage_log = UsageLog(
            user_id=self.user_id,
            request_id=self.request_id,
            usage=self._current_usage,
            operation_type=self.operation_type,
            provider=self.provider,
        )
        self.logger.log_usage(usage_log)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        asyncio.create_task(self._handle_llm_end(response))

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        await self._handle_llm_end(response)

    async def _handle_llm_end(self, response: LLMResult):
        usage, model_name = self._extract_usage(response)
        if usage:
            self._finalize_usage(usage, model_name)

    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        usage_log = UsageLog(
            user_id=self.user_id,
            request_id=self.request_id,
            usage=self._current_usage,
            operation_type=self.operation_type,
            status="error",
            error_message=str(error),
            provider=self.provider,
        )
        self.logger.log_usage(usage_log)

    async def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        self.on_llm_error(error, **kwargs)