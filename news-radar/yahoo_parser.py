import sys
sys.dont_write_bytecode = True
import feedparser
from collections import Counter
from news_classifier import clean_label, NewsClassifier
from gaia.agents.base.tools import tool

def fetch_headlines(url="https://finance.yahoo.com/news/rssindex", limit=5):
    feed = feedparser.parse(url)
    return [entry.title for entry in feed.entries[:limit]]

def extract_tool_headlines(process_query_result, tool_name="fetch_headlines_tool"):
    for message in process_query_result.get("conversation", []):
        if message.get("role") == "tool" and message.get("name") == tool_name:
            return message["content"]
    return []

class YahooNewsAgent(NewsClassifier):
    def _register_tools(self):
        super()._register_tools()
        self._register_yahoo_tools()

    def _register_yahoo_tools(self):
        @tool
        def fetch_headlines_tool(limit: int = 5) -> list:
            """Fetch the latest finance headlines from Yahoo Finance RSS.

            Args:
                limit: Maximum number of headlines to return (default 5)
            """
            return fetch_headlines(limit=limit)

    def classify_headlines(self, headlines):
        results = []
        for headline in headlines:
            raw = self.process_query(f"Classify this headline as good, neutral, or bad: {headline}")
            raw = raw.get("result", raw) if isinstance(raw, dict) else raw
            label = clean_label(raw)
            results.append((headline, label))
        return results

if __name__ == "__main__":
    agent = YahooNewsAgent()

    fetch_result = agent.process_query("Fetch the latest finance headlines from Yahoo Finance RSS.")
    headlines = extract_tool_headlines(fetch_result)

    results = agent.classify_headlines(headlines)

    for headline, label in results:
        print(f"{headline}: {label}")

    counts = Counter(label for _, label in results)
    print(f"\nUnknown: {counts['unknown']} out of {len(results)}")