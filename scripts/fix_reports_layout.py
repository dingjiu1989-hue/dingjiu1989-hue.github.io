"""
Fix all AI Analyst reports:
1. Move scripts from after </html> to before </body>
2. Add bg-gray-50 to body if missing
3. Add section navigation bar at top of content area
4. Handle CCB CN separately (different layout)
5. Deduplicate nav bars (idempotent — safe to run multiple times)

Usage: python3 scripts/fix_reports_layout.py
"""

import os
import re

REPORTS_DIR = '/Users/daniel/gh-pages-demo'

REPORTS = [
    'ai-analyst/nvidia-2026.html',
    'ai-analyst/google-2026.html',
    'ai-analyst/microsoft-2026.html',
    'ai-analyst/amazon-2026.html',
    'ai-analyst/meta-2026.html',
    'ai-analyst/tsmc-2026.html',
    'ai-analyst/broadcom-2026.html',
    'ai-analyst/tencent-2026.html',
    'ai-analyst/apple-2026.html',
    'ai-analyst/baba-2026.html',
    'ai-analyst/xiaomi-group-2026.html',
    'ai-analyst/huahong-semiconductor-2026.html',
    'ai-analyst/oracle-2026.html',
    'ai-analyst/netflix-2026.html',
    'ai-analyst/asml-2026.html',
    'ai-analyst/amd-2026.html',
    'ai-analyst/catl-2026.html',
    'ai-analyst/ccb-2026.html',
    'ai-analyst/micron-2026.html',
    'en/ai-analyst/nvidia-2026-en.html',
    'en/ai-analyst/google-2026-en.html',
    'en/ai-analyst/microsoft-2026-en.html',
    'en/ai-analyst/amazon-2026-en.html',
    'en/ai-analyst/meta-2026-en.html',
    'en/ai-analyst/tsmc-2026-en.html',
    'en/ai-analyst/broadcom-2026-en.html',
    'en/ai-analyst/tencent-2026-en.html',
    'en/ai-analyst/baba-2026-en.html',
    'en/ai-analyst/oracle-2026-en.html',
    'en/ai-analyst/netflix-2026-en.html',
    'en/ai-analyst/asml-2026-en.html',
    'en/ai-analyst/amd-2026-en.html',
    'en/ai-analyst/catl-2026-en.html',
    'en/ai-analyst/ccb-2026-en.html',
    'en/ai-analyst/micron-2026-en.html',
    'en/ai-analyst/tesla-2026.html',
    'en/ai-analyst/apple-2026-en.html',
]

NAV_CSS = '''
    /* ── Section Navigation ── */
    .section-nav { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 24px; justify-content: center; }
    .nav-pill { display: inline-block; padding: 5px 12px; font-size: .78rem; font-weight: 600; border-radius: 999px; background: #f1f5f9; color: #475569; text-decoration: none; transition: all .15s; white-space: nowrap; }
    .nav-pill:hover { background: #2563eb; color: #fff; }
    @media (max-width: 480px) { .section-nav { gap: 4px; } .nav-pill { font-size: .72rem; padding: 4px 10px; } }
    '''


def is_cn_report(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        head = f.read(2000)
    return 'lang="zh-CN"' in head


def is_ccb_cn(filepath):
    return 'ai-analyst/ccb-2026.html' == filepath.replace(REPORTS_DIR + '/', '')


def deduplicate_nav(content):
    """Remove duplicate section-nav divs and CSS, keeping only one of each."""
    # Deduplicate section-nav HTML divs — keep only the first
    nav_div_count = len(re.findall(r'<div\s+class="section-nav">', content))
    if nav_div_count > 1:
        # Remove all section-nav divs, then re-add one at the first position
        # First, find and capture the first nav div content
        first_match = re.search(r'<!-- Section Navigation -->\s*<div class="section-nav">.*?</div>', content, re.DOTALL)
        first_nav = first_match.group(0) if first_match else ''

        # Remove all nav divs (including the comment markers)
        content = re.sub(
            r'\s*<!-- Section Navigation -->\s*<div class="section-nav">.*?</div>\s*',
            '\n',
            content,
            flags=re.DOTALL
        )
        # Put back the first one after the prose-container opening (or appropriate location)
        content = re.sub(
            r'(<div\s+class="prose-container">)\s*',
            r'\1\n    ' + first_nav.strip() + '\n',
            content,
            count=1
        )

    # Deduplicate section-nav CSS — keep only the last occurrence
    css_blocks = re.findall(r'/\* ── Section Navigation ── \*/.*?@media[^}]*\}', content, re.DOTALL)
    if len(css_blocks) > 1:
        # Remove all but the last
        for block in css_blocks[:-1]:
            content = content.replace(block, '', 1)

    return content


def fix_body_class(content):
    """Add bg-gray-50 to body tag if missing."""
    if 'bg-gray-50' in content:
        return content

    # <body> with no class attribute
    content = re.sub(r'(<body\s*>)', r'<body class="bg-gray-50">', content)
    return content


def fix_scripts_after_html(content):
    """Move scripts from after </html> to before </body>."""
    last_html = content.rfind('</html>')
    if last_html < 0:
        return content

    after = content[last_html + 7:]  # everything after </html>
    # Check if there are any script tags in the after section
    if '<script' not in after and 'include' not in after and 'render' not in after:
        return content

    # Extract stray content
    match = re.search(r'</html>\s*((?:\s*<script[^>]*>.*?</script>\s*)*)', content, re.DOTALL)
    if not match:
        return content

    stray = match.group(1).strip()
    if not stray:
        return content

    content = content[:match.start(1)] + content[match.end(1):]
    content = content.replace('</body>', stray + '\n</body>', 1)
    return content


def add_section_nav(content, items):
    """Add section navigation bar at top of content — only if not already present."""
    if '<div class="section-nav">' in content:
        return content

    # Build nav HTML
    links = ' '.join(
        f'<a href="#{anchor}" class="nav-pill">{label}</a>' for anchor, label in items
    )
    nav_html = f'''
    <!-- Section Navigation -->
    <div class="section-nav">
        {links}
    </div>
    '''

    # Insert after the opening content container
    content = re.sub(
        r'(<div\s+class="prose-container">)\s*',
        r'\1' + nav_html,
        content,
        count=1
    )
    return content


def add_section_nav_ccb(content, items):
    """Add section nav for CCB CN (article-card layout)."""
    if '<div class="section-nav">' in content:
        return content

    links = ' '.join(
        f'<a href="#{anchor}" class="nav-pill">{label}</a>' for anchor, label in items
    )
    nav_html = f'''
    <!-- Section Navigation -->
    <div class="section-nav">
        {links}
    </div>
    '''

    content = re.sub(
        r'(<(?:div|article)\s+class="article-card">)\s*',
        r'\1' + nav_html,
        content,
        count=1
    )
    return content


def add_nav_styles(content):
    """Add nav CSS if not already present."""
    if '.section-nav' in content:
        return content
    content = content.replace('</style>', NAV_CSS + '\n</style>', 1)
    return content


def fix_report(filepath):
    fullpath = os.path.join(REPORTS_DIR, filepath)
    if not os.path.exists(fullpath):
        print(f'  SKIP (not found): {filepath}')
        return False

    with open(fullpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    is_cn = is_cn_report(fullpath)
    is_ccb = is_ccb_cn(fullpath)

    # Step 0: Deduplicate nav bars (in case script was run before)
    content = deduplicate_nav(content)

    # Step 1: Fix body class
    if not is_ccb:
        content = fix_body_class(content)

    # Step 2: Fix scripts after </html>
    content = fix_scripts_after_html(content)

    # Step 3: Add nav styles + nav bar
    content = add_nav_styles(content)
    items = ['公司概况', '财务分析', '技术分析', '市场情绪', '竞品对比', '估值', '风险', '结论'] if is_cn else ['Overview', 'Financials', 'Technical', 'Sentiment', 'Competition', 'Valuation', 'Risks', 'Conclusion']
    nav_items = list(zip(['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8'], items))

    if is_ccb:
        content = add_section_nav_ccb(content, nav_items)
    else:
        content = add_section_nav(content, nav_items)

    if content != original:
        with open(fullpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  Updated: {filepath}')
        return True
    else:
        return False


def main():
    print(f'Checking {len(REPORTS)} AI Analyst reports...')
    updated = 0
    for r in REPORTS:
        if fix_report(r):
            updated += 1
    print(f'Done! {updated} files updated.')


if __name__ == '__main__':
    main()
