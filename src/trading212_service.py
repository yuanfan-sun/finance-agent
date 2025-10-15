import base64
import requests
import os
import json
import time

class Trading212:
    BASE_URL = "https://live.trading212.com/api/v0"
    PORTFOLIO_CACHE_FILE = "portfolio.json"
    INSTRUMENTS_CACHE_FILE = "instruments.json"
    CACHE_EXPIRATION = 3600  # 1 hour in seconds

    def __init__(self, api_key, api_secret):
        self.headers = self._get_auth_headers(api_key, api_secret)
        self.instruments = None
        self.portfolio = None

    def _get_auth_headers(self, key, secret):
        """Constructs the authentication headers for Trading 212 API."""
        credentials = f"{key}:{secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

    def _get_api_data(self, endpoint, cache_file=None):
        """Fetches data from a specified API endpoint, with optional caching."""
        if cache_file and os.path.exists(cache_file):
            file_mod_time = os.path.getmtime(cache_file)
            if (time.time() - file_mod_time) < self.CACHE_EXPIRATION:
                print(f"Loading {endpoint} from cache file: {cache_file}...")
                with open(cache_file, 'r') as f:
                    return json.load(f)

        print(f"Fetching fresh {endpoint} data from API...")
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if cache_file:
                with open(cache_file, 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"Saved fresh {endpoint} data to cache file: {cache_file}")
            return data
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            if err.response.status_code == 401:
                print("Authentication failed. Please check your API Key and Secret.")
                print(f"Response: {err.response.text}")
        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")
        return None

    def get_portfolio_data(self):
        if self.portfolio is None:
            self.portfolio = self._get_api_data("/equity/portfolio", self.PORTFOLIO_CACHE_FILE)
        if self.instruments is None:
            self.instruments = self._get_api_data("/equity/metadata/instruments", self.INSTRUMENTS_CACHE_FILE)

    def get_instruments(self):
        self.get_portfolio_data()
        return self.instruments

    def get_cash(self):
        # Cash balance should generally not be cached
        return self._get_api_data("/equity/account/cash")

    def get_portfolio(self):
        self.get_portfolio_data()
        return self.portfolio

    def get_short_name_by_ticker(self, ticker):
        """Converts a ticker to its shortName."""
        instruments = self.get_instruments()
        if instruments:
            for instrument in instruments:
                if instrument['ticker'] == ticker:
                    return instrument['shortName']
        return None

    def get_portfolio_tickers(self):
        """Fetches portfolio tickers from Trading 212, filtering for stocks only."""
        tickers = set()
        # Ensure portfolio and instrument data are loaded once
        self.get_portfolio_data()

        if not self.portfolio or not self.instruments:
            return tickers

        # Create efficient lookup maps
        instrument_map = {inst['ticker']: {'type': inst['type'], 'shortName': inst.get('shortName')} for inst in self.instruments}

        for position in self.portfolio:
            ticker = position.get('ticker')
            if not ticker:
                continue

            instrument_details = instrument_map.get(ticker)
            if instrument_details and instrument_details.get('type') == 'STOCK':
                # Prefer shortName if available, otherwise use the ticker
                display_name = instrument_details.get('shortName') or ticker
                tickers.add(display_name)
        return tickers

    def get_portfolio_pl(self):
        """Calculates the P/L for each ticker in the portfolio."""
        portfolio_pl = {}
        positions_data = self.get_portfolio()
        if positions_data:
            for position in positions_data:
                ticker = position.get('ticker')
                if ticker:
                    short_name = self.get_short_name_by_ticker(ticker)
                    pl = position.get('ppl', 0)
                    if short_name:
                        portfolio_pl[short_name] = pl
                    else:
                        portfolio_pl[ticker] = pl
        return portfolio_pl

