import os
from dotenv import load_dotenv
from src.trading212_service import Trading212
from src.news_service import NewsService
from src.agents.llm_agent import LLMAgent
import json

def load_watchlist():
    """Loads the watchlist from watchlist.json."""
    with open('watchlist.json', 'r') as f:
        return set(json.load(f))

def fetch_portfolio_tickers(trading212):
    """Fetches portfolio tickers from Trading 212."""
    tickers = set()
    positions_data = trading212.get_portfolio()
    if positions_data:
        for position in positions_data:
            ticker = position.get('ticker')
            if ticker:
                tickers.add(ticker)
    return tickers

def main():
    """Main function to monitor the portfolio and fetch news."""
    load_dotenv()

    # --- Step 1: Load watchlist and fetch portfolio ---
    watchlist = load_watchlist()

    api_key = os.getenv("TRADING212_API_KEY")
    api_secret = os.getenv("TRADING212_API_SECRET")

    if api_key and api_secret:
        trading212 = Trading212(api_key, api_secret)
        portfolio_tickers = fetch_portfolio_tickers(trading212)
        watchlist.update(portfolio_tickers)

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
