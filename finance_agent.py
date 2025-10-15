import os
from dotenv import load_dotenv

from news_service import NewsService
from llm_agent import LLMAgent

import json

def main():
    """Main function to monitor the portfolio and fetch news."""
    load_dotenv()

    # --- Step 1: Load watchlist ---
    with open('watchlist.json', 'r') as f:
        watchlist = json.load(f)

    news_service = NewsService()

    # --- Step 2: Fetch, display, and summarize news ---
    print("\n--- Recent News Summary ---")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("GEMINI_API_KEY not found in .env file. Skipping news summarization.")
    else:
        llm_agent = LLMAgent(gemini_api_key)
        for ticker in watchlist:
            print(f"\n--- News Summary for {ticker} ---")
            
            news_articles = news_service.get_news(ticker)
            summary = llm_agent.summarize_news(news_articles)
            print(summary)

if __name__ == "__main__":
    main()
