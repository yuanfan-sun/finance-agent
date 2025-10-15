import google.generativeai as genai
from financial_data_service import get_financials
import os
import json
from datetime import datetime

ANALYSIS_DIR = "analysis_reports"

class AnalysisAgent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def analyze_stock(self, ticker):
        """
        Performs a comprehensive analysis of a stock using a generative model and saves it to a JSON file.
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
            analysis_text = response.text

            # 4. Save the analysis to a JSON file
            os.makedirs(ANALYSIS_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = os.path.join(ANALYSIS_DIR, f"{ticker}_{timestamp}")

            # Save as JSON
            json_filename = f"{base_filename}.json"
            report_data = {
                "ticker": ticker,
                "timestamp": timestamp,
                "analysis": analysis_text
            }
            with open(json_filename, 'w') as f:
                json.dump(report_data, f, indent=4)
            print(f"Analysis saved to {json_filename}")

            # Save as Markdown
            md_filename = f"{base_filename}.md"
            with open(md_filename, 'w') as f:
                f.write(analysis_text)
            print(f"Analysis saved to {md_filename}")

            return analysis_text
        except Exception as e:
            return f"Error generating analysis: {e}"
