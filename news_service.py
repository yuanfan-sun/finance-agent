import yfinance as yf

class NewsService:
    def get_news(self, ticker):
        """Fetches recent news for a given stock ticker using yfinance."""
        try:
            cleaned_ticker = ticker.split('_')[0]
            if len(cleaned_ticker) == 4 and cleaned_ticker.endswith('1'):
                cleaned_ticker = cleaned_ticker[:-1]
            
            stock = yf.Ticker(cleaned_ticker)
            return stock.news if stock.news else []
        except Exception:
            return []
