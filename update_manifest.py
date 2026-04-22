# -*- coding: utf-8 -*-
"""Update manifest.json with all 10 language fields for each article."""
import json
from pathlib import Path

BASE = Path(r'C:\Users\Administrator\.qclaw\workspace\liu-blog')
MANIFEST = BASE / 'manifest.json'

LANG_FIELDS = ['ja', 'ko', 'ru', 'es', 'fr', 'it', 'th', 'vi']

# Slug → ja title (for stub)
JA_TITLES = {
    'phenolic-basics': 'フェノール树脂配件入门：材料特性、优势与应用场景',
    'material-selection': '如何选择合适的酚醛树脂型号',
    'mold-design': '酚醛树脂射出成形金型设计要点',
    'quality-control': 'フェノール树脂配件品质管理方法',
    'industry-cases': 'フェノール树脂配件行业应用案例',
    'custom-process': '非標準定制フェノール树脂配件流程',
}

with open(MANIFEST, 'r', encoding='utf-8') as f:
    manifest = json.load(f)

updated = 0
for a in manifest['articles']:
    slug = a['slug']
    for lang in LANG_FIELDS:
        if lang not in a:
            a[lang] = None
    updated += 1

print(f'Updated {updated} articles with lang fields')

manifest['site']['languages'] = {
    'zh': {'name': '简体中文', 'nameNative': '简体中文', 'dir': 'ltr'},
    'en': {'name': 'English', 'nameNative': 'English', 'dir': 'ltr'},
    'ja': {'name': '日本語', 'nameNative': '日本語', 'dir': 'ltr'},
    'ko': {'name': '한국어', 'nameNative': '한국어', 'dir': 'ltr'},
    'ru': {'name': 'Русский', 'nameNative': 'Русский', 'dir': 'ltr'},
    'es': {'name': 'Español', 'nameNative': 'Español', 'dir': 'ltr'},
    'fr': {'name': 'Français', 'nameNative': 'Français', 'dir': 'ltr'},
    'it': {'name': 'Italiano', 'nameNative': 'Italiano', 'dir': 'ltr'},
    'th': {'name': 'ภาษาไทย', 'nameNative': 'ภาษาไทย', 'dir': 'ltr'},
    'vi': {'name': 'Tiếng Việt', 'nameNative': 'Tiếng Việt', 'dir': 'ltr'},
}

with open(MANIFEST, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print('manifest.json updated!')
