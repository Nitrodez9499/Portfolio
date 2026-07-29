from turtle import pd
from urllib.request import Request, urlopen
from zipfile import Path
from bs4 import BeautifulSoup
from gaia.agents.base.agent import Agent

class FinanceAgent(Agent):
    def __init__(self, **kwargs):
        kwargs.setdefault("model_id", "Qwen3.5-35B-A3B-GGUF")
        super().__init__(**kwargs)

    def _get_system_prompt(self):
        return "Classify finance headlines as good, neutral, or bad. Return exactly one word."

    def _register_tools(self):
        @self.register_tool("process_query")
        
        def process_query(query):
            return self._process_query(query)

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
    path = input("Enter text file path: ").strip()
    sample_size = int(input("How many headlines do you want to sample? ").strip())

    with open(path, "r", encoding="latin-1") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise ValueError("No usable lines found.")

    sample_size = min(sample_size, len(lines))
    sample = random.sample(lines, sample_size)

    agent = FinanceAgent()
    results = []

    for i, headline in enumerate(sample, start=1):
        result = agent.process_query(f"Classify this headline as good, neutral, or bad: {headline}")
        raw = result.get("result", result) if isinstance(result, dict) else result
        answer = clean_label(raw)

        print(f"\n[{i}] Selected headline: {headline}")
        print(f"    Agent answer: {answer}")

        results.append({"headline": headline, "answer": answer})

    out_path = Path.home() / "Desktop" / "headline_answers.csv"
    out_path = Path("output") / "headline_answers.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(results).to_csv(out_path, index=False)
    pd.DataFrame(results).to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")

if __name__ == "__main__":
    main()