#!/usr/bin/env python3
"""Add contextual cross-references to articles that lack in-body internal links.

For each article without in-body links, finds the 2-3 most semantically
similar articles (based on title/description keyword overlap) and inserts
a "See also" paragraph before the closing </div> of article-body.
"""

import json, re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
EN_ARTICLES = ROOT / "en" / "articles.json"
BOARDS = ["ai", "tech", "sidehustle", "tools", "compare"]

# Articles that are index/utility pages — skip these
SKIP_FILES = {"index.html", "nav.html", "footer.html", "privacy.html"}


def load_all_articles():
    """Load all English article metadata and build a search index."""
    data = json.loads(EN_ARTICLES.read_text(encoding="utf-8"))
    articles = []
    for board in data["boards"]:
        for art in board["posts"]:
            articles.append({
                "board": board["id"],
                "slug": art["slug"],
                "title": art["title"],
                "description": art.get("description", ""),
                "date": art.get("date", ""),
            })
    return articles


def get_body(html):
    """Extract article body content."""
    m = re.search(r'<div class="article-body">(.*?)</article>', html, re.DOTALL)
    return m.group(1) if m else None


def extract_keywords(title, description):
    """Extract normalized keywords from title and description."""
    text = f"{title} {description}".lower()
    # Remove common stop words and punctuation
    words = re.findall(r'[a-z]{3,}', text)
    stop = {"the", "and", "for", "with", "your", "from", "that", "this",
            "what", "are", "how", "can", "its", "not", "you", "all",
            "best", "more", "than", "into", "has", "been", "will"}
    return set(w for w in words if w not in stop)


def find_related(article, all_articles, k=3, min_score=0.03):
    """Find k most semantically similar articles based on keyword overlap.
    Falls back to same-board articles if no strong matches found."""
    target_kw = extract_keywords(article["title"], article["description"])
    scores = []
    for other in all_articles:
        if other["slug"] == article["slug"]:
            continue
        other_kw = extract_keywords(other["title"], other["description"])
        overlap = len(target_kw & other_kw)
        union = len(target_kw | other_kw)
        if union == 0:
            continue
        score = overlap / union
        if other["board"] == article["board"]:
            score *= 1.2
        title_overlap = len(target_kw & set(re.findall(r'[a-z]{3,}', other["title"].lower())))
        score += title_overlap * 0.05
        scores.append((score, other))
    scores.sort(key=lambda x: x[0], reverse=True)

    # Filter to strong matches (above min_score) first
    strong = [s[1] for s in scores if s[0] >= min_score]
    # Then same-board articles as fallback
    same_board = [s[1] for s in scores if s[1]["board"] == article["board"] and s[1] not in strong]
    # Combine: strong matches first, then same-board, limit to k
    result = strong + same_board
    return result[:k]


def build_see_also_html(related_articles, prefix="/en/"):
    """Build a 'See also' HTML paragraph with links to related articles."""
    links = []
    for art in related_articles:
        url = f"{prefix}{art['board']}/{art['slug']}.html"
        links.append(f'<a href="{url}">{art["title"]}</a>')
    return f'<p><strong>See also:</strong> {", ".join(links)}.</p>'


def inject_see_also(html, see_also_html):
    """Insert 'See also' paragraph before the last block-level element in article-body,
    or before the closing </div> of article-body."""
    body_match = re.search(r'(<div class="article-body">.*?)(</div>\s*</article>)', html, re.DOTALL)
    if not body_match:
        return None
    prefix = body_match.group(1)
    suffix = body_match.group(2)
    return html.replace(body_match.group(0), f'{prefix}\n{see_also_html}\n{suffix}')


def process_articles(articles, board_dirs, link_pattern, label, url_prefix="/en/"):
    """Find articles without in-body links and inject cross-references."""
    needs_links = []
    for board_id in BOARDS:
        board_dir = board_dirs / board_id
        if not board_dir.exists():
            continue
        for html_file in sorted(board_dir.glob("*.html")):
            if html_file.name in SKIP_FILES:
                continue
            html = html_file.read_text(encoding="utf-8")
            body = get_body(html)
            if not body:
                continue
            internal = re.findall(link_pattern, body)
            if not internal:
                slug = html_file.stem
                art = next((a for a in articles if a["slug"] == slug), None)
                if art:
                    needs_links.append((html_file, art))

    print(f"[{label}] Articles without in-body links: {len(needs_links)}")
    if not needs_links:
        print(f"[{label}] All articles already have internal links.")
        return 0

    updated = 0
    for html_file, art in needs_links:
        related = find_related(art, articles, k=3)
        if not related:
            continue
        see_also = build_see_also_html(related, prefix=url_prefix)
        html = html_file.read_text(encoding="utf-8")
        new_html = inject_see_also(html, see_also)
        if new_html and new_html != html:
            html_file.write_text(new_html, encoding="utf-8")
            updated += 1
            titles = [r["title"] for r in related]
            print(f"  ✓ {art['board']}/{art['slug']}.html → {titles}")

    print(f"[{label}] Updated {updated} articles with cross-references.\n")
    return updated


def main():
    print("=== Internal Link Injector ===\n")

    total_updated = 0

    # ── English articles ──
    en_articles = load_all_articles()
    print(f"Loaded {len(en_articles)} English articles from en/articles.json")
    en_updated = process_articles(
        en_articles,
        ROOT / "en",
        r'href="(/en/(?:ai|tech|sidehustle|tools|compare)/[^"]+\.html)"',
        "EN",
        url_prefix="/en/"
    )
    total_updated += en_updated

    # ── Chinese articles ──
    cn_json = ROOT / "articles.json"
    if cn_json.exists():
        cn_data = json.loads(cn_json.read_text(encoding="utf-8"))
        cn_articles = []
        for board in cn_data.get("boards", []):
            for art in board.get("posts", []):
                cn_articles.append({
                    "board": board["id"],
                    "slug": art["slug"],
                    "title": art["title"],
                    "description": art.get("description", ""),
                    "date": art.get("date", ""),
                })
        print(f"Loaded {len(cn_articles)} Chinese articles from articles.json")
        cn_updated = process_articles(
            cn_articles,
            ROOT,
            r'href="(/(?:ai|tech|sidehustle|tools|compare)/[^"]+\.html)"',
            "CN",
            url_prefix="/"
        )
        total_updated += cn_updated

    # ── Regenerate AI-friendly artifacts ──
    if total_updated > 0:
        print(f"\nTotal updated: {total_updated} articles.")
        print("Regenerating Markdown copies...")
        import subprocess
        result = subprocess.run(
            ["python3", str(ROOT / "scripts" / "gen_ai_friendly.py")],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"WARNING: gen_ai_friendly.py failed:\n{result.stderr}")
    else:
        print("No articles updated.")


if __name__ == "__main__":
    main()
