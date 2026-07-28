## This is the same as finance_agent.py but is being used for this project specifically
import sys
sys.dont_write_bytecode = True
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from gaia.agents.base.agent import Agent

class NewsClassifier(Agent):
    def __init__(self, **kwargs):
        kwargs.setdefault("model_id", "Qwen3.5-35B-A3B-GGUF")
        super().__init__(**kwargs)

    def _get_system_prompt(self):
        return "Classify finance headlines as good, neutral, or bad. Return exactly one word."

    def _register_tools(self):
        pass

def clean_label(text):
    text = str(text).strip().lower()
    if "good" in text:
        return "good"
    if "neutral" in text:
        return "neutral"
    if "bad" in text:
        return "bad"
    return "unknown"

def get_headline(url):
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=15) as response:
        html = response.read().decode("utf-8", errors="ignore")

    soup = BeautifulSoup(html, "html.parser")

    for tag in ["h1", "title"]:
        el = soup.find(tag)
        if el and el.get_text(strip=True):
            return el.get_text(strip=True)

    return None

def main():
    url = input("Enter URL: ").strip()
    headline = get_headline(url)

    if not headline:
        print("Could not find a headline.")
        return

    agent = NewsClassifier()
    result = agent.process_query(f"Classify this headline as good, neutral, or bad: {headline}")
    raw = result.get("result", result) if isinstance(result, dict) else result
    answer = clean_label(raw)

    print(f"Headline: {headline}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()