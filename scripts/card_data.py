"""Shared card data for AI analyst search cards.

Central source of truth for company name mappings, sector assignments,
and helper functions. Imported by add_search_cards.py, fix_search_cards.py,
and gen_ai_report.py.
"""
import re

# ── Hand-written reports (already have correct names — DON'T touch) ──
HAND_WRITTEN_SLUGS = {
    'nvidia-2026', 'google-2026', 'microsoft-2026', 'amazon-2026',
    'meta-2026', 'tsmc-2026', 'broadcom-2026', 'tencent-2026',
    'apple-2026', 'baba-2026', 'xiaomi-group-2026', 'huahong-semiconductor-2026',
    'oracle-2026', 'netflix-2026', 'asml-2026', 'amd-2026', 'catl-2026',
    'ccb-2026', 'micron-2026',
    '600036-2026', '600900-2026', '601988-2026', '601398-2026', '601288-2026',
}

# ── Name mapping: slug -> (en_short_name, cn_short_name) ──
# Covers ALL batch-generated companies
NAME_MAP = {
    # First batch (from add_search_cards.py)
    '688981-2026': ('SMIC', '中芯国际'),
    '688041-2026': ('Hygon', '海光信息'),
    '002371-2026': ('NAURA', '北方华创'),
    '603501-2026': ('Will Semiconductor', '韦尔股份'),
    '688012-2026': ('AMEC', '中微公司'),
    '688256-2026': ('Cambricon', '寒武纪'),
    '603986-2026': ('GigaDevice', '兆易创新'),
    '002049-2026': ('Unigroup Guoxin', '紫光国微'),
    '600584-2026': ('JCET', '长电科技'),
    '688008-2026': ('Montage Technology', '澜起科技'),
    '300782-2026': ('Maxscend', '卓胜微'),
    '300661-2026': ('SG Micro', '圣邦股份'),
    '300223-2026': ('Ingenic', '北京君正'),
    '002185-2026': ('Huatian Technology', '华天科技'),
    '002156-2026': ('Tongfu Microelectronics', '通富微电'),
    # Second batch (from fix_search_cards.py)
    '600460-2026': ('Silan Micro', '士兰微'),
    '688396-2026': ('China Resources Microelectronics', '华润微'),
    '688099-2026': ('Amlogic', '晶晨股份'),
    '688385-2026': ('Fudan Micro', '复旦微电'),
    '688052-2026': ('Novosense Micro', '纳芯微'),
    '688536-2026': ('3Peak', '思瑞浦'),
    '688047-2026': ('Loongson', '龙芯中科'),
    '688126-2026': ('NSIG', '沪硅产业'),
    '688019-2026': ('Anji Micro', '安集科技'),
    '688072-2026': ('Piotech', '拓荆科技'),
}

# ── A-stock codes that should be '半导体' sector ──
SEMICONDUCTOR_CODES = {
    '688981', '688041', '002371', '603501', '688012', '688256', '603986',
    '002049', '600584', '688008', '300782', '300661', '300223', '002185',
    '002156', '600460', '688396', '688099', '688385', '688052',
    '688536', '688047', '688126', '688019', '688072',
}

# ── Sector → badge color ──
SECTOR_COLORS = {
    '半导体': 'red-600',
    '金融': 'blue-600',
    '科技': 'blue-600',
    '新能源': 'green-600',
    '公用事业': 'yellow-500',
    'AI': 'purple-600',
    '通信': 'indigo-600',
    '消费电子': 'orange-500',
}


# ── Helpers ──

def get_name(slug):
    """Short English name for a slug."""
    if slug in NAME_MAP:
        return NAME_MAP[slug][0]
    return slug.split('-')[0]


def get_name_cn(slug):
    """Short Chinese name for a slug."""
    if slug in NAME_MAP:
        return NAME_MAP[slug][1]
    return slug.split('-')[0]


def get_sector(slug):
    """Sector label for a slug (半导体 or 科技)."""
    code = slug.split('-')[0]
    return '半导体' if code in SEMICONDUCTOR_CODES else '科技'


def get_rating_color(sector):
    """Badge color for a sector."""
    return SECTOR_COLORS.get(sector, 'blue-600')


def get_sector_color(sector):
    """Alias for get_rating_color."""
    return get_rating_color(sector)


def slug_to_ticker(slug):
    """Convert slug like '002156-2026' → '002156.SZ'."""
    code = slug.split('-')[0]
    if code.isdigit():
        if code.startswith('6') or code.startswith('688'):
            return f'{code}.SH'
        if code.startswith('0') or code.startswith('3'):
            return f'{code}.SZ'
    return code


def is_batch_entry(slug, c):
    """Check if this card is batch-generated (not hand-written)."""
    if slug in HAND_WRITTEN_SLUGS:
        return False
    code = slug.split('-')[0]
    if code.isdigit():
        return True
    if '全面分析报告' in c.get('name', '') or '全面分析报告' in c.get('nameCn', ''):
        return True
    return False


def clean_summary(text):
    """Remove markdown formatting artifacts from summary text."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\\n\\n', ' ', text)
    text = re.sub(r'\\n', ' ', text)
    text = text.replace('**', '')
    if len(text) > 150:
        text = text[:147] + '...'
    return text.strip()
