#!/usr/bin/env python3
"""Inject AdSense script tag into all HTML pages across the entire site."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ADSENSE_TAG = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3258394111169733" crossorigin="anonymous"></script>'

# Files to skip (partials, non-pages)
SKIP = {'nav.html', 'footer.html', '404.html'}

# The anchor to inject after — present in every page
ANCHOR = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'

def inject_into_file(path):
    content = path.read_text(encoding='utf-8')
    if 'pagead2.googlesyndication.com' in content:
        return False  # already done

    if ANCHOR not in content:
        print(f'  SKIP (no anchor): {path}')
        return False

    content = content.replace(ANCHOR, f'{ANCHOR}\n    {ADSENSE_TAG}')
    path.write_text(content, encoding='utf-8')
    return True


def main():
    updated = 0

    # Walk all directories, find .html files
    for html_file in sorted(ROOT.rglob('*.html')):
        # Skip partials and scripts dir
        if html_file.name in SKIP:
            continue
        parts = html_file.relative_to(ROOT).parts
        if parts[0] in ('scripts', '.git', '.claude', 'node_modules'):
            continue

        if inject_into_file(html_file):
            updated += 1
            print(f'  ✓ {html_file.relative_to(ROOT)}')

    print(f'\nInjected AdSense into {updated} files.')


if __name__ == '__main__':
    main()
