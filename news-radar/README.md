# News Radar

A local, agent-driven news digest that fetches the latest finance headlines, classifies each one as **good**, **neutral**, or **bad**, and writes a clean summary — built on top of [GAIA](https://github.com/lemonade-sdk/gaia) and running entirely on local models via Lemonade.

News Radar was built as a hands-on exercise in going from "a script that scrapes a headline" to "an agent that decides to fetch its own data," while tracking how often a small local model goes off-script when asked to follow a strict output format.

## How it works

1. **Fetch** — `fetch_headlines()` pulls the latest headlines directly from Yahoo Finance's RSS feed (`https://finance.yahoo.com/news/rssindex`) using `feedparser`. RSS over scraping — it's structured and doesn't break when a page redesigns.
2. **Classify** — `NewsClassifier`, a GAIA `Agent` subclass, runs each headline through a local LLM (`Qwen3.5-35B-A3B-GGUF` via Lemonade) with the instruction to return exactly one word: `good`, `neutral`, or `bad`. `clean_label()` normalizes the raw response and catches anything that doesn't match, tagging it `unknown`.
3. **Agent-driven fetch** — `YahooNewsAgent` registers `fetch_headlines` as a real `@tool`. Instead of `main()` calling it directly, the agent is given a plain-language goal ("fetch the latest finance headlines") and decides on its own to call the tool — the piece that makes this an actual agent rather than a script that happens to use an LLM.
4. **Digest** — headlines are grouped by label and formatted into a summary: counts for all four categories, plus the full list of headlines that landed in **good** and **bad**.
5. **Runs on login** — scheduled via Windows Task Scheduler, so a fresh digest is waiting whenever you log in.

## Project structure

```
news-radar/
├── news_classifier.py   # NewsClassifier (base agent) + clean_label()
├── yahoo_parser.py       # fetch_headlines, YahooNewsAgent, digest building, main()
├── digests/               # timestamped digest output (created automatically)
└── README.md
```

## Setup

**1. Clone and create a virtual environment**

```bash
git clone <this repo>
cd news-radar
python -m venv .venv
```

Activate it:
```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**2. Install dependencies**

```bash
python -m pip install feedparser beautifulsoup4
```

**3. Install GAIA and Lemonade**

News Radar runs classification through [AMD's GAIA](https://github.com/lemonade-sdk/gaia) framework, backed by a local model served through [Lemonade](https://lemonade-server.ai/). Follow GAIA's setup instructions to install it and confirm Lemonade is running.

**4. Pull the model**

```bash
lemonade-server pull Qwen3.5-35B-A3B-GGUF
```

Sizing note: this model is ~20 GB. Make sure you've got comfortable headroom below your available GPU memory (or system RAM if running on CPU) — see Lemonade's own sizing guidance if you'd rather use a smaller model.

## Usage

Run it directly:

```bash
python yahoo_parser.py
```

This will:
- Have the agent fetch the latest ~20 headlines
- Classify each one
- Print and save a digest to `digests/digest_<timestamp>.txt`

## Running automatically at login

Set up via Windows Task Scheduler with a trigger of **"At log on"**, pointing at `yahoo_parser.py` (run through the project's virtual environment's Python interpreter). Each run produces a new timestamped file in `digests/`, so a digest is waiting whenever you log in — no terminal window required.

## Notes

- Classification is single-word sentiment on the headline text alone — it doesn't read the full article, so nuance (e.g., a bearish-sounding phrase inside an otherwise bullish story) can occasionally land on the "wrong" label.
- The `unknown` count tracks how often the model doesn't return a clean one-word answer — a useful signal for how reliably a given model follows the format instruction.
