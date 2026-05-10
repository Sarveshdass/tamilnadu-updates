"""
Updates the GitHub Pages website with new posts
Generates a beautiful static HTML site
"""

import json
import os
import base64
from datetime import datetime
from pathlib import Path


def load_posts():
    """Load existing posts from posts.json"""
    posts_file = "website/posts.json"
    try:
        with open(posts_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def save_posts(posts):
    """Save posts to posts.json"""
    os.makedirs("website", exist_ok=True)
    with open("website/posts.json", 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)


def encode_image_to_base64(image_path):
    """Encode image for embedding in HTML"""
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except:
        return None


def update_website_posts(article, website_post, image_path):
    """Add new post and regenerate the website"""

    # Load existing posts
    posts = load_posts()

    # Encode image
    img_b64 = encode_image_to_base64(image_path)
    img_src = f"data:image/jpeg;base64,{img_b64}" if img_b64 else ""

    # Create new post entry
    new_post = {
        "id": datetime.now().strftime('%Y%m%d%H%M%S'),
        "title": website_post['title'],
        "content": website_post['content'],
        "source": website_post['source'],
        "source_link": website_post['source_link'],
        "category": website_post['category'],
        "published": website_post['published'],
        "generated_at": website_post['generated_at'],
        "image": img_src[:500] + "..." if img_src else ""  # Truncate for JSON
    }

    # Add to front of list, keep last 50 posts
    posts.insert(0, new_post)
    posts = posts[:50]

    # Save JSON
    save_posts(posts)

    # Save image separately
    if img_b64:
        os.makedirs("website/images", exist_ok=True)
        img_filename = f"website/images/{new_post['id']}.jpg"
        with open(img_filename, 'wb') as f:
            f.write(base64.b64decode(img_b64))
        new_post['image_file'] = f"images/{new_post['id']}.jpg"

    # Regenerate full HTML site
    generate_website_html(posts)
    print(f"  Website updated with {len(posts)} posts")


def generate_website_html(posts):
    """Generate the complete website HTML"""

    # Generate post cards
    cards_html = ""
    for i, post in enumerate(posts):
        img_tag = ""
        if post.get('image_file'):
            img_tag = f'<img src="{post["image_file"]}" alt="{post["title"]}" class="post-image">'

        category_color = {
            "General": "#e63946",
            "Politics": "#7209b7",
            "Weather": "#0096c7",
            "Sports": "#2d6a4f",
            "Business": "#e9c46a",
        }.get(post.get('category', 'General'), '#e63946')

        is_featured = "featured" if i == 0 else ""

        cards_html += f"""
        <article class="post-card {is_featured}" onclick="openPost('{post['id']}')">
            {img_tag}
            <div class="post-body">
                <span class="category-tag" style="background:{category_color}">{post.get('category', 'News')}</span>
                <h2 class="post-title">{post['title']}</h2>
                <p class="post-excerpt">{post['content'][:180]}...</p>
                <div class="post-meta">
                    <span class="post-source">📰 {post['source']}</span>
                    <span class="post-date">🕐 {post['published']}</span>
                </div>
            </div>
        </article>"""

    # Generate modal posts data
    posts_json = json.dumps(posts[:50], ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tamil Nadu Updates – Daily News & Updates</title>
<meta name="description" content="Latest news and updates from Tamil Nadu. Auto-updated twice daily.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Tiro+Tamil&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root {{
  --red: #e63946;
  --dark: #0f1923;
  --mid: #1e2d3d;
  --light: #2d3f50;
  --text: #e8edf2;
  --muted: #8899aa;
  --accent: #457b9d;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: var(--dark); color: var(--text); font-family: 'DM Sans', sans-serif; }}

/* HEADER */
header {{
  background: var(--dark);
  border-bottom: 3px solid var(--red);
  padding: 0 24px;
  position: sticky; top: 0; z-index: 100;
}}
.header-inner {{
  max-width: 1200px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between;
  height: 70px;
}}
.logo {{ display: flex; align-items: center; gap: 12px; text-decoration: none; }}
.logo-dot {{ width: 14px; height: 14px; background: var(--red); border-radius: 50%; animation: pulse 1.5s infinite; }}
@keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:.4}} }}
.logo-text {{ font-size: 22px; font-weight: 700; color: var(--text); }}
.logo-sub {{ font-size: 12px; color: var(--muted); letter-spacing: 2px; }}
.ig-link {{
  background: linear-gradient(135deg, #833ab4, #fd1d1d, #fcb045);
  color: white; padding: 8px 18px; border-radius: 6px;
  text-decoration: none; font-size: 14px; font-weight: 600;
}}

/* HERO */
.hero {{
  background: linear-gradient(135deg, var(--mid), var(--dark));
  padding: 60px 24px;
  text-align: center;
  border-bottom: 1px solid var(--light);
}}
.hero h1 {{ font-size: clamp(28px, 5vw, 52px); line-height: 1.2; }}
.hero h1 span {{ color: var(--red); }}
.hero p {{ color: var(--muted); margin-top: 16px; font-size: 18px; }}
.update-badge {{
  display: inline-block; margin-top: 20px;
  background: var(--light); border-radius: 20px;
  padding: 6px 16px; font-size: 13px; color: var(--muted);
}}

/* GRID */
.container {{ max-width: 1200px; margin: 0 auto; padding: 40px 24px; }}
.posts-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}}

/* CARDS */
.post-card {{
  background: var(--mid);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: transform .2s, box-shadow .2s;
  border: 1px solid var(--light);
}}
.post-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 30px rgba(0,0,0,.4); }}
.post-card.featured {{ grid-column: 1 / -1; display: grid; grid-template-columns: 1fr 1fr; }}
.post-image {{ width: 100%; height: 220px; object-fit: cover; }}
.featured .post-image {{ height: 100%; min-height: 300px; }}
.post-body {{ padding: 20px; }}
.category-tag {{
  display: inline-block; padding: 3px 10px; border-radius: 4px;
  font-size: 11px; font-weight: 700; letter-spacing: 1px; margin-bottom: 10px;
}}
.post-title {{ font-size: 18px; font-weight: 700; line-height: 1.4; margin-bottom: 10px; }}
.featured .post-title {{ font-size: 26px; }}
.post-excerpt {{ color: var(--muted); font-size: 14px; line-height: 1.6; margin-bottom: 16px; }}
.post-meta {{ display: flex; gap: 16px; flex-wrap: wrap; }}
.post-source, .post-date {{ font-size: 12px; color: var(--muted); }}

/* MODAL */
.modal-overlay {{
  display: none; position: fixed; inset: 0;
  background: rgba(0,0,0,.85); z-index: 1000;
  overflow-y: auto; padding: 40px 20px;
}}
.modal-overlay.active {{ display: flex; align-items: flex-start; justify-content: center; }}
.modal {{
  background: var(--mid); border-radius: 16px;
  max-width: 760px; width: 100%; padding: 40px;
  position: relative; margin: auto;
}}
.modal-close {{
  position: absolute; top: 20px; right: 20px;
  background: var(--light); border: none; color: var(--text);
  width: 36px; height: 36px; border-radius: 50%; cursor: pointer;
  font-size: 18px;
}}
.modal h2 {{ font-size: 26px; line-height: 1.4; margin-bottom: 20px; }}
.modal p {{ color: var(--muted); line-height: 1.8; font-size: 16px; margin-bottom: 16px; }}
.modal-source {{ font-size: 13px; color: var(--accent); }}
.modal a {{ color: var(--accent); }}

/* FOOTER */
footer {{
  background: var(--mid); border-top: 1px solid var(--light);
  text-align: center; padding: 30px;
  color: var(--muted); font-size: 13px;
}}

@media (max-width: 700px) {{
  .post-card.featured {{ grid-template-columns: 1fr; }}
  .featured .post-image {{ height: 220px; }}
}}
</style>
</head>
<body>

<header>
  <div class="header-inner">
    <a href="/" class="logo">
      <div class="logo-dot"></div>
      <div>
        <div class="logo-text">Tamil Nadu Updates</div>
        <div class="logo-sub">AUTO-UPDATED TWICE DAILY</div>
      </div>
    </a>
    <a href="https://instagram.com/TamilNaduUpdates" class="ig-link" target="_blank">
      📸 Follow on Instagram
    </a>
  </div>
</header>

<div class="hero">
  <h1>Latest News from<br><span>Tamil Nadu</span></h1>
  <p>Auto-curated updates, posted every morning & evening</p>
  <div class="update-badge">🔄 Last updated: {datetime.now().strftime('%d %b %Y, %I:%M %p IST')}</div>
</div>

<div class="container">
  <div class="posts-grid">
    {cards_html}
  </div>
</div>

<div class="modal-overlay" id="modalOverlay" onclick="closeModal(event)">
  <div class="modal" id="modal">
    <button class="modal-close" onclick="closePost()">✕</button>
    <div id="modal-content"></div>
  </div>
</div>

<footer>
  <p>Tamil Nadu Updates • Auto-generated news • Updated twice daily</p>
  <p style="margin-top:8px">Follow us on <a href="https://instagram.com/TamilNaduUpdates" style="color:#fd1d1d">Instagram</a></p>
</footer>

<script>
const posts = {posts_json};

function openPost(id) {{
  const post = posts.find(p => p.id === id);
  if (!post) return;
  const img = post.image_file ? `<img src="${{post.image_file}}" style="width:100%;border-radius:8px;margin-bottom:20px">` : '';
  document.getElementById('modal-content').innerHTML = `
    ${{img}}
    <span class="category-tag" style="background:#e63946;margin-bottom:16px;display:inline-block">${{post.category || 'News'}}</span>
    <h2>${{post.title}}</h2>
    <p style="margin-top:16px">${{post.content.replace(/\\n/g,'<br>')}}</p>
    <p class="modal-source">
      📰 ${{post.source}} | 🕐 ${{post.published}}<br>
      <a href="${{post.source_link}}" target="_blank">Read full story →</a>
    </p>
  `;
  document.getElementById('modalOverlay').classList.add('active');
  document.body.style.overflow = 'hidden';
}}

function closePost() {{
  document.getElementById('modalOverlay').classList.remove('active');
  document.body.style.overflow = '';
}}

function closeModal(e) {{
  if (e.target.id === 'modalOverlay') closePost();
}}

document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closePost(); }});
</script>
</body>
</html>"""

    os.makedirs("website", exist_ok=True)
    with open("website/index.html", 'w', encoding='utf-8') as f:
        f.write(html)
    print("  Website HTML regenerated")
