# core/async_stock_researcher_with_cost.py

import asyncio
import os
import json
import instructor
from dotenv import load_dotenv
from openai import AsyncOpenAI
from schemas.stock_schema import StockAnalysis
from utils.token_tracker import calculate_cost, log_api_cost

load_dotenv()

# Initialize the instructor client
client = instructor.from_openai(AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY")))

async def research_stock(ticker: str) -> dict:
    """
    Performs concurrent research and tracks exact token costs.
    """
    print(f"📡 Analyzing {ticker}...")
    model_name = "gpt-4o-mini"
    
    try:
        # 'create_with_completion' returns BOTH the parsed Pydantic object
        # AND the raw completion metadata (containing token usage)
        analysis, completion = await client.chat.completions.create_with_completion(
            model=model_name,
            response_model=StockAnalysis,
            messages=[
                {"role": "system", "content": "You are a professional equity researcher."},
                {"role": "user", "content": f"Perform a research task for ticker: {ticker}"}
            ]
        )
        
        # Calculate token costs
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        cost_record = calculate_cost(model_name, prompt_tokens, completion_tokens)
        
        # Log to terminal
        log_api_cost(ticker, cost_record)
        
        # Merge structured analysis data with the cost breakdown
        result_data = analysis.model_dump()
        result_data["cost_metadata"] = {
            "model_used": cost_record.model,
            "prompt_tokens": cost_record.prompt_tokens,
            "completion_tokens": cost_record.completion_tokens,
            "usd_cost": cost_record.usd_cost
        }
        
        return result_data

    except Exception as e:
        print(f"❌ Error researching {ticker}: {e}")
        return None

async def main():
    tickers = ["AAPL", "TSLA", "NVDA"]
    print(f"🚀 Starting concurrent research and budget tracking for {tickers}...\n")
    
    tasks = [research_stock(t) for t in tickers]
    results = await asyncio.gather(*tasks)
    
    valid_results = [r for r in results if r is not None]
    
    # Calculate aggregate session cost
    total_spend = sum(r["cost_metadata"]["usd_cost"] for r in valid_results)
    
    output_package = {
        "session_summary": {
            "total_stocks_processed": len(valid_results),
            "total_usd_spend": round(total_spend, 6)
        },
        "results": valid_results
    }
    
    # Save results locally
    with open("stock_analysis_with_cost.json", "w") as f:
        json.dump(output_package, f, indent=4)
        
    print(f"\n✅ Pipeline Complete. Run cost: ${total_spend:.6f}")
    print("Results and cost metadata saved to 'stock_analysis_with_cost.json'")

if __name__ == "__main__":
    asyncio.run(main())
