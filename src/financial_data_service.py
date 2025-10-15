import yfinance as yf
import pandas as pd


def get_earnings_calendar(tickers):
    """
    Gets the next earnings date for a list of stock tickers.

    Args:
        tickers (list): A list of stock ticker symbols.

    Returns:
        dict: A dictionary mapping tickers to their next earnings date.
    """
    earnings_dates = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        try:
            calendar = stock.calendar
            # yfinance can return a dict. Check for that and extract the date.
            if isinstance(calendar, dict) and calendar.get('Earnings') and calendar['Earnings'].get('Earnings Date'):
                earnings_dates[ticker] = pd.to_datetime(calendar['Earnings']['Earnings Date'][0])
            # The expected response is a DataFrame.
            elif isinstance(calendar, pd.DataFrame) and not calendar.empty:
                earnings_dates[ticker] = calendar.iloc[0, 0]
        except Exception as e:
            print(f"Could not retrieve earnings date for {ticker}: {e}")
    return earnings_dates

def get_financials(ticker):
    """
    Gets historical financial data (income statement) for a given ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the annual income statement.
    """
    stock = yf.Ticker(ticker)
    try:
        income_statement = stock.financials
        if income_statement is not None and not income_statement.empty:
            return income_statement.loc[['Total Revenue', 'EBITDA']]
        else:
            return None
    except Exception as e:
        print(f"Could not retrieve financials for {ticker}: {e}")
        return None
