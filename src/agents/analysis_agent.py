import google.generativeai as genai
from financial_data_service import get_financials

class AnalysisAgent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def analyze_stock(self, ticker):
        """
        Performs a comprehensive analysis of a stock using a generative model.
        """
        print(f"Performing comprehensive analysis for {ticker}...")

        # 1. Get financial data
        financial_data = get_financials(ticker)
        if financial_data is None:
            return f"Could not retrieve financial data for {ticker}. Cannot perform analysis."

        # 2. Construct a detailed prompt
        prompt = f"""
        Please perform a comprehensive investment analysis for the company with the ticker symbol: {ticker}.

        Here is their recent quarterly financial data for context:
        {financial_data.to_string()}

        Based on this data and your general knowledge, please provide the following:

        1.  **Discounted Cash Flow (DCF) Analysis Summary:**
            *   Provide a brief explanation of a DCF analysis for this company.
            *   What are the key assumptions (growth rate, discount rate)?
            *   What is a potential fair value range based on a DCF model?

        2.  **Peer Analysis:**
            *   Identify 2-3 of the company's main competitors.
            *   Provide a brief comparison based on key metrics (e.g., P/E ratio, revenue growth, market cap).

        3.  **Bull vs. Bear Theses:**
            *   **Bull Thesis:** What are 2-3 key reasons to be optimistic about the stock? (e.g., competitive advantages, market growth, new products).
            *   **Bear Thesis:** What are 2-3 key risks or reasons to be pessimistic? (e.g., competition, regulatory hurdles, valuation concerns).

        4.  **Final Recommendation:**
            *   Based on all the above points, provide a summary conclusion. Is this stock a potential Buy, Hold, or Sell for a long-term investor? Justify your reasoning.

        Please structure your response clearly with these four sections.
        """

        # 3. Generate the analysis
        try:
            print("Generating analysis with Gemini...")
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating analysis: {e}"
