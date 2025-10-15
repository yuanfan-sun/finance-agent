import base64
import requests

class Trading212:
    BASE_URL = "https://live.trading212.com/api/v0"

    def __init__(self, api_key, api_secret):
        self.headers = self._get_auth_headers(api_key, api_secret)

    def _get_auth_headers(self, key, secret):
        """Constructs the authentication headers for Trading 212 API."""
        credentials = f"{key}:{secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

    def _get_api_data(self, endpoint):
        """Fetches data from a specified API endpoint."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            if err.response.status_code == 401:
                print("Authentication failed. Please check your API Key and Secret.")
        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")
        return None
    
    def get_instruments(self):
        return self._get_api_data("/equity/metadata/instruments")

    def get_cash(self):
        return self._get_api_data("/equity/account/cash")

    def get_portfolio(self):
        return self._get_api_data("/equity/portfolio")
