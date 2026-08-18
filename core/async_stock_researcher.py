import asyncio
import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI

# 1. Professional Environment Setup [3]
load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Asynchronous Worker Function [2]
async def fetch_stock_news(ticker):
    print(f"📡 Fetching latest news events for: {ticker}...")
    try:
        # Programmatic API call using the Async client
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial researcher. Provide 5 recent news events for the given ticker."},
                {"role": "user", "content": f"Ticker: {ticker}"}
            ]
        )
        # In Module 3, we will transition this to Structured JSON [2]
        return {
            "ticker": ticker,
            "news": response.choices[0].message.content
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


# 3. Orchestration Layer using asyncio.gather() [2, 4]
async def main():
    tickers = ["AAPL", "TSLA", "NVDA"]
    
    print(f"🚀 Starting concurrent research for {tickers}...\n")
    
    # Triggering multiple API calls simultaneously
    results = await asyncio.gather(*[fetch_stock_news(t) for t in tickers])
    
    # 4. Data Persistence [4]
    with open("stock_news_results.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print("\n✅ Research Complete. Results saved to stock_news_results.json")

if __name__ == "__main__":
    asyncio.run(main())