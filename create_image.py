"""
Creates visually appealing post images for Tamil Nadu news
Uses Python Pillow — no paid tools needed!
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from datetime import datetime


# Color themes for different categories
THEMES = {
    "General": {"bg": "#0f1923", "header": "#e63946", "accent": "#457b9d"},
    "Politics": {"bg": "#1a0a2e", "header": "#7209b7", "accent": "#f72585"},
    "Weather": {"bg": "#023e8a", "header": "#0096c7", "accent": "#90e0ef"},
    "Sports":  {"bg": "#1b4332", "header": "#2d6a4f", "accent": "#74c69d"},
    "Business": {"bg": "#1a1a2e", "header": "#e9c46a", "accent": "#f4a261"},
    "Crime":   {"bg": "#370617", "header": "#e85d04", "accent": "#faa307"},
    "Default": {"bg": "#0f1923", "header": "#e63946", "accent": "#457b9d"},
}

# Image dimensions (Instagram square)
WIDTH, HEIGHT = 1080, 1080


def get_font(size, bold=False):
    """Try to load system fonts, fall back to default"""
    font_paths = [
        # Ubuntu/Debian (GitHub Actions)
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'Bold' if bold else ''}.ttf",
        f"/usr/share/fonts/truetype/liberation/LiberationSans-{'Bold' if bold else 'Regular'}.ttf",
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        # Windows
        "C:/Windows/Fonts/arial.ttf",
    ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue

    # Default fallback
    return ImageFont.load_default()


def draw_rounded_rect(draw, coords, radius, fill):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = coords
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.ellipse([x1, y1, x1 + radius*2, y1 + radius*2], fill=fill)
    draw.ellipse([x2 - radius*2, y1, x2, y1 + radius*2], fill=fill)
    draw.ellipse([x1, y2 - radius*2, x1 + radius*2, y2], fill=fill)
    draw.ellipse([x2 - radius*2, y2 - radius*2, x2, y2], fill=fill)


def create_post_image(title, source, category="General", output_path="/tmp/post_image.jpg"):
    """Create a beautiful 1080x1080 news post image"""

    # Get theme colors
    theme = THEMES.get(category, THEMES["Default"])
    bg_color = theme["bg"]
    header_color = theme["header"]
    accent_color = theme["accent"]

    # Create base image
    img = Image.new('RGB', (WIDTH, HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)

    # === BACKGROUND DESIGN ===
    # Large decorative circle (background element)
    draw.ellipse([-200, -200, 700, 700], fill=_lighten(bg_color, 15))
    draw.ellipse([500, 400, 1300, 1300], fill=_lighten(bg_color, 10))

    # === TOP HEADER BAR ===
    draw.rectangle([0, 0, WIDTH, 130], fill=header_color)

    # Channel name
    header_font = get_font(46, bold=True)
    draw.text((50, 40), "🔴  TAMIL NADU UPDATES", font=header_font, fill="white")

    # Live badge
    draw_rounded_rect(draw, [900, 42, 1030, 88], 8, fill="white")
    badge_font = get_font(28, bold=True)
    draw.text((916, 50), "LATEST", font=badge_font, fill=header_color)

    # === CATEGORY TAG ===
    cat_font = get_font(32, bold=True)
    cat_text = f"  {category.upper()}  "
    draw_rounded_rect(draw, [50, 155, 50 + len(cat_text) * 18 + 20, 205], 6, fill=accent_color)
    draw.text((60, 160), cat_text, font=cat_font, fill="white")

    # === NEWS TITLE ===
    title_font = get_font(56, bold=True)
    # Wrap title to fit
    max_chars = 26
    wrapped = textwrap.wrap(title, width=max_chars)[:6]

    y = 240
    for line in wrapped:
        draw.text((60, y), line, font=title_font, fill="white")
        y += 70

    # === DIVIDER LINE ===
    draw.rectangle([60, y + 20, WIDTH - 60, y + 24], fill=header_color)
    y += 50

    # === DATE & SOURCE ===
    meta_font = get_font(34)
    date_str = datetime.now().strftime("%d %B %Y  |  %I:%M %p")
    draw.text((60, y + 10), f"🕐  {date_str}", font=meta_font, fill=accent_color)

    # === BOTTOM FOOTER ===
    draw.rectangle([0, 940, WIDTH, HEIGHT], fill=header_color)

    # Source
    source_font = get_font(32)
    draw.text((50, 960), f"📰  {source}", font=source_font, fill="white")

    # Follow text
    follow_font = get_font(30)
    draw.text((50, 1005), "Follow @TamilNaduUpdates for daily updates", font=follow_font, fill="rgba(255,255,255,180)")

    # === WATERMARK LOGO AREA ===
    logo_font = get_font(28, bold=True)
    draw.text((WIDTH - 250, 960), "tamilnaduupdates.com", font=logo_font, fill="rgba(255,255,255,150)")

    # Save image
    img.save(output_path, 'JPEG', quality=95)
    print(f"  Image saved: {output_path}")
    return output_path


def _lighten(hex_color, amount):
    """Lighten a hex color by amount (0-255)"""
    try:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + amount)
        g = min(255, g + amount)
        b = min(255, b + amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    except:
        return hex_color


if __name__ == "__main__":
    # Test image creation
    create_post_image(
        title="Chennai Metro Phase 2 Construction Reaches Major Milestone Ahead of Schedule",
        source="The Hindu - Tamil Nadu",
        category="General",
        output_path="test_image.jpg"
    )
    print("Test image saved as test_image.jpg")
