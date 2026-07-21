import feedparser

def fetch_headlines(url="https://finance.yahoo.com/news/rssindex", limit=20):
    feed = feedparser.parse(url)
    return [entry.title for entry in feed.entries[:limit]]

if __name__ == "__main__":
    headlines = fetch_headlines()
    for i, h in enumerate(headlines, 1):
        print(f"{i}. {h}")