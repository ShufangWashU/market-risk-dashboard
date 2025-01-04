import feedparser

def fetch_stock_news(stock):
    feed_url = f"https://news.google.com/rss/search?q={stock}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(feed_url)
    return [{"title": entry.title, "link": entry.link} for entry in feed.entries]
