"""
Generates Instagram captions and website posts
Uses Groq's FREE API (LLaMA 3) — very generous free tier
Sign up at: https://console.groq.com
"""

import os
import requests
from datetime import datetime

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"  # Free model


def call_groq(prompt, max_tokens=600):
    """Make a call to Groq's free LLaMA API"""
    if not GROQ_API_KEY:
        print("⚠️ GROQ_API_KEY not set, using fallback content")
        return None

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7
            },
            timeout=30
        )
        data = response.json()

        if 'choices' in data:
            return data['choices'][0]['message']['content'].strip()
        else:
            print(f"⚠️ Groq API error: {data}")
            return None

    except Exception as e:
        print(f"⚠️ Groq API call failed: {e}")
        return None


def generate_instagram_caption(article):
    """Generate an engaging Instagram caption for Tamil Nadu news"""
    prompt = f"""You are a Tamil Nadu news social media manager. Create an engaging Instagram post.

News Title: {article['title']}
News Summary: {article['summary']}
Source: {article['source']}
Date: {article['published']}

Write an Instagram caption that:
1. Starts with 1-2 relevant emojis and a punchy opening line
2. Explains the news in 3-4 simple sentences (easy to understand)
3. Adds a relatable comment about why this matters to Tamil Nadu people
4. Ends with 12-15 hashtags including #TamilNadu #TamilNaduNews #Chennai #Tamilans #TamilNaduUpdates

Important:
- Write naturally, not like a robot
- Use simple English that everyone understands
- Do NOT add any extra labels or headers, just the post text
- Total length: 150-250 words max
"""

    caption = call_groq(prompt)

    if not caption:
        # Fallback if API fails
        caption = f"""🔴 {article['title']}

{article['summary'][:200]}...

Stay updated with the latest happenings in Tamil Nadu!

#TamilNadu #TamilNaduNews #Chennai #TamilNaduUpdates #TamilNews
#Tamilans #TamilNaduPolitics #TamilNaduGovernment #IndiaNews
#BreakingNews #TamilNaduToday #நியூஸ் #தமிழ்நாடு
"""

    # Always add source credit
    caption += f"\n\n📰 Source: {article['source']}"

    return caption


def generate_website_post(article):
    """Generate a full article for the website"""
    prompt = f"""You are a Tamil Nadu news writer. Write a clear, informative news article.

News Title: {article['title']}
News Summary: {article['summary']}
Source: {article['source']}

Write a news article with:
1. A strong opening paragraph (2-3 sentences) explaining what happened
2. A "Details" paragraph with more context (3-4 sentences)
3. A "What it means" paragraph explaining the impact on Tamil Nadu people (2-3 sentences)
4. A brief closing line

Format as plain paragraphs only. No headers, no bullet points. Total: 150-200 words.
"""

    content = call_groq(prompt, max_tokens=400)

    if not content:
        content = f"""{article['summary']}

This is an important development for Tamil Nadu. Readers are encouraged to follow the source link for the complete story.

Stay tuned to Tamil Nadu Updates for more news from across the state."""

    return {
        'title': article['title'],
        'content': content,
        'source': article['source'],
        'source_link': article['link'],
        'category': article['category'],
        'published': article['published'],
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


if __name__ == "__main__":
    # Test with a sample article
    test_article = {
        'title': 'Chennai receives heavy rains as northeast monsoon strengthens',
        'summary': 'Heavy rainfall lashed Chennai and surrounding districts as the northeast monsoon intensified over Tamil Nadu. The India Meteorological Department has issued an orange alert for several districts.',
        'source': 'The Hindu - Tamil Nadu',
        'published': '2024-11-10 09:00',
        'category': 'Weather',
        'link': 'https://example.com'
    }

    print("Testing caption generation...")
    caption = generate_instagram_caption(test_article)
    print("\n--- INSTAGRAM CAPTION ---")
    print(caption)

    print("\n\nTesting website post generation...")
    post = generate_website_post(test_article)
    print("\n--- WEBSITE CONTENT ---")
    print(post['content'])
