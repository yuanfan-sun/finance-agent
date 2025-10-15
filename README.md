# Finance Agent CLI

## Project Overview

The Finance Agent CLI is a Python-based command-line interface tool designed to assist investors with portfolio monitoring and stock analysis. It integrates with the Trading 212 API to fetch portfolio data, leverages `yfinance` for financial market data, and utilizes the Gemini API for AI-powered news summarization and comprehensive stock analysis.

## Features

*   **Portfolio News Summaries**: Get AI-generated summaries of recent news for stocks in your Trading 212 portfolio.
*   **Earnings Calendar**: View upcoming earnings dates for your portfolio holdings.
*   **Historical Financials**: Retrieve detailed quarterly financial statements (Income Statement) for any given stock ticker.
*   **Comprehensive Stock Analysis**: Perform an AI-powered analysis of a stock, including:
    *   Discounted Cash Flow (DCF) analysis summary.
    *   Peer comparison.
    *   Bull vs. Bear theses.
    *   Final investment recommendation.
*   **API Caching**: Efficiently caches Trading 212 API responses to prevent rate-limiting issues.
*   **Analysis Report Storage**: Automatically saves detailed stock analysis reports in both JSON and Markdown formats for easy review and persistence.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/finance-agent.git
    cd finance-agent
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

This project requires API keys for Trading 212 and Gemini. Create a `.env` file in the project root directory with the following content:

```dotenv
TRADING212_API_KEY="your_trading212_api_key"
TRADING212_API_SECRET="your_trading212_api_secret"
GEMINI_API_KEY="your_gemini_api_key"
```

*   **TRADING212_API_KEY/SECRET**: Obtain these from your Trading 212 account settings.
*   **GEMINI_API_KEY**: Obtain this from the Google AI Studio or Google Cloud Console.

## Usage

All commands are run via `python src/main.py <command> [arguments]`.

### 1. Get News Summaries for Your Portfolio

Fetches recent news for all stock instruments in your Trading 212 portfolio and provides AI-generated summaries.

```bash
python src/main.py news
```

### 2. Get Upcoming Earnings Dates for Your Portfolio

Displays the next reported earnings date for each stock in your Trading 212 portfolio.

```bash
python src/main.py earnings_calendar
```

### 3. Get Historical Financials for a Stock

Retrieves and displays the full quarterly income statement for a specified stock ticker.

```bash
python src/main.py financials AAPL
```

### 4. Perform Comprehensive Stock Analysis

Generates a detailed investment analysis for a given stock ticker, including DCF summary, peer analysis, bull/bear theses, and a recommendation. The analysis is also saved to the `analysis_reports/` directory.

```bash
python src/main.py analyze MSFT
```

## Analysis Reports

When you run the `analyze` command, the generated reports are saved in the `analysis_reports/` directory at the project root. Each analysis is saved as two files:

*   `.json`: For structured data storage.
*   `.md`: For human-readable, formatted content (viewable in any Markdown editor).

Example filename format: `analysis_reports/AAPL_20251015_195438.json` and `analysis_reports/AAPL_20251015_195438.md`.

## Caching

To comply with API rate limits, responses from the Trading 212 API (portfolio and instrument data) are cached locally in `portfolio.json` and `instruments.json` files. These caches expire after 1 hour. Subsequent calls within this period will load data from the cache instead of making new API requests.

**Note:** The cache files (`*.json`) are automatically added to `.gitignore` and should not be committed to version control.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details (if applicable).
