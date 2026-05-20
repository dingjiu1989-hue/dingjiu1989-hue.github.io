#!/usr/bin/env python3
"""
Generate cover images for all articles.
Each cover is a 1200x630 PNG with gradient background, title, board label, and site name.
Used for og:image (social sharing) and inline article hero images.
"""
import json, os, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
COVERS_DIR = ROOT / "images" / "covers"
LANGS = ["en", "zh"]

# Board color schemes (background gradient from top to bottom)
BOARD_COLORS = {
    "ai": ("#7C3AED", "#4F46E5"),           # Purple → Indigo
    "tech": ("#059669", "#0891B2"),          # Emerald → Cyan
    "tools": ("#D97706", "#DC2626"),         # Amber → Red
    "compare": ("#2563EB", "#7C3AED"),       # Blue → Purple
    "sidehustle": ("#DB2777", "#9333EA"),    # Pink → Violet
    "security": ("#1E3A5F", "#0F172A"),      # Navy → Dark
    "database": ("#0D9488", "#0F766E"),      # Teal → Dark Teal
    "architecture": ("#4B5563", "#1F2937"),  # Gray → Dark Gray
}

# Board display names
BOARD_LABELS = {
    "ai": "AI", "tech": "Tech", "tools": "Tools",
    "compare": "Compare", "sidehustle": "Side Hustle",
    "security": "Security", "database": "Database",
    "architecture": "Architecture",
}
BOARD_LABELS_ZH = {
    "ai": "AI 人工智能", "tech": "技术", "tools": "工具",
    "compare": "对比", "sidehustle": "副业",
    "security": "安全", "database": "数据库",
    "architecture": "架构",
}

W, H = 1200, 630


def get_font(size, bold=False):
    """Get a font that supports both CJK and Latin chars."""
    font_paths = [
        "/Library/Fonts/Arial Unicode.ttf",      # Best CJK coverage
        "/System/Library/Fonts/Helvetica.ttc",    # English fallback
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def make_gradient(draw, color1, color2):
    """Draw a vertical gradient from color1 (top) to color2 (bottom)."""
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    for y in range(H):
        ratio = y / H
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))


def draw_cover(title, board, lang, output_path):
    colors = BOARD_COLORS.get(board, ("#4B5563", "#1F2937"))
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    make_gradient(draw, colors[0], colors[1])

    # Board tag (top-left)
    tag_font = get_font(24)
    label = BOARD_LABELS_ZH.get(board, board) if lang == "zh" else BOARD_LABELS.get(board, board)
    tag_text = label.upper()
    tag_bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
    tag_w, tag_h = tag_bbox[2] - tag_bbox[0], tag_bbox[3] - tag_bbox[1]
    tag_x, tag_y = 60, 50
    # Tag background pill
    draw.rounded_rectangle(
        [tag_x - 20, tag_y - 10, tag_x + tag_w + 20, tag_y + tag_h + 10],
        radius=20, fill=(255, 255, 255, 40)
    )
    draw.text((tag_x, tag_y), tag_text, fill="#FFFFFF", font=tag_font)

    # Title (centered, wrapped)
    title_font = get_font(42, bold=True)
    max_width = W - 200
    # Wrap title into lines that fit
    lines = []
    words = title.split(" ")
    current = ""
    for w in words:
        test = current + (" " if current else "") + w
        bbox = draw.textbbox((0, 0), test, font=title_font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)

    # If still too long (e.g., CJK text without spaces), do character wrapping
    if not lines:
        current = ""
        for ch in title:
            test = current + ch
            bbox = draw.textbbox((0, 0), test, font=title_font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = ch
        if current:
            lines.append(current)

    # Draw title lines
    line_h = 56
    total_h = len(lines) * line_h
    start_y = (H - total_h) // 2 - 20
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        w = bbox[2] - bbox[0]
        x = (W - w) // 2
        y = start_y + i * line_h
        # Text shadow
        draw.text((x + 2, y + 2), line, fill=(0, 0, 0, 80), font=title_font)
        draw.text((x, y), line, fill="#FFFFFF", font=title_font)

    # Site name (bottom)
    site_font = get_font(22)
    site_text = "SourceHub" if lang == "en" else "SourceHub · AI 自习室"
    site_bbox = draw.textbbox((0, 0), site_text, font=site_font)
    site_w = site_bbox[2] - site_bbox[0]
    draw.text(((W - site_w) // 2, H - 70), site_text, fill=(255, 255, 255, 180), font=site_font)

    # Decorative line above site name
    line_y = H - 85
    draw.line([(W // 2 - 60, line_y), (W // 2 + 60, line_y)], fill=(255, 255, 255, 100), width=2)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "PNG")
    webp_path = str(output_path).replace('.png', '.webp')
    img.save(webp_path, "WEBP", quality=82)


def main():
    for lang in LANGS:
        articles_json = ROOT / lang / "articles.json"
        if not articles_json.exists():
            continue
        data = json.loads(articles_json.read_text(encoding="utf-8"))
        total = 0
        for board in data["boards"]:
            bid = board["id"]
            for art in board["posts"]:
                out_path = COVERS_DIR / lang / bid / f"{art['slug']}.png"
                if out_path.exists():
                    continue
                draw_cover(art["title"], bid, lang, out_path)
                total += 1
        print(f"{lang}: generated {total} new covers")

    # Also generate a default OG image
    default_path = ROOT / "images" / "og-default.png"
    if not default_path.exists():
        img = Image.new("RGB", (W, H))
        draw = ImageDraw.Draw(img)
        make_gradient(draw, "#4F46E5", "#7C3AED")
        font = get_font(36)
        text = "SourceHub"
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, (H - 50) // 2), text, fill="#FFFFFF", font=font)
        default_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(default_path), "PNG")
        img.save(str(default_path).replace('.png', '.webp'), "WEBP", quality=82)
        print("Created default og image")

    print("Done.")


if __name__ == "__main__":
    main()
