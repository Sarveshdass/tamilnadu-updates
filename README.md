# 🔴 Tamil Nadu Auto Poster
**Fully automated Tamil Nadu news → Instagram + Website**
Posts twice daily, completely free.

---

## 🆓 What You Need (All Free)

| Service | What For | Cost |
|---------|---------|------|
| [GitHub](https://github.com) | Code + Automation + Website | FREE |
| [Groq API](https://console.groq.com) | AI content writing | FREE |
| [imgbb.com](https://api.imgbb.com) | Image hosting for Instagram | FREE |
| [Instagram Graph API](https://developers.facebook.com) | Post to Instagram | FREE |

---

## 📋 STEP-BY-STEP SETUP GUIDE

### STEP 1: Create GitHub Repository

1. Go to [github.com](https://github.com) → Sign up (free)
2. Click **New Repository**
3. Name it: `tamilnadu-updates`
4. Set it as **Public** (required for free GitHub Pages)
5. Upload all the files from this folder to the repo

### STEP 2: Get Groq API Key (Free AI)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with Google/Email (completely free)
3. Click **API Keys** → **Create API Key**
4. Copy the key — looks like: `gsk_xxxxxxxxxxxx`
5. Free limit: **14,400 requests/day** (way more than enough)

### STEP 3: Get imgbb API Key (Free Image Hosting)

1. Go to [api.imgbb.com](https://api.imgbb.com/)
2. Sign up free
3. Click **Get API key**
4. Copy the key — looks like: `abc123def456`

### STEP 4: Set Up Instagram (Most Complex — Read Carefully!)

You need an **Instagram Business Account** connected to a **Facebook Page**.

**4a. Convert Instagram to Business Account:**
1. Open Instagram app → Profile → Menu (☰)
2. Settings → Account → Switch to Professional Account
3. Choose **Business** → Select category → Done

**4b. Create a Facebook Page (if you don't have one):**
1. Go to [facebook.com/pages/create](https://facebook.com/pages/create)
2. Create a page (e.g., "Tamil Nadu Updates")
3. Link your Instagram: Facebook Page → Settings → Instagram → Connect

**4c. Create a Facebook Developer App:**
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Sign up → **Create App**
3. Choose **Business** type → Give it a name
4. Add **Instagram Graph API** product to your app

**4d. Get Your Instagram User ID:**
1. In Meta Developer console → Instagram Basic Display
2. Or use this URL (replace YOUR_TOKEN and YOUR_IG_USERNAME):
   ```
   https://graph.facebook.com/v18.0/me?fields=id,name&access_token=YOUR_TOKEN
   ```
3. The number returned is your **IG_USER_ID**

**4e. Get Long-Lived Access Token:**
1. In Meta Developer Console → Tools → Graph API Explorer
2. Select your app → Generate Access Token
3. Add permissions: `instagram_basic`, `instagram_content_publish`, `pages_show_list`
4. Click **Generate Token** and copy it
5. Exchange for long-lived token (valid 60 days) — run this in browser:
   ```
   https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_TOKEN
   ```
6. Copy the `access_token` from the response

### STEP 5: Add Secrets to GitHub

1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add each one:

| Secret Name | Value |
|-------------|-------|
| `GROQ_API_KEY` | Your Groq key |
| `IG_USER_ID` | Your Instagram Business Account ID |
| `IG_ACCESS_TOKEN` | Your long-lived access token |
| `IMGBB_API_KEY` | Your imgbb API key |

### STEP 6: Enable GitHub Pages (Free Website)

1. Go to your GitHub repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` → Folder: `/website`
4. Click **Save**
5. Your site will be live at: `https://YOUR-USERNAME.github.io/tamilnadu-updates`

### STEP 7: Test It!

1. Go to your repo → **Actions** tab
2. Click **Tamil Nadu Auto Poster**
3. Click **Run workflow** → **Run workflow**
4. Watch the logs — should post to Instagram and update the website!

---

## ⏰ When Does It Post?

The bot automatically posts at:
- **9:00 AM IST** (morning news)
- **6:00 PM IST** (evening update)

To change the time, edit `.github/workflows/daily_post.yml` — the cron schedule.
- IST = UTC + 5:30, so subtract 5h30m from IST to get UTC for cron.

---

## 🔧 Customizing

**Change channel name:** Edit `create_image.py` → change `"TAMIL NADU UPDATES"` and footer text

**Change news sources:** Edit `fetch_news.py` → add/remove RSS feeds from `RSS_FEEDS` list

**Change posting times:** Edit `.github/workflows/daily_post.yml` → modify cron times

**Change design colors:** Edit `create_image.py` → modify the `THEMES` dictionary

---

## 📊 Project Structure

```
tamilnadu-updates/
├── .github/
│   └── workflows/
│       └── daily_post.yml     ← Automation schedule
├── scripts/
│   ├── main.py                ← Main runner
│   ├── fetch_news.py          ← Fetches RSS news
│   ├── generate_post.py       ← AI caption + article writing
│   ├── create_image.py        ← Creates post image
│   ├── post_instagram.py      ← Posts to Instagram
│   └── update_website.py      ← Updates your website
├── website/
│   ├── index.html             ← Auto-generated website
│   └── posts.json             ← Post history
├── posted_titles.json         ← Tracks posted articles
├── requirements.txt
└── README.md
```

---

## ❓ Troubleshooting

**Instagram posting fails?**
- Check that your access token hasn't expired (they last 60 days — refresh it monthly)
- Make sure your Instagram account is set to Business, not Personal
- Verify the Facebook Page is properly linked to Instagram

**No news found?**
- Some RSS feeds may change URLs — check `fetch_news.py` and update them

**GitHub Actions not running?**
- Make sure the repo is not archived
- Check the Actions tab for error logs
- Verify all 4 secrets are correctly added

---

## 🔄 Monthly Maintenance

Instagram access tokens expire every 60 days. Set a calendar reminder to:
1. Generate a new token via Graph API Explorer
2. Update the `IG_ACCESS_TOKEN` secret in GitHub

---

*Built with Python, GitHub Actions, Groq AI, and Instagram Graph API. 100% free.*
