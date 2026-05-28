#!/usr/bin/env python3
"""Save an AI-generated analyst report to the ai-analyst/ directory.

Usage:
    python3 scripts/save_ai_report.py "公司名称"
    python3 scripts/save_ai_report.py "公司名称" --commit   # auto commit & push
"""
import json
import os
import re
import subprocess
import sys

WORKER_URL = "https://ai-analyst.dingjiu1989.workers.dev"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_JSON = os.path.join(BASE_DIR, "articles.json")
INDEX_HTML = os.path.join(BASE_DIR, "ai-analyst", "index.html")
REPORTS_DIR = os.path.join(BASE_DIR, "ai-analyst")
TODAY = "2026-05-28"


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(1)

    company = sys.argv[1].strip()
    do_commit = "--commit" in sys.argv

    print(f"Generating {company} report...")

    # 1. Call Worker (use curl for reliability with long-running requests)
    payload = json.dumps({"company": company})
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", WORKER_URL,
             "-H", "Content-Type: application/json",
             "-d", payload,
             "--max-time", "180"],
            capture_output=True, text=True, timeout=200,
        )
        if result.returncode != 0:
            print(f"Worker request failed (exit={result.returncode})")
            sys.exit(1)
        data = json.loads(result.stdout)
    except Exception as e:
        print(f"Worker request failed: {e}")
        sys.exit(1)

    if not data.get("ok"):
        print(f"Generation failed: {data.get('error', 'unknown')}")
        sys.exit(1)

    html = data["html"]
    slug = data["slug"]
    company_name = data["company"]
    stock_code = data["code"]
    subtitle = data.get("subtitle", "").strip() or "AI 深度研究"
    title = f"{company_name}全面分析报告：{subtitle}"
    filename = f"{slug}.html"
    filepath = os.path.join(REPORTS_DIR, filename)

    # 2. Save HTML
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  HTML saved: ai-analyst/{filename} ({len(html)} bytes)")

    # 3. Register in articles.json
    with open(ARTICLES_JSON, encoding="utf-8") as f:
        articles = json.load(f)

    for board in articles["boards"]:
        if board["id"] == "ai-analyst":
            posts = board["posts"]
            # Check for duplicate
            if any(p["slug"] == slug for p in posts):
                print(f"  Slug '{slug}' already exists in articles.json, skipping")
                break
            next_id = max(p["id"] for p in posts) + 1
            posts.append({
                "id": next_id,
                "slug": slug,
                "title": title,
                "description": f"深度分析{company_name}（{stock_code}）：AI 深度研究报告，覆盖财务、技术面、竞品、估值与风险分析。",
                "date": TODAY,
                "lastActive": TODAY,
                "tags": [company_name, "投资分析", "深度研究"],
            })
            break

    with open(ARTICLES_JSON, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"  articles.json updated (total: {len(posts)})")

    # 4. Update index.html — parse JSON-LD as real JSON
    with open(INDEX_HTML, encoding="utf-8") as f:
        index_content = f.read()

    # 4a. Update article count in description
    index_content = re.sub(
        r'（\d+ 篇文章）',
        f'（{len(posts)} 篇文章）',
        index_content,
    )

    # 4b. Patch the CollectionPage JSON-LD block
    # Find the first JSON-LD block (CollectionPage with itemListElement)
    ld_pattern = re.compile(
        r'(<script type="application/ld\+json">\s*)(\{.*?"@type"\s*:\s*"CollectionPage".*?itemListElement.*?\}\s*\})\s*(</script>)',
        re.DOTALL,
    )
    ld_match = ld_pattern.search(index_content)
    if not ld_match:
        print("  ERROR: Could not find CollectionPage JSON-LD")
        sys.exit(1)

    ld_json = json.loads(ld_match.group(2))
    items = ld_json.get("mainEntity", {}).get("itemListElement", [])

    # Check for duplicate
    new_url = f"https://aidev.fit/ai-analyst/{filename}"
    if not any(item.get("url") == new_url for item in items):
        items.append({"@type": "ListItem", "position": len(items) + 1, "url": new_url})
        ld_json["numberOfItems"] = len(items)
        ld_json["mainEntity"]["itemListElement"] = items

        new_ld = json.dumps(ld_json, ensure_ascii=False)
        index_content = index_content[:ld_match.start(2)] + new_ld + index_content[ld_match.end(2):]
        print(f"  JSON-LD updated (numberOfItems={len(items)})")
    else:
        print(f"  JSON-LD already contains this entry, skipping")

    # 4c. Add noscript <li> (check for duplicate first)
    li_tag = f'<li><a href="/ai-analyst/{filename}">{title}</a> <small>{TODAY}</small></li>'
    if f'href="/ai-analyst/{filename}"' not in index_content:
        index_content = index_content.replace(
            '</ul></noscript></div>',
            f'{li_tag}\n</ul></noscript></div>',
        )
        print(f"  index.html noscript list updated")
    else:
        print(f"  index.html already contains this entry, skipping")

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(index_content)

    # 5. Commit & push
    if do_commit:
        subprocess.run(
            ["git", "add", filepath, ARTICLES_JSON, INDEX_HTML],
            cwd=BASE_DIR, check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", f"Register {company_name} AI-generated report in analyst section"],
            cwd=BASE_DIR, check=True,
        )
        subprocess.run(["git", "push"], cwd=BASE_DIR, check=True)
        print(f"  Committed and pushed")
    else:
        print(f"\nTo commit: git add ai-analyst/{filename} articles.json ai-analyst/index.html && git commit -m 'Register {company_name} report' && git push")

    print(f"\n  https://aidev.fit/ai-analyst/{filename}")


if __name__ == "__main__":
    main()
