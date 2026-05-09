#!/usr/bin/env python3
"""
Syndicate English articles to Hashnode via GraphQL API.

Hashnode has DA 80+ and supports canonical URLs, making it a powerful
backlink source. Each article published includes a canonical URL pointing
back to our GitHub Pages site.

Auth: Personal Access Token from https://hashnode.com/settings/developer
API:  https://gql.hashnode.com/ (GraphQL)
Rate limit: ~10 requests/minute on free tier.
"""

import json, time, os, sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://dingjiu1989-hue.github.io"
EN_ARTICLES = ROOT / "en" / "articles.json"
TRACK_FILE = ROOT / "data" / "hashnode-published.json"

API_KEY = os.environ.get("HASHNODE_API_KEY")
if not API_KEY:
    key_file = ROOT / ".hashnode-key"
    if key_file.exists():
        API_KEY = key_file.read_text(encoding="utf-8").strip()

if not API_KEY:
    print("ERROR: Set HASHNODE_API_KEY env var or create .hashnode-key file")
    print("Get your key at: https://hashnode.com/settings/developer")
    sys.exit(1)

PUBLICATION_ID = os.environ.get("HASHNODE_PUBLICATION_ID", "")
HASHNODE_API = "https://gql.hashnode.com/"

import _ssl_compat  # noqa
import urllib.request
import urllib.error


def graphql(query, variables=None):
    """Execute a Hashnode GraphQL query/mutation."""
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(HASHNODE_API, data=body)
    req.add_header("Authorization", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "AI-Study-Room/1.0")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read().decode("utf-8"))
        if "errors" in result:
            raise Exception(json.dumps(result["errors"], indent=2))
        return result.get("data", {})
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        if e.code == 429:
            return {"_rate_limited": True}
        raise Exception(f"HTTP {e.code}: {err_body[:500]}")


def get_publication_id():
    """Discover the user's publication ID."""
    global PUBLICATION_ID
    if PUBLICATION_ID:
        return PUBLICATION_ID

    # Query: get current user's publications
    query = """
    query Me {
      me {
        id
        username
        publications(first: 5) {
          edges {
            node {
              id
              title
              url
            }
          }
        }
      }
    }
    """
    data = graphql(query)
    me = data.get("me", {})
    pubs = me.get("publications", {}).get("edges", [])
    if pubs:
        PUBLICATION_ID = pubs[0]["node"]["id"]
        print(f"  Found publication: {pubs[0]['node']['title']} ({PUBLICATION_ID})")
        return PUBLICATION_ID

    # Fallback: use user ID as personal blog
    user_id = me.get("id")
    if user_id:
        PUBLICATION_ID = user_id
        print(f"  Using personal blog: {me.get('username')} ({user_id})")
        return PUBLICATION_ID

    raise Exception("No publication found. Create one at https://hashnode.com/new")


def get_existing_slugs():
    """Get list of already-published article slugs."""
    if TRACK_FILE.exists():
        try:
            return set(json.loads(TRACK_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    return set()


def save_tracking(slugs):
    """Save the list of published slugs."""
    TRACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    TRACK_FILE.write_text(json.dumps(sorted(slugs), indent=2, ensure_ascii=False), encoding="utf-8")


def extract_body_markdown(html_path):
    """Extract article body and convert to Markdown-like plain text for Hashnode.
    Hashnode accepts contentMarkdown — we use the pre-generated MD files."""
    md_path = ROOT / "md" / "en" / html_path.parent.name / f"{html_path.stem}.md"
    if md_path.exists():
        content = md_path.read_text(encoding="utf-8")
        # Strip YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        # Convert relative article links to absolute URLs
        import re
        content = re.sub(
            r'\]\(/(en/(?:ai|tech|sidehustle|tools|compare)/[^)]+\.html)\)',
            rf']({BASE}/\1)',
            content
        )
        return content
    return None


def publish_to_hashnode(art, board_id, publication_id):
    """Publish one article to Hashnode with canonical URL."""
    md_body = extract_body_markdown(
        ROOT / "en" / board_id / f"{art['slug']}.html"
    )
    if not md_body:
        # Fallback: simple description
        md_body = art.get("description", art["title"])

    canonical = f"{BASE}/en/{board_id}/{art['slug']}.html"

    # Truncate if too long (Hashnode limit ~200KB)
    if len(md_body) > 150000:
        md_body = md_body[:150000] + f"\n\n... [Read full article]({canonical})"

    # Map boards to Hashnode tags
    BOARD_TAGS = {
        "ai": ["AI", "artificial-intelligence", "programming"],
        "tech": ["programming", "tutorial", "web-development"],
        "sidehustle": ["side-project", "entrepreneurship", "programming"],
        "tools": ["tools", "productivity", "programming"],
        "compare": ["programming", "comparison", "web-development"],
    }
    tags = BOARD_TAGS.get(board_id, ["programming"])

    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post {
          id
          slug
          url
          title
        }
      }
    }
    """

    variables = {
        "input": {
            "publicationId": publication_id,
            "title": art["title"],
            "contentMarkdown": md_body,
            "tags": [{"slug": t, "name": t.replace("-", " ").title()} for t in tags],
            "originalArticleURL": canonical,
            "slug": art["slug"][:60],
            "subtitle": art.get("description", "")[:140],
            "disableComments": False,
        }
    }

    data = graphql(mutation, variables)
    if data.get("_rate_limited"):
        return None, "rate_limited"

    post = data.get("publishPost", {}).get("post", {})
    return post, None


def main():
    print(f"=== Hashnode Syndicator — {date.today().isoformat()} ===\n")

    # Load articles
    en_data = json.loads(EN_ARTICLES.read_text(encoding="utf-8"))
    all_articles = []
    for board in en_data["boards"]:
        for art in board["posts"]:
            all_articles.append((art, board["id"]))

    existing = get_existing_slugs()
    already_published = len(existing)
    print(f"Already published on Hashnode: {already_published}")

    # Find unpublished articles
    unpublished = [(a, b) for a, b in all_articles if a["slug"] not in existing]
    print(f"Unpublished: {len(unpublished)}")
    if not unpublished:
        print("All articles published. Done.")
        return

    # Get publication ID
    try:
        publication_id = get_publication_id()
    except Exception as e:
        print(f"ERROR getting publication ID: {e}")
        print("Set HASHNODE_PUBLICATION_ID env var to skip discovery.")
        sys.exit(1)

    # Publish up to 3 articles per run
    published_this_run = 0
    for art, board_id in unpublished[:3]:
        print(f"  [{published_this_run + 1}/3] {art['title'][:60]}...")
        post, error = publish_to_hashnode(art, board_id, publication_id)

        if error == "rate_limited":
            print(f"    Rate limited. Stopping batch.")
            break
        elif error:
            print(f"    ERROR: {error[:200]}")
            break
        elif post:
            print(f"    URL: {post.get('url', 'N/A')}")
            existing.add(art["slug"])
            published_this_run += 1
            save_tracking(existing)

        time.sleep(3)  # Be respectful with API calls

    print(f"\nDone. {published_this_run} articles syndicated to Hashnode this run.")
    print(f"Total: {len(existing)}/{len(all_articles)} published.")


if __name__ == "__main__":
    main()
