from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum

class ModelType(Enum):
    """Enum for different types of models."""
    CHAT = "chat"
    EMBEDDING = "embedding"

@dataclass
class ModelPricing:
    """Pricing information for a specific model."""
    input_price_per_1k: float  # Price per 1K input tokens
    output_price_per_1k: float  # Price per 1K output tokens
    model_type: ModelType

class PricingService:
    """Service for calculating token costs based on model pricing."""
    
    _PRICING_MAP: Dict[str, ModelPricing] = {
        # GPT-4 Models
        "gpt-4": ModelPricing(0.03, 0.06, ModelType.CHAT),
        "gpt-4-32k": ModelPricing(0.06, 0.12, ModelType.CHAT),
        "gpt-4-turbo": ModelPricing(0.01, 0.03, ModelType.CHAT),
        "gpt-4-turbo-preview": ModelPricing(0.01, 0.03, ModelType.CHAT),
        # "gpt-4o-2024-08-06": ModelPricing(0.015, 0.03, ModelType.CHAT),  # Optimized version
        "gpt-4o": ModelPricing(0.015, 0.03, ModelType.CHAT),  # Optimized version
        "gpt-4.1-mini": ModelPricing(0.005, 0.015, ModelType.CHAT),  # Smaller version
        "gpt-4.1": ModelPricing(0.02, 0.04, ModelType.CHAT),  # Updated version
        "o3": ModelPricing(0.008, 0.016, ModelType.CHAT),  # Optimized version 3
        
        # GPT-3.5 Models
        "gpt-3.5-turbo": ModelPricing(0.0005, 0.0015, ModelType.CHAT),
        "gpt-3.5-turbo-16k": ModelPricing(0.001, 0.002, ModelType.CHAT),
        
        # Embedding Models
        "text-embedding-3-small": ModelPricing(0.00002, 0.0, ModelType.EMBEDDING),
        "text-embedding-3-large": ModelPricing(0.00013, 0.0, ModelType.EMBEDDING),
        "text-embedding-ada-002": ModelPricing(0.0001, 0.0, ModelType.EMBEDDING),
    }

    @classmethod
    def calculate_cost(
        cls,
        model_name: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        """Calculate the cost for token usage.
        
        Args:
            model_name: Name of the model used
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            float: Total cost in USD, returns 0 if any error occurs or model not found
        """
        try:
            pricing = cls._PRICING_MAP.get(model_name)
            if not pricing:
                return 0.0
                
            # Calculate costs
            input_cost = (input_tokens / 1000) * pricing.input_price_per_1k
            output_cost = (output_tokens / 1000) * pricing.output_price_per_1k
            
            return input_cost + output_cost
        except Exception:
            return 0.0

    @classmethod
    def get_model_pricing(cls, model_name: str) -> Optional[ModelPricing]:
        """Get pricing information for a specific model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Optional[ModelPricing]: Pricing information if available
        """
        return cls._PRICING_MAP.get(model_name) 