#!/usr/bin/env python3
"""Bump freshness dates on old articles to trigger Google re-crawl.

Picks N random eligible articles (lastActive >30 days old) and updates
their lastActive to today. This propagates to:
  - Sitemap <lastmod>
  - JSON-LD dateModified
  - OpenGraph article:modified_time
  - Visible "Last active" badge on article page

Usage:
  python3 scripts/bump_freshness.py [--count=10] [--dry-run]
"""

import json, random, sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN_JSON = ROOT / 'en' / 'articles.json'
ZH_JSON = ROOT / 'zh' / 'articles.json'
TODAY = date.today().isoformat()

STALE_DAYS = 30  # Articles older than this are eligible


def bump(json_path, count=10, dry_run=False):
    """Bump lastActive on `count` random eligible articles."""
    with open(json_path) as f:
        data = json.load(f)

    eligible = []
    threshold = date.today() - timedelta(days=STALE_DAYS)

    for board in data['boards']:
        for post in board['posts']:
            la = post.get('lastActive') or post['date']
            if la < threshold.isoformat():
                eligible.append((board, post))

    if not eligible:
        print(f'  No eligible articles (all within {STALE_DAYS} days).')
        return 0

    # Pick random subset, weighted toward older articles
    random.shuffle(eligible)
    # Sort by lastActive ascending so oldest get bumped first
    eligible.sort(key=lambda x: x[1].get('lastActive', x[1]['date']))
    picked = eligible[:count]

    for board, post in picked:
        old_la = post.get('lastActive', post['date'])
        post['lastActive'] = TODAY
        print(f'  {board["id"]:12s} {post["slug"]:40s} {old_la} → {TODAY}')

    if not dry_run:
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f'  Updated {len(picked)} articles in {json_path.name}')

    return len(picked)


def main():
    count = 10
    dry_run = False
    for arg in sys.argv[1:]:
        if arg.startswith('--count='):
            count = int(arg.split('=')[1])
        elif arg == '--dry-run':
            dry_run = True

    tag = ' [DRY RUN]' if dry_run else ''
    print(f'Bumping freshness (count={count}){tag}...')

    en_count = bump(EN_JSON, count, dry_run)
    zh_count = bump(ZH_JSON, max(1, count // 3), dry_run)
    print(f'Done{tag}. EN: {en_count}, ZH: {zh_count}')


if __name__ == '__main__':
    main()
