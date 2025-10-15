import google.generativeai as genai

class NewsAgent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def summarize_news(self, articles):
        """Summarizes a list of news articles using a generative model."""
        if not articles:
            return "No news to summarize."

        prompt = "Summarize the following news articles in a single paragraph, focusing on the key financial takeaways:\n"
        for article in articles:
            prompt += f"- {article['content']['title']}\n"

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error summarizing news: {e}"