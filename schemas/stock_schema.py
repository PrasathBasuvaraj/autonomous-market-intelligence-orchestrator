from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class TradeSignal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class StockAnalysis(BaseModel):
    """
    Schema for the final structured output of the Concurrent Stock Researcher.
    Ensures the agent returns validated data ready for downstream systems.
    """
    ticker: str = Field(..., description="The stock ticker symbol (e.g., AAPL)")
    trade_signal: TradeSignal = Field(..., description="The recommended action: BUY, SELL, or HOLD")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in the signal from 0 to 1")
    key_news_summary: List[str] = Field(..., min_items=3, max_items=3, description="A list of the top 3 recent news events")
    reasoning: str = Field(..., description="A brief explanation for the trade signal and confidence score")
