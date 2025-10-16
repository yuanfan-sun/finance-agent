import yfinance as yf
import requests
import os
import json
import time
from datetime import datetime, timedelta

NEWS_CACHE_DIR = "news_cache"
CACHE_EXPIRATION = 3600  # 1 hour in seconds

class NewsService:
    def __init__(self):
        self.newsapi_key = os.getenv("NEWSAPI_KEY")
        self.alphavantage_key = os.getenv("ALPHAVANTAGE_API_KEY")
        os.makedirs(NEWS_CACHE_DIR, exist_ok=True)

    def get_news(self, ticker, source='yfinance', days=None):
        """Fetches news for a ticker, allowing for a lookback in days or a default of 5 articles in 30 days."""
        days_str = f"{days}d" if days else "default"
        cache_filename = f"{ticker}_{source}_{days_str}.json"
        cache_filepath = os.path.join(NEWS_CACHE_DIR, cache_filename)

        if os.path.exists(cache_filepath):
            file_mod_time = os.path.getmtime(cache_filepath)
            if (time.time() - file_mod_time) < CACHE_EXPIRATION:
                print(f"Loading news for {ticker} from cache...")
                with open(cache_filepath, 'r') as f:
                    return json.load(f)

        print(f"Fetching fresh news for {ticker} from {source}...")
        if source == 'newsapi':
            news = self._get_news_newsapi(ticker, days)
        elif source == 'alphavantage':
            news = self._get_news_alphavantage(ticker, days)
        else: # Default to yfinance
            news = self._get_news_yfinance(ticker, days)

        if news:
            with open(cache_filepath, 'w') as f:
                json.dump(news, f, indent=4)
            print(f"Saved fresh news for {ticker} to cache.")

        return news

    def _get_news_yfinance(self, ticker, days):
        try:
            stock = yf.Ticker(ticker)
            news = stock.news if stock.news else []
            
            # yfinance doesn't support date filtering in the API call, so we filter afterwards
            from_timestamp = (datetime.now() - timedelta(days=days)).timestamp() if days else (datetime.now() - timedelta(days=30)).timestamp()

            filtered_news = []
            for article in news:
                pub_time = article.get('provider_publish_time')
                if not pub_time or pub_time < from_timestamp:
                    continue
                filtered_news.append(article)
            
            # Apply default limit if no days are specified
            if not days:
                filtered_news = filtered_news[:5]

            # yfinance provides a summary, not the full article content. This is standard for news APIs.
            return [{"title": article['title'], "content": article.get('summary', article['title'])} for article in filtered_news]
        except Exception as e:
            print(f"Error fetching news from yfinance: {e}")
            return []

    def _get_news_newsapi(self, ticker, days):
        if not self.newsapi_key:
            print("NEWSAPI_KEY not found.")
            return []
        
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d') if days else (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        page_size = 100 if days else 5 # Fetch more if a specific date range is given, else just 5

        url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={self.newsapi_key}&language=en&sortBy=publishedAt&from={from_date}&pageSize={page_size}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            # NewsAPI provides a description/snippet, not the full article content.
            return [{"title": article['title'], "content": article.get('description', '') or article['title']} for article in articles]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news from NewsAPI: {e}")
            return []

    def _get_news_alphavantage(self, ticker, days):
        if not self.alphavantage_key:
            print("ALPHAVANTAGE_API_KEY not found.")
            return []

        limit = 500 if days else 5
        url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={self.alphavantage_key}&limit={limit}"
        
        if days:
            from_date = (datetime.now() - timedelta(days=days))
            time_from = from_date.strftime('%Y%m%dT%H%M')
            url += f"&time_from={time_from}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            articles = data.get('feed', [])
            # Alpha Vantage provides a summary, not the full article content.
            return [{"title": article['title'], "content": article.get('summary', '') or article['title']} for article in articles]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news from Alpha Vantage: {e}")
            return []
