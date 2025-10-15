import os
from dotenv import load_dotenv
from trading212_service import Trading212
from news_service import NewsService
from llm_agent import LLMAgent

def main():
    """Main function to monitor the portfolio and fetch news."""
    load_dotenv()

    api_key = os.getenv("TRADING212_API_KEY")
    api_secret = os.getenv("TRADING212_API_SECRET")

    if not api_key or not api_secret:
        print("Error: TRADING212_API_KEY or TRADING212_API_SECRET not found in .env file.")
        return

    trading212 = Trading212(api_key, api_secret)
    news_service = NewsService()

    # --- Step 1: Fetch all instrument metadata and create a name map ---
    print("--- Fetching instrument metadata from Trading 212 ---")
    instruments_data = trading212.get_instruments()
    instrument_name_map = {}
    if instruments_data:
        for instrument in instruments_data:
            if 'ticker' in instrument and 'shortName' in instrument:
                instrument_name_map[instrument['ticker']] = instrument['shortName']
    print(f"Loaded metadata for {len(instrument_name_map)} instruments.")

    # --- Step 2: Fetch portfolio status ---
    print("\n--- Trading 212 Portfolio Status ---")
    cash_data = trading212.get_cash()
    if cash_data:
        print(f"Free Cash: {cash_data.get('free')} {cash_data.get('currency')}")

    positions_data = trading212.get_portfolio()
    if positions_data:
        total_portfolio_value = 0
        print("\n--- Open Positions ---")
        for position in positions_data:
            ticker = position.get('ticker')
            quantity = position.get('quantity')
            current_price = position.get('currentPrice')
            ppl = position.get('ppl')

            # Use the map to get the display name
            display_name = instrument_name_map.get(ticker, ticker)

            if current_price is not None and ppl is not None:
                holding_value = quantity * current_price
                total_portfolio_value += holding_value
                print(f"{display_name} ({ticker}):")
                print(f"  {quantity} shares @ ${current_price:.2f} = ${holding_value:.2f} (P/L: {ppl:.2f})")
            else:
                print(f"{display_name} ({ticker}): {quantity} shares (Price data not available)")
        
        print("------------------------------------")
        print(f"Total Portfolio Value (Stocks): ${total_portfolio_value:.2f}")
        
        if cash_data and cash_data.get('free'):
            total_account_value = total_portfolio_value + cash_data.get('free')
            print(f"Total Account Value (Stocks + Cash): ${total_account_value:.2f}")
        
        print("------------------------------------")

        # --- Step 3: Fetch, display, and summarize news ---
        print("\n--- Recent News Summary ---")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            print("GEMINI_API_KEY not found in .env file. Skipping news summarization.")
        else:
            llm_agent = LLMAgent(gemini_api_key)
            for position in positions_data:
                ticker = position.get('ticker')
                if ticker:
                    display_name = instrument_name_map.get(ticker, ticker)
                    print(f"\n--- News Summary for {display_name} ({ticker}) ---")
                    
                    news_articles = news_service.get_news(ticker)
                    summary = llm_agent.summarize_news(news_articles)
                    print(summary)

if __name__ == "__main__":
    main()
