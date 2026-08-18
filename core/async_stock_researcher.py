import asyncio
import json
import os

import instructor
from dotenv import load_dotenv
from openai import AsyncOpenAI

from schemas.stock_schema import StockAnalysis

# 1. Professional Environment & Client Setup
load_dotenv() # Securely load API keys from .env [2, 8]

# 'patch' or 'from_openai' allows the client to handle Pydantic models [3, 9]
client = instructor.from_openai(AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")))

# 2. Asynchronous Research Worker
async def research_stock(ticker: str) -> StockAnalysis:
    """
    Performs concurrent research and returns a validated StockAnalysis object.
    """
    print(f"📡 Analyzing {ticker}...")
    try:
        # The 'response_model' parameter forces the LLM to follow your Pydantic schema [4, 9]
        analysis = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_model=StockAnalysis,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional equity researcher. Provide a detailed analysis based on the latest market data."
                },
                {"role": "user", "content": f"Perform a research task for ticker: {ticker}"}
            ]
        )
        return analysis
    except Exception as e:
        print(f"❌ Error researching {ticker}: {e}")
        return None

# 3. Orchestration Layer
async def main():
    tickers = ["AAPL", "TSLA", "NVDA"]
    
    print(f"🚀 Starting concurrent research for {tickers}...\n")
    
    # asyncio.gather triggers all API calls simultaneously to avoid latency [4, 9, 10]
    tasks = [research_stock(t) for t in tickers]
    results = await asyncio.gather(*tasks)
    
    # Filter out any failed tasks and convert Pydantic objects to dictionaries for JSON storage
    valid_results = [r.model_dump() for r in results if r is not None]
    
    # 4. Data Persistence [11, 12]
    with open("stock_analysis_results.json", "w") as f:
        json.dump(valid_results, f, indent=4)
    
    print(f"\n✅ Research Complete. Processed {len(valid_results)} stocks.")
    print("Results saved to 'stock_analysis_results.json'")

if __name__ == "__main__":
    asyncio.run(main())