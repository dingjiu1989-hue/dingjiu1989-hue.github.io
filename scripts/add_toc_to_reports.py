#!/usr/bin/env python3
"""
Add CCB-style TOC sidebar + mobile TOC to all AI analyst reports (CN + EN).
Preserves existing NVIDIA-style prose-container layout, Chart.js code, footer.

Usage: PYTHONPATH=. python3 scripts/add_toc_to_reports.py
"""

import re
import os

BASE = '/Users/daniel/gh-pages-demo'

# ── TOC labels ──
CN_TOC = [
    ("s1", "公司概况", "fa-building"),
    ("s2", "财务分析", "fa-chart-line"),
    ("s3", "技术分析", "fa-candlestick-chart"),
    ("s4", "市场情绪", "fa-users"),
    ("s5", "竞品对比", "fa-table-cells-large"),
    ("s6", "估值与财务健康度", "fa-calculator"),
    ("s7", "主要风险", "fa-triangle-exclamation"),
    ("s8", "结论与建议", "fa-bullseye"),
]

EN_TOC = [
    ("s1", "Company Overview", "fa-building"),
    ("s2", "Financial Analysis", "fa-chart-line"),
    ("s3", "Technical Analysis", "fa-candlestick-chart"),
    ("s4", "Market Sentiment", "fa-users"),
    ("s5", "Competitive Comparison", "fa-table-cells-large"),
    ("s6", "Valuation & Financial Health", "fa-calculator"),
    ("s7", "Key Risks", "fa-triangle-exclamation"),
    ("s8", "Conclusion & Recommendations", "fa-bullseye"),
]

# ── TOC sidebar HTML ──
def toc_sidebar_html(toc_items, toc_title):
    items_html = '\n'.join(
        f'            <li><a href="#{sid}"><i class="fas {icon} fa-fw" style="width:16px;color:#2563eb"></i> {label}</a></li>'
        for sid, label, icon in toc_items
    )
    return f'''    <!-- TOC Sidebar -->
    <nav class="toc-sidebar" aria-label="{toc_title}">
        <div class="toc-title">{toc_title}</div>
        <ul class="toc-list">
{items_html}
        </ul>
    </nav>'''

def mobile_toc_html(toc_items, placeholder):
    items_html = '\n'.join(
        f'                <option value="{sid}">{label}</option>'
        for sid, label, icon in toc_items
    )
    return f'''        <!-- Mobile TOC -->
        <div class="mobile-toc">
            <select onchange="if(this.value) document.getElementById(this.value).scrollIntoView({{behavior:'smooth'}}); this.selectedIndex=0;">
                <option value="">— {placeholder} —</option>
{items_html}
            </select>
        </div>'''

# ── TOC CSS ──
TOC_CSS = '''
    /* ── TOC Sidebar ── */
    .report-wrap { max-width: 1100px; margin: 0 auto; padding: 20px; display: grid; grid-template-columns: 220px 1fr; gap: 28px; }
    @media (max-width: 1023px) { .report-wrap { grid-template-columns: 1fr; } }
    .toc-sidebar { position: sticky; top: 24px; height: fit-content; max-height: calc(100vh - 48px); overflow-y: auto; }
    .toc-sidebar::-webkit-scrollbar { width: 3px; }
    .toc-sidebar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    @media (max-width: 1023px) { .toc-sidebar { display: none; } }
    .toc-title { font-size: .7rem; font-weight: 700; text-transform: uppercase; letter-spacing: .12em; color: #64748b; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; }
    .toc-list { list-style: none; padding: 0; margin: 0; }
    .toc-list li { margin-bottom: 2px; }
    .toc-list a {
        display: block; padding: 6px 10px; border-radius: 6px;
        font-size: .8rem; color: #64748b; text-decoration: none;
        transition: all .15s; line-height: 1.3;
    }
    .toc-list a:hover { background: #e8edf5; color: #2563eb; }
    .mobile-toc { display: none; }
    @media (max-width: 1023px) {
        .mobile-toc { display: block; background: #fff; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,.06); }
        .mobile-toc select { width: 100%; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: .88rem; background: #fff; appearance: auto; color: #1e293b; }
    }
    .btt-btn {
        position: fixed; bottom: 32px; right: 32px; width: 44px; height: 44px;
        border-radius: 50%; background: #2563eb; color: #fff; border: none;
        font-size: 1.1rem; cursor: pointer; box-shadow: 0 4px 12px rgba(37,99,235,.35);
        opacity: 0; visibility: hidden; transition: all .2s; z-index: 50;
        display: flex; align-items: center; justify-content: center;
    }
    .btt-btn.show { opacity: 1; visibility: visible; }
    .btt-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(37,99,235,.45); }
'''

# ── h2 anchor regex ──
H2_RE = re.compile(r'<h2\b(?![^>]*\bid=)([^>]*)>(.*?)</h2>', re.DOTALL)

def add_h2_ids(html, toc_items):
    idx = [0]
    def replacer(m):
        attrs = m.group(1)
        content = m.group(2)
        if idx[0] < len(toc_items):
            sid = toc_items[idx[0]][0]
            idx[0] += 1
            return f'<h2 id="{sid}"{attrs}>{content}</h2>'
        return m.group(0)
    return H2_RE.sub(replacer, html)


def find_tag_before(html, pos, tag):
    """Find a tag opener like <div going backwards from pos."""
    # Look for <tag or <tag  within 100 chars before pos
    search_area = html[max(0, pos - 100):pos]
    idx = search_area.rfind('<' + tag)
    if idx == -1:
        idx = search_area.rfind('<' + tag + ' ')
    if idx == -1:
        return -1
    return max(0, pos - 100) + idx


def find_prose_container_bounds(html):
    """Find the opening and closing bounds of the prose-container div.

    Returns (start_of_opening_tag, end_of_closing_tag) or None.
    Uses proper script-block-aware div nesting.
    """
    # Find prose-container attribute
    pc_start = html.find('class="prose-container"')
    if pc_start == -1:
        pc_start = html.find("class='prose-container'")
    if pc_start == -1:
        return None

    # Find the <div opener
    div_start = find_tag_before(html, pc_start, 'div')
    if div_start == -1:
        return None

    # Find > that closes this opening div tag
    tag_close = html.find('>', pc_start)
    if tag_close == -1:
        return None

    # Now find matching </div> by counting nesting, skipping <script> blocks
    pos = tag_close + 1
    level = 1
    in_script = False

    while level > 0 and pos < len(html):
        # Find next relevant marker
        next_div_open = html.find('<div', pos)
        next_div_close = html.find('</div>', pos)
        next_script_open = html.find('<script', pos)
        next_script_close = html.find('</script>', pos)

        # If in a script block, only look for </script>
        if in_script:
            if next_script_close == -1:
                return None  # malformed
            in_script = False
            pos = next_script_close + 9  # len('</script>')
            continue

        # Collect valid markers
        candidates = []
        if next_div_open != -1:
            candidates.append((next_div_open, 'div_open'))
        if next_div_close != -1:
            candidates.append((next_div_close, 'div_close'))
        if next_script_open != -1:
            candidates.append((next_script_open, 'script_open'))
        if next_script_close != -1:
            candidates.append((next_script_close, 'script_close'))

        if not candidates:
            return None

        candidates.sort()
        earliest_pos, earliest_type = candidates[0]

        if earliest_type == 'script_open' and earliest_pos < (
            next_div_close if next_div_close != -1 else float('inf')
        ):
            in_script = True
            # also check if next_script_close == earliest_pos (empty script)
            if next_script_close == earliest_pos + 7:
                in_script = False
                pos = next_script_close + 9
            else:
                pos = earliest_pos + 7
            continue

        if earliest_type == 'div_open':
            level += 1
            pos = earliest_pos + 4
        elif earliest_type == 'div_close':
            level -= 1
            if level == 0:
                return (div_start, earliest_pos + 6)  # +6 for len('</div>')
            pos = earliest_pos + 6
        else:
            pos = earliest_pos + 1

    return None


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    is_cn = 'lang="zh-CN"' in html
    toc_items = CN_TOC if is_cn else EN_TOC
    toc_title = "目录" if is_cn else "Contents"
    toc_placeholder = "跳转到章节" if is_cn else "Jump to section"

    # Skip if already has TOC
    if 'class="report-wrap"' in html and 'class="toc-sidebar"' in html:
        print(f"  SKIP (already has TOC): {filepath}")
        return False

    # 1. Inject TOC CSS before </style>
    style_end = html.find('</style>')
    if style_end == -1:
        print(f"  WARN: no </style> in {filepath}")
        return False
    html = html[:style_end] + TOC_CSS + html[style_end:]

    # 2. Add h2 anchors
    html = add_h2_ids(html, toc_items)

    # 3. Find prose-container bounds
    bounds = find_prose_container_bounds(html)
    if bounds is None:
        print(f"  WARN: cannot find prose-container bounds in {filepath}")
        return False

    pc_div_open, pc_div_close = bounds

    # Split: before prose-container div, content inside, after closing
    # Find the > that closes the <div class="prose-container" ... >
    tag_end = html.find('>', pc_div_open)
    before_pc = html[:pc_div_open]
    prose_inner = html[tag_end + 1:pc_div_close - 6]  # -6 for </div>
    # Find what's inside the closing </div> tag area
    after_pc = html[pc_div_close:]

    # 4. Build new structure
    sidebar = toc_sidebar_html(toc_items, toc_title)
    mobile = mobile_toc_html(toc_items, toc_placeholder)
    btt_lang = "返回顶部" if is_cn else "Back to top"

    has_footer = 'footer-placeholder' in after_pc or 'footer-placeholder' in prose_inner
    has_btt = 'bttBtn' in html

    footer_div = '' if has_footer else '        <div id="footer-placeholder"></div>'

    btt_html = ''
    if not has_btt:
        btt_html = f'''<button class="btt-btn" id="bttBtn" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="{btt_lang}"><i class="fas fa-arrow-up"></i></button>
<script>
(function(){{
    var btn = document.getElementById('bttBtn');
    if(!btn) return;
    window.addEventListener('scroll', function(){{
        btn.classList.toggle('show', window.scrollY > 400);
    }});
}})();
</script>
'''

    new_body = f'''<div class="report-wrap">
{sidebar}

    <div class="report-content">
{mobile}
        <div class="prose-container">
{prose_inner}
        </div>
{footer_div}
    </div>
</div>

{btt_html}<script src="/js/include.js"></script>
<script src="/js/render.js"></script>'''

    # 5. Reassemble
    html = before_pc + new_body + '\n' + after_pc

    # Clean up duplicate include/render scripts
    html = re.sub(r'<script src="/js/include\.js"></script>\s*', '', html)
    html = re.sub(r'<script src="/js/render\.js"></script>\s*', '', html)
    # Add them back exactly once
    html = html.rstrip() + '\n<script src="/js/include.js"></script>\n<script src="/js/render.js"></script>\n'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  OK: {filepath}")
    return True


def main():
    files = []
    for d in [os.path.join(BASE, 'ai-analyst'), os.path.join(BASE, 'en', 'ai-analyst')]:
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.endswith('.html') and f not in ('index.html', 'analysis.html', 'template.html'):
                    files.append(os.path.join(d, f))

    print(f"Found {len(files)} report files to process")
    ok = 0
    for fp in files:
        try:
            if process_file(fp):
                ok += 1
        except Exception as e:
            import traceback
            print(f"  ERROR: {fp}: {e}")
            traceback.print_exc()

    print(f"\nDone. {ok}/{len(files)} files processed.")


if __name__ == '__main__':
    main()
