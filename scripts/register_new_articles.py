#!/usr/bin/env python3
"""Scan md directories and register new articles in articles.json."""
import json, re, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EN_MD = ROOT / 'md' / 'en'
ZH_MD = ROOT / 'md' / 'zh'
EN_JSON = ROOT / 'en' / 'articles.json'
ZH_JSON = ROOT / 'articles.json'  # root-level, not zh/

BOARD_TAGS = {
    'tech': ['Technology','DevOps','Cloud'],
    'sidehustle': ['Business','Startup','SaaS'],
    'tools': ['Technology','DevTools','Productivity'],
    'ai': ['AI','Machine Learning','LLM'],
    'compare': ['Technology','Comparison','Reviews'],
    'security': ['Security','DevOps','Cloud'],
    'database': ['Database','Backend','Data'],
    'architecture': ['Architecture','System Design','Backend'],
}

def parse_frontmatter(path):
    with open(path) as f:
        content = f.read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).strip().split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm

def get_slug(path):
    return path.stem

def get_board(path):
    return path.parent.name

def register_new(lang, md_dir, json_path):
    with open(json_path) as f:
        data = json.load(f)

    existing = {}
    for b in data['boards']:
        for p in b['posts']:
            existing[(b['id'], p['slug'])] = True

    added = 0
    for board_dir in sorted(md_dir.iterdir()):
        if not board_dir.is_dir():
            continue
        board_id = board_dir.name
        for md_file in sorted(board_dir.glob('*.md')):
            slug = get_slug(md_file)
            if (board_id, slug) in existing:
                continue
            fm = parse_frontmatter(md_file)
            if not fm:
                print(f"  SKIP (no frontmatter): {md_file.name}")
                continue

            title = fm.get('title', slug.replace('-', ' ').title())
            desc = fm.get('description', '')
            date = fm.get('date', '2026-05-12')
            tags = BOARD_TAGS.get(board_id, ['Technology'])

            entry = {
                'slug': slug,
                'title': title,
                'description': desc[:160],
                'date': date,
                'tags': tags,
                'pinned': False,
                'replies': 0,
            }

            match = [b for b in data['boards'] if b['id'] == board_id]
            if not match:
                print(f"  SKIP: no board '{board_id}' in articles.json")
                continue
            board = match[0]
            board['posts'].append(entry)
            existing[(board_id, slug)] = True
            added += 1
            print(f"  ADDED: {board_id}/{slug}")

    if added > 0:
        # Update stats
        total = sum(len(b['posts']) for b in data['boards'])
        data['site']['stats']['total'] = total
        if lang == 'en':
            data['site']['stats']['english'] = total

        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n=== {lang.upper()} === Registered {added} new articles. Total: {total}")
    else:
        print(f"\n=== {lang.upper()} === No new articles to register.")

    return added

if __name__ == '__main__':
    en_added = register_new('en', EN_MD, EN_JSON)
    zh_added = register_new('zh', ZH_MD, ZH_JSON)
    print(f"\nTotal added: {en_added + zh_added}")
