"""
Main orchestration script for Tamil Nadu Auto Poster
Runs twice daily via GitHub Actions
"""

import os
import json
from datetime import datetime
from fetch_news import fetch_latest_news
from generate_post import generate_instagram_caption, generate_website_post
from create_image import create_post_image
from post_instagram import post_to_instagram
from update_website import update_website_posts

def run_daily_post():
    print(f"\n{'='*50}")
    print(f"Tamil Nadu Auto Poster - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")

    # Step 1: Fetch latest Tamil Nadu news
    print("📰 Fetching latest Tamil Nadu news...")
    articles = fetch_latest_news(num_articles=10)
    if not articles:
        print("❌ No articles found. Exiting.")
        return

    # Pick the best article (first unposted one)
    posted_titles = load_posted_titles()
    article = None
    for a in articles:
        if a['title'] not in posted_titles:
            article = a
            break

    if not article:
        print("⚠️ All articles already posted. Using latest.")
        article = articles[0]

    print(f"✅ Selected: {article['title'][:60]}...")

    # Step 2: Generate Instagram caption
    print("\n✍️ Generating Instagram caption...")
    caption = generate_instagram_caption(article)
    print(f"✅ Caption generated ({len(caption)} chars)")

    # Step 3: Generate website post content
    print("\n🌐 Generating website post...")
    website_post = generate_website_post(article)

    # Step 4: Create image
    print("\n🎨 Creating post image...")
    image_path = create_post_image(
        title=article['title'],
        source=article['source'],
        category=article.get('category', 'News'),
        output_path="/tmp/post_image.jpg"
    )
    print(f"✅ Image created: {image_path}")

    # Step 5: Post to Instagram
    print("\n📸 Posting to Instagram...")
    ig_success = post_to_instagram(image_path, caption)
    if ig_success:
        print("✅ Posted to Instagram!")
    else:
        print("⚠️ Instagram post failed (check tokens)")

    # Step 6: Update website
    print("\n🌐 Updating website...")
    update_website_posts(article, website_post, image_path)
    print("✅ Website updated!")

    # Save posted title
    save_posted_title(article['title'])

    print(f"\n{'='*50}")
    print("✅ Done! Post complete.")
    print(f"{'='*50}\n")


def load_posted_titles():
    try:
        with open("posted_titles.json", "r") as f:
            return json.load(f)
    except:
        return []


def save_posted_title(title):
    titles = load_posted_titles()
    titles.insert(0, title)
    titles = titles[:100]  # Keep last 100
    with open("posted_titles.json", "w") as f:
        json.dump(titles, f)


if __name__ == "__main__":
    run_daily_post()
