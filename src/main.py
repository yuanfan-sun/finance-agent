import os
import argparse
from dotenv import load_dotenv
from trading212_service import Trading212
from news_service import NewsService
from agents.news_agent import NewsAgent
import financial_data_service as fds

def main():
    """Main function to run financial agent commands."""
    load_dotenv()

    parser = argparse.ArgumentParser(description="Finance Agent CLI")
    subparsers = parser.add_subparsers(dest='command')

    # News command
    subparsers.add_parser('news', help='Get news summaries for the portfolio.')

    # Earnings calendar command
    subparsers.add_parser('earnings_calendar', help='Get the earnings calendar for the portfolio.')

    # Financials command
    parser_financials = subparsers.add_parser('financials', help='Get historical financials for a stock.')
    parser_financials.add_argument('symbol', type=str, help='Stock symbol to get financials for.')

    args = parser.parse_args()

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    trading212_api_key = os.getenv("TRADING212_API_KEY")
    trading212_api_secret = os.getenv("TRADING212_API_SECRET")

    portfolio_tickers = []
    if args.command in ['news', 'earnings_calendar']:
        if trading212_api_key and trading212_api_secret:
            trading212 = Trading212(trading212_api_key, trading212_api_secret)
            trading212.get_portfolio_data()
            portfolio_tickers = trading212.get_portfolio_tickers()

        else:
            print("Trading212 API credentials not found. Please set TRADING212_API_KEY and TRADING212_API_SECRET.")
            return

    if args.command == 'news':
        news_service = NewsService()
        news_agent = NewsAgent(gemini_api_key)
        for ticker in portfolio_tickers:
            news = news_service.get_news(ticker)
            summary = news_agent.summarize_news(news)
            print(f"\nNews for {ticker}:")
            print(summary)

    elif args.command == 'earnings_calendar':
        earnings = fds.get_earnings_calendar(list(portfolio_tickers))
        print("Upcoming Earnings Dates:")
        for ticker, date in earnings.items():
            # Format date safely, checking if it's not NaT (Not a Time)
            if date and not pd.isna(date):
                print(f"{ticker}: {date.strftime('%Y-%m-%d')}")
            else:
                print(f"{ticker}: N/A")

    elif args.command == 'financials':
        financials = fds.get_financials(args.symbol)
        if financials is not None:
            print(f"Financials for {args.symbol}:")
            print(financials)
        else:
            print(f"Could not retrieve financials for {args.symbol}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
