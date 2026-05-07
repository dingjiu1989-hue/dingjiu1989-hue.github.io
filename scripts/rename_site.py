#!/usr/bin/env python3
"""Rename site: 资料库 → AI自习室 (CN), SourceHub → AI Study Room (EN)."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent

# Files to process (all .html, .json, .js, .xml that contain old names)
OLD_CN = '资料库'
NEW_CN = 'AI自习室'
OLD_EN = 'SourceHub'
NEW_EN = 'AI Study Room'

SKIP_DIRS = {'.git', '.superpowers', 'scripts', 'node_modules', '.claude'}

def process_file(path):
    """Replace site names in a file."""
    try:
        content = path.read_text(encoding='utf-8')
    except:
        return False

    original = content

    # Determine locale: files under /en/ use English name
    is_en = '/en/' in str(path) or path.name.startswith('en_')

    if is_en:
        content = content.replace(OLD_EN, NEW_EN)
    else:
        content = content.replace(OLD_CN, NEW_CN)

    if content != original:
        path.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    updated = 0

    for f in sorted(ROOT.rglob('*')):
        if not f.is_file():
            continue
        parts = f.relative_to(ROOT).parts
        # Skip hidden/dirs
        if any(p.startswith('.') for p in parts):
            continue
        if parts[0] in SKIP_DIRS:
            continue
        if f.suffix in ('.html', '.json', '.js', '.xml', '.md', '.txt'):
            if process_file(f):
                updated += 1
                print(f'  ✓ {f.relative_to(ROOT)}')

    # Special: update data/content-calendar.json
    cal = ROOT / 'data' / 'content-calendar.json'
    if cal.exists():
        c = cal.read_text()
        cal.write_text(c)
        process_file(cal)

    print(f'\nUpdated {updated} files.')

    # Verify
    en_data = json.loads((ROOT / 'en' / 'articles.json').read_text())
    cn_data = json.loads((ROOT / 'articles.json').read_text())
    print(f'  EN site name: {en_data["site"]["name"]}')
    print(f'  CN site name: {cn_data["site"]["name"]}')


if __name__ == '__main__':
    main()
