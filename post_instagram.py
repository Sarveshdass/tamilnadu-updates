"""
Posts to Instagram using the free Instagram Graph API
Setup guide in README.md

Required environment variables:
- IG_USER_ID: Your Instagram Business Account ID
- IG_ACCESS_TOKEN: Long-lived Page Access Token
- IMGBB_API_KEY: Free image hosting (sign up at imgbb.com)
"""

import os
import requests
import base64
import time

IG_USER_ID = os.environ.get('IG_USER_ID')
IG_ACCESS_TOKEN = os.environ.get('IG_ACCESS_TOKEN')
IMGBB_API_KEY = os.environ.get('IMGBB_API_KEY')
GRAPH_API_VERSION = "v18.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


def upload_image_to_imgbb(image_path):
    """
    Upload image to imgbb.com (FREE image hosting)
    Returns public URL of the image
    Sign up at: https://api.imgbb.com/
    """
    if not IMGBB_API_KEY:
        print("  ⚠️ IMGBB_API_KEY not set")
        return None

    try:
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={
                "key": IMGBB_API_KEY,
                "image": image_data,
                "expiration": 86400  # Keep for 24 hours
            },
            timeout=30
        )

        data = response.json()
        if data.get('success'):
            url = data['data']['url']
            print(f"  Image uploaded to imgbb: {url[:50]}...")
            return url
        else:
            print(f"  ⚠️ imgbb upload failed: {data}")
            return None

    except Exception as e:
        print(f"  ⚠️ Image upload error: {e}")
        return None


def create_instagram_media_container(image_url, caption):
    """Step 1: Create a media container in Instagram"""
    try:
        response = requests.post(
            f"{GRAPH_API_BASE}/{IG_USER_ID}/media",
            data={
                "image_url": image_url,
                "caption": caption,
                "access_token": IG_ACCESS_TOKEN
            },
            timeout=30
        )

        data = response.json()
        if 'id' in data:
            print(f"  Media container created: {data['id']}")
            return data['id']
        else:
            print(f"  ⚠️ Container creation failed: {data}")
            return None

    except Exception as e:
        print(f"  ⚠️ Container creation error: {e}")
        return None


def publish_instagram_media(creation_id):
    """Step 2: Publish the media container"""
    try:
        # Wait a moment for Instagram to process
        time.sleep(3)

        response = requests.post(
            f"{GRAPH_API_BASE}/{IG_USER_ID}/media_publish",
            data={
                "creation_id": creation_id,
                "access_token": IG_ACCESS_TOKEN
            },
            timeout=30
        )

        data = response.json()
        if 'id' in data:
            print(f"  ✅ Published! Post ID: {data['id']}")
            return data['id']
        else:
            print(f"  ⚠️ Publish failed: {data}")
            return None

    except Exception as e:
        print(f"  ⚠️ Publish error: {e}")
        return None


def post_to_instagram(image_path, caption):
    """Main function: Upload image and post to Instagram"""
    if not all([IG_USER_ID, IG_ACCESS_TOKEN, IMGBB_API_KEY]):
        missing = [k for k, v in {
            'IG_USER_ID': IG_USER_ID,
            'IG_ACCESS_TOKEN': IG_ACCESS_TOKEN,
            'IMGBB_API_KEY': IMGBB_API_KEY
        }.items() if not v]
        print(f"  ⚠️ Missing credentials: {', '.join(missing)}")
        print("  ℹ️ See README for Instagram setup instructions")
        return False

    # Step 1: Upload image to public URL
    print("  Uploading image...")
    image_url = upload_image_to_imgbb(image_path)
    if not image_url:
        return False

    # Step 2: Create media container
    print("  Creating Instagram media container...")
    creation_id = create_instagram_media_container(image_url, caption)
    if not creation_id:
        return False

    # Step 3: Publish
    print("  Publishing to Instagram...")
    post_id = publish_instagram_media(creation_id)
    return post_id is not None


def check_instagram_account():
    """Verify your Instagram credentials are working"""
    if not all([IG_USER_ID, IG_ACCESS_TOKEN]):
        print("❌ IG_USER_ID and IG_ACCESS_TOKEN must be set")
        return False

    try:
        response = requests.get(
            f"{GRAPH_API_BASE}/{IG_USER_ID}",
            params={
                "fields": "username,name,followers_count",
                "access_token": IG_ACCESS_TOKEN
            }
        )
        data = response.json()
        if 'username' in data:
            print(f"✅ Connected to Instagram: @{data['username']}")
            print(f"   Followers: {data.get('followers_count', 'N/A')}")
            return True
        else:
            print(f"❌ Instagram check failed: {data}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("Checking Instagram connection...")
    check_instagram_account()
