"""
Fetches Tamil Nadu news from free RSS feeds
No API key needed!
"""

import feedparser
import requests
from datetime import datetime
from html import unescape
import re

# Free RSS feeds covering Tamil Nadu news
RSS_FEEDS = [
    {
        "url": "https://www.thehindu.com/news/national/tamil-nadu/feeder/default.rss",
        "source": "The Hindu - Tamil Nadu",
        "category": "General"
    },
    {
        "url": "https://www.newindianexpress.com/states/tamil-nadu/rssfeed/?id=170&getXmlFeed=true",
        "source": "New Indian Express - TN",
        "category": "General"
    },
    {
        "url": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
        "source": "Times of India - Tamil Nadu",
        "category": "General"
    },
    {
        "url": "https://feeds.feedburner.com/ndtvnews-tamil-nadu",
        "source": "NDTV Tamil Nadu",
        "category": "General"
    },
    {
        "url": "https://www.oneindia.com/rss/news-tamil-nadu-feeds.xml",
        "source": "OneIndia Tamil Nadu",
        "category": "General"
    },
]

def clean_html(text):
    """Remove HTML tags from text"""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def fetch_latest_news(num_articles=10):
    """Fetch latest Tamil Nadu news from all RSS feeds"""
    all_articles = []

    for feed_info in RSS_FEEDS:
        try:
            print(f"  Fetching from {feed_info['source']}...")
            feed = feedparser.parse(feed_info['url'])

            for entry in feed.entries[:5]:
                title = clean_html(entry.get('title', ''))
                summary = clean_html(entry.get('summary', entry.get('description', '')))

                # Skip if no title or too short
                if not title or len(title) < 20:
                    continue

                # Try to get published date
                published = entry.get('published', '')
                try:
                    pub_date = entry.published_parsed
                    published = datetime(*pub_date[:6]).strftime('%Y-%m-%d %H:%M')
                except:
                    published = datetime.now().strftime('%Y-%m-%d %H:%M')

                all_articles.append({
                    'title': title,
                    'summary': summary[:500] if summary else title,
                    'link': entry.get('link', ''),
                    'published': published,
                    'source': feed_info['source'],
                    'category': feed_info['category']
                })

        except Exception as e:
            print(f"  ⚠️ Error fetching {feed_info['source']}: {e}")
            continue

    # Remove duplicates by title similarity
    unique_articles = []
    seen_titles = set()
    for article in all_articles:
        # Simple dedup: skip if first 5 words match
        key = ' '.join(article['title'].split()[:5]).lower()
        if key not in seen_titles:
            seen_titles.add(key)
            unique_articles.append(article)

    print(f"  Found {len(unique_articles)} unique articles")
    return unique_articles[:num_articles]


if __name__ == "__main__":
    articles = fetch_latest_news(5)
    for i, a in enumerate(articles, 1):
        print(f"\n{i}. {a['title']}")
        print(f"   Source: {a['source']} | {a['published']}")
        print(f"   Summary: {a['summary'][:100]}...")
