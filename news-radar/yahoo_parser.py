import sys
sys.dont_write_bytecode = True
import feedparser
from collections import Counter
from news_classifier import clean_label, NewsClassifier
from gaia.agents.base.tools import tool
from datetime import datetime

def fetch_headlines(url="https://finance.yahoo.com/news/rssindex", limit=20):
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
        def fetch_headlines_tool(limit: int = 20) -> list:
            """Fetch the latest finance headlines from Yahoo Finance RSS.

            Args:
                limit: Maximum number of headlines to return (default 20)
            """
            return fetch_headlines(limit=limit)

    def classify_headlines(self, headlines):
        results = []
        for headline in headlines:
            # Prefer the internal `_process_query` if available so the model
            # doesn't try to call registered tools (like fetch_headlines_tool)
            direct = getattr(self, "_process_query", None)
            if callable(direct):
                raw = direct(f"Classify this headline as good, neutral, or bad: {headline}")
            else:
                raw = self.process_query(f"Classify this headline as good, neutral, or bad: {headline}")

            raw = raw.get("result", raw) if isinstance(raw, dict) else raw
            label = clean_label(raw)
            results.append((headline, label))
        return results

    def group_by_label(self, results):
        grouped = {"good": [], "neutral": [], "bad": [], "unknown": []}
        for headline, label in results:
            grouped[label].append(headline)
        return grouped

    def build_digest(self, grouped):
        lines = []
        lines.append("=== News Digest ===")
        lines.append(f"Good: {len(grouped['good'])}")
        lines.append(f"Neutral: {len(grouped['neutral'])}")
        lines.append(f"Bad: {len(grouped['bad'])}")
        lines.append(f"Unknown: {len(grouped['unknown'])}")
        lines.append("")

        lines.append("--- Good headlines ---")
        for headline in grouped["good"]:
            lines.append(f"  + {headline}")

        lines.append("")
        lines.append("--- Bad headlines ---")
        for headline in grouped["bad"]:
            lines.append(f"  - {headline}")

        return "\n".join(lines)

    def _get_timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def save_digest(self, digest, folder="digests"):
        import os
        os.makedirs(folder, exist_ok=True)
        timestamp = self._get_timestamp()
        filepath = os.path.join(folder, f"digest_{timestamp}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(digest)
        return filepath

if __name__ == "__main__":
    agent = YahooNewsAgent(model_id="Qwen3.5-35B-A3B-GGUF", silent_mode=True)

    fetch_result = agent.process_query("Fetch the latest finance headlines from Yahoo Finance RSS.")
    headlines = extract_tool_headlines(fetch_result)

    # If the tool extraction returned no headlines, loudly warn and fall back
    # to a direct fetch to avoid producing an empty/"no news" digest.
    if not headlines:
        print("WARNING: No headlines returned from tool extraction. Falling back to direct fetch_headlines().")
        try:
            headlines = fetch_headlines(limit=20)
        except Exception as e:
            print(f"ERROR: Direct fetch_headlines() failed: {e}")

    results = agent.classify_headlines(headlines)

    grouped = agent.group_by_label(results)
    digest = agent.build_digest(grouped)

    filepath = agent.save_digest(digest)
    print(f"Digest saved to {filepath}")