# utils/token_tracker.py

from typing import Dict, Any
from dataclasses import dataclass

# 2026 Active Model Pricing per 1 Million Tokens (in USD)
MODEL_PRICING = {
    # OpenAI Models
    "gpt-4o": {"input": 5.00, "output": 15.00},
    "gpt-4o-mini": {"input": 0.150, "output": 0.600},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    
    # Anthropic Models (Claude 4/5 Generations)
    "claude-sonnet-5": {"input": 2.00, "output": 10.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00},
}

@dataclass
class CostRecord:
    model: str
    prompt_tokens: int
    completion_tokens: int
    usd_cost: float

def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> CostRecord:
    """
    Calculates the exact USD cost of an API call based on model pricing.
    """
    pricing = MODEL_PRICING.get(model, {"input": 3.00, "output": 15.00}) # Default fallback rate
    
    input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
    output_cost = (completion_tokens / 1_000_000) * pricing["output"]
    total_cost = input_cost + output_cost
    
    return CostRecord(
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        usd_cost=round(total_cost, 6)
    )

def log_api_cost(ticker: str, cost_record: CostRecord) -> None:
    """
    Prints a formatted summary of the token usage and cost in the terminal.
    """
    print(f"\n[📊 Cost Log] Ticker: {ticker} | Model: {cost_record.model}")
    print(f"  └─ Tokens: {cost_record.prompt_tokens} prompt | {cost_record.completion_tokens} completion")
    print(f"  └─ USD Cost: ${cost_record.usd_cost:.6f}")
