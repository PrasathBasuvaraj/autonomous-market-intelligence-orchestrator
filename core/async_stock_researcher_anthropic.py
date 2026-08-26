import asyncio
import json
import os

import instructor
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

from schemas.stock_schema import StockAnalysis

# 1. Professional Environment & Client Setup
load_dotenv()

# 'from_anthropic' patches the AsyncAnthropic client to handle your Pydantic schemas
client = instructor.from_anthropic(AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY")))

# 2. Asynchronous Research Worker for Anthropic
async def research_stock(ticker: str) -> StockAnalysis:
    """
    Performs concurrent research using Claude and returns a validated StockAnalysis object.
    """
    print(f"📡 Analyzing {ticker} with Claude...")
    try:
        # Anthropic calls require 'max_tokens' and handle 'system' instructions as a top-level parameter
        analysis = await client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            system="You are a professional equity researcher. Provide a detailed analysis based on the latest market data.",
            response_model=StockAnalysis,
            messages=[
                {"role": "user", "content": f"Perform a research task for ticker: {ticker}"}
            ]
        )
        return analysis
    except Exception as e:
        print(f"❌ Error researching {ticker} via Anthropic: {e}")
        return None

# 3. Orchestration Layer
async def main():
    tickers = ["AAPL", "TSLA", "NVDA"]
    
    print(f"🚀 Starting concurrent Anthropic research for {tickers}...\n")
    
    # asyncio.gather triggers all Claude API calls simultaneously to avoid latency
    tasks = [research_stock(t) for t in tickers]
    results = await asyncio.gather(*tasks)
    
    # Filter out failed runs and dump Pydantic models to JSON-serialisable dicts
    valid_results = [r.model_dump() for r in results if r is not None]
    
    # 4. Data Persistence
    with open("stock_analysis_anthropic_results.json", "w") as f:
        json.dump(valid_results, f, indent=4)
    
    print(f"\n✅ Research Complete. Processed {len(valid_results)} stocks.")
    print("Results saved to 'stock_analysis_anthropic_results.json'")

if __name__ == "__main__":
    asyncio.run(main())