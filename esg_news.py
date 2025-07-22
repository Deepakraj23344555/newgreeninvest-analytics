# esg_news.py

import feedparser

def get_esg_news():
    rss_url = "https://news.google.com/rss/search?q=ESG+Investing&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    
    articles = []
    for entry in feed.entries[:5]:  # Show top 5 news articles
        article = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        }
        articles.append(article)
    return articles
