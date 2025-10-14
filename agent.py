
import json
import yfinance as yf

def load_portfolio(filename="portfolio.json"):
    """Loads the portfolio from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None

def get_stock_data(symbol):
    """Retrieves stock data for a given symbol using yfinance."""
    try:
        stock = yf.Ticker(symbol)
        return stock.info
    except Exception as e:
        print(f"Could not retrieve data for {symbol}: {e}")
        return None

def main():
    """Main function to monitor the portfolio."""
    portfolio = load_portfolio()
    if not portfolio:
        return

    total_portfolio_value = 0
    print("--- Portfolio Status ---")

    for stock_holding in portfolio.get("stocks", []):
        symbol = stock_holding.get("symbol")
        shares = stock_holding.get("shares")
        
        if not symbol or not shares:
            continue

        stock_data = get_stock_data(symbol)
        
        if stock_data:
            current_price = stock_data.get("currentPrice")
            if current_price:
                holding_value = current_price * shares
                total_portfolio_value += holding_value
                print(f"{symbol}: {shares} shares @ ${current_price:.2f} = ${holding_value:.2f}")
            else:
                print(f"{symbol}: Could not retrieve current price.")
        else:
            print(f"{symbol}: Could not retrieve stock data.")

    print("------------------------")
    print(f"Total Portfolio Value: ${total_portfolio_value:.2f}")
    print("------------------------")

if __name__ == "__main__":
    main()
