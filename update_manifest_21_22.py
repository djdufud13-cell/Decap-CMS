#!/usr/bin/env python3
import json

manifest_path = "C:/Users/Administrator/.qclaw/workspace/liudeboke-blog/manifest.json"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Add article 21
article21 = {
    "id": "21",
    "slug": "phenolic-resin-mechanical-parts-why-industrial-manufacturers",
    "title": "Phenolic Resin Mechanical Parts: Why Industrial Manufacturers Choose Bakelite in 2026",
    "titleEn": "Phenolic Resin Mechanical Parts: Why Industrial Manufacturers Choose Bakelite in 2026",
    "category": "Market Analysis",
    "tags": ["phenolic resin mechanical parts manufacturer", "bakelite mechanical parts manufacturer", "phenolic resin parts price 2026"],
    "date": "2026-05-15",
    "readtime": 8,
    "excerpt": "Market dynamics driving phenolic resin adoption in 2026: feedstock price trends (phenol CNY 6,800-9,500/ton), geopolitical supply disruptions, and actionable procurement recommendations.",
    "zh": None,
    "en": "posts/en/21-phenolic-resin-mechanical-parts-why-industrial-manufacturers.html",
    "ja": None,
    "ko": None,
    "featured": False,
    "ru": None,
    "es": None,
    "fr": None,
    "it": None,
    "th": None,
    "vi": None
}

# Add article 22
article22 = {
    "id": "22",
    "slug": "phenolic-resin-mechanical-parts-supplier-global-sourcing-str",
    "title": "Phenolic Resin Mechanical Parts Supplier: Global Sourcing Strategies and Market Outlook 2026",
    "titleEn": "Phenolic Resin Mechanical Parts Supplier: Global Sourcing Strategies and Market Outlook 2026",
    "category": "Supplier Selection",
    "tags": ["phenolic resin mechanical parts supplier", "PF resin parts supplier", "phenolic resin parts sourcing 2026"],
    "date": "2026-05-15",
    "readtime": 10,
    "excerpt": "Global sourcing strategies for phenolic resin mechanical parts in 2026: regional supplier dynamics, phenol/formaldehyde price intelligence, supplier evaluation framework, and emerging trends.",
    "zh": None,
    "en": "posts/en/22-phenolic-resin-mechanical-parts-supplier-global-sourcing-str.html",
    "ja": None,
    "ko": None,
    "featured": False,
    "ru": None,
    "es": None,
    "fr": None,
    "it": None,
    "th": None,
    "vi": None
}

manifest["articles"].append(article21)
manifest["articles"].append(article22)

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"manifest.json updated. Total articles: {len(manifest['articles'])}")
