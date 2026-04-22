#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
刘的博客 · 自动化构建脚本 v2（全10语种）
- manifest.json 为唯一数据源
- 自动生成 posts/{lang}/, pages/{lang}/blog.html, sitemap.xml, feed.xml
- 自动注入 article list 到 index.html（各语种独立版本）
"""

import json, re, os, sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.resolve()
MANIFEST = BASE / "manifest.json"

LANGS = ['zh', 'en', 'ja', 'ko', 'ru', 'es', 'fr', 'it', 'th', 'vi']

# ── UI 翻译 ─────────────────────────────────────
T = {
    'zh': {
        'siteName': '刘的博客', 'author': '刘',
        'home': '首页', 'blog': '博客', 'products': '产品', 'contact': '联系',
        'heroBadge': '酚醛树脂配件 · 十五年专业深耕',
        'heroTitle': '十年深耕，<br>专注酚醛树脂配件。',
        'heroSubtitle': '从原材料选型到模具设计，从工艺控制到出厂检验——记录实战经验，<br>分享专业见解。',
        'aboutTitle': '关于刘',
        'aboutText': '华玲机械创始人，十五年专注酚醛树脂配件生产与研发。产品覆盖手轮、把手、手柄、油镜、阀片、旋钮等，年出口约200万件，服务30+国家客户。',
        'col1Title': '入门手册', 'col1Desc': '酚醛树脂基础知识、材料对比、选型要点——从小白到入门。',
        'col2Title': '技术深潜', 'col2Desc': '模具设计、工艺控制、质量管理——深度解析每一个技术细节。',
        'col3Title': '行业观察', 'col3Desc': '市场趋势、应用案例、非标定制——看懂行业，抓住机会。',
        'col4Title': '选型指南', 'col4Desc': '不同型号对比、参数详解、常见误区——选对产品不走弯路。',
        'stats1': '年出口件数', 'stats2': '覆盖国家', 'stats3': '年行业经验', 'stats4': '合作客户',
        'stats1Unit': '万件', 'stats2Unit': '个+',
        'newsTitle': '行业资讯', 'newsSubtitle': '技术文章与行业洞察，持续更新',
        'newsAll': '查看全部文章 →',
        'subscribeTitle': '订阅更新', 'subscribeSubtitle': '有新文章时通过邮件通知你',
        'emailPlaceholder': '输入你的邮箱',
        'subscribeBtn': '立即订阅',
        'subscribeSuccess': '订阅成功！',
        'contactTitle': '联系刘工', 'contactCompany': '华玲机械 · 河北省衡水市',
        'contactTel': '电话', 'contactEmail': '邮箱', 'contactWechat': '微信',
        'productTitle': '产品展示', 'productSubtitle': '胶木/Bakelite 配件精选',
        'pdfTitle': '下载产品目录',
        'pdfDesc': '完整产品 PDF 图册，含全部规格参数',
        'footerLinks': '快速链接', 'footerCopy': '保留所有权利',
    },
    'en': {
        'siteName': "Liu's Blog", 'author': 'Liu',
        'home': 'Home', 'blog': 'Blog', 'products': 'Products', 'contact': 'Contact',
        'heroBadge': 'Phenolic Resin Parts · 15 Years of Expertise',
        'heroTitle': '15 Years of Focus on<br>Phenolic Resin Parts.',
        'heroSubtitle': 'From material selection to mold design, from process control to final inspection — sharing practical experience and professional insights.',
        'aboutTitle': 'About Liu',
        'aboutText': "Founder of Hualing Machinery, 15 years dedicated to phenolic resin parts manufacturing. Products include handwheels, handles, levers, oil gauges, valve discs, knobs and dials. Annual exports ~2 million pcs, serving 30+ countries.",
        'col1Title': 'Getting Started', 'col1Desc': 'Phenolic resin basics, material comparison, selection tips — from beginner to confident.',
        'col2Title': 'Technical Deep Dive', 'col2Desc': 'Mold design, process control, quality management — in-depth analysis of every technical detail.',
        'col3Title': 'Industry Insights', 'col3Desc': 'Market trends, application cases, custom manufacturing — understanding the industry and opportunities.',
        'col4Title': 'Selection Guide', 'col4Desc': 'Model comparisons, parameter details, common mistakes — choose the right product without detours.',
        'stats1': 'Annual Exports', 'stats2': 'Countries', 'stats3': 'Years Experience', 'stats4': 'Clients',
        'stats1Unit': '10K+ pcs', 'stats2Unit': '+',
        'newsTitle': 'Industry News', 'newsSubtitle': 'Technical articles and industry insights, updated regularly',
        'newsAll': 'View all articles →',
        'subscribeTitle': 'Subscribe to Updates', 'subscribeSubtitle': 'Get notified by email when new articles are published',
        'emailPlaceholder': 'Enter your email',
        'subscribeBtn': 'Subscribe',
        'subscribeSuccess': 'Subscribed!',
        'contactTitle': 'Contact Liu', 'contactCompany': 'Hualing Machinery · Hengshui, Hebei, China',
        'contactTel': 'Phone', 'contactEmail': 'Email', 'contactWechat': 'WeChat',
        'productTitle': 'Product Showcase', 'productSubtitle': 'Bakelite / Phenolic Resin Parts',
        'pdfTitle': 'Download Product Catalog',
        'pdfDesc': 'Complete product PDF catalog with all specifications',
        'footerLinks': 'Quick Links', 'footerCopy': 'All rights reserved',
    },
}

# Fallback for other languages (copy English)
for lang in LANGS:
    if lang not in T:
        T[lang] = T['en'].copy()
        T[lang]['siteName'] = f"Blog {lang.upper()}"
        T[lang]['author'] = 'Liu'


# ── Article cards ────────────────────────────────
def news_card(data, lang):
    """首页行业资讯小卡片"""
    slug = data['slug']
    # Find available href for this language
    href = None
    src_lang = None
    for try_lang in [lang, 'en', 'zh']:
        if data.get(try_lang):
            href = data[try_lang]  # already contains 'posts/zh/...'
            src_lang = try_lang
            break
    if href is None:
        return ''

    cat = data.get('category', '')
    date = data.get('date', '')
    title = data.get(f'title{lang.capitalize()}') or data.get('title', '')
    excerpt = data.get('excerpt', '')
    rt = data.get('readtime', 8)
    t = T.get(lang, T['en'])

    return f'''<a href="{href}" class="news-card">
  <div class="news-card-meta"><span class="news-card-category">{cat}</span><span class="news-card-date">{date}</span></div>
  <h3 class="news-card-title">{title}</h3>
  <p class="news-card-excerpt">{excerpt[:80]}…</p>
  <span class="news-card-cta">{"阅读" if lang=="zh" else "Read"} {rt}min →</span>
</a>'''


def article_card(data, lang):
    """博客列表页大卡片"""
    slug = data['slug']
    href = None
    for try_lang in [lang, 'en', 'zh']:
        if data.get(try_lang):
            href = data[try_lang]  # already contains 'posts/zh/...'
            break
    if href is None:
        return ''

    cat = data.get('category', '')
    date = data.get('date', '')
    title = data.get(f'title{lang.capitalize()}') or data.get('title', '')
    excerpt = data.get('excerpt', '')
    rt = data.get('readtime', 8)
    tags = ''.join(f'<span class="article-tag">{tag}</span>' for tag in data.get('tags', []))

    return f'''<a href="../../{href}" class="article-card">
  <div class="article-card-inner">
    <div class="article-card-meta"><span class="article-card-category">{cat}</span><span class="article-card-date">{date}</span></div>
    <h3 class="article-card-title">{title}</h3>
    <p class="article-card-excerpt">{excerpt}</p>
    <div class="article-card-tags">{tags}</div>
    <div class="article-card-footer"><span class="article-card-readtime">{"阅读约" if lang=="zh" else "Read for"} {rt} {"分钟" if lang=="zh" else "min"}</span><span class="article-card-arrow">→</span></div>
  </div>
</a>'''


# ── Manifest → injected JS ──────────────────────
def build_manifest_js(articles, lang):
    """生成 article list JSON 注入到 index 页面，供 main.js 读取"""
    items = []
    for a in articles[:6]:  # top 6
        href = None
        for try_lang in [lang, 'en', 'zh']:
            if a.get(try_lang):
                href = a[try_lang]  # already contains 'posts/zh/01-phenolic-basics.html'
                break
        title = a.get(f'title{lang.capitalize()}') or a.get('title', '')
        items.append({
            'id': a['id'],
            'slug': a['slug'],
            'title': title,
            'category': a.get('category', ''),
            'date': a.get('date', ''),
            'excerpt': a.get('excerpt', ''),
            'readtime': a.get('readtime', 8),
            'href': href or '#',
            'tags': a.get('tags', []),
        })
    return json.dumps(items, ensure_ascii=False)


# ── Blog listing page ────────────────────────────
def build_blog_page(articles, lang):
    t = T.get(lang, T['en'])

    # Filter articles that have this lang version (or fallback to en/zh)
    available = [a for a in articles if a.get(lang) or a.get('en') or a.get('zh')]
    cards = '\n'.join(article_card(a, lang) for a in available)
    tpl = t.get('newsTitle', 'Articles')

    # Category sections
    from collections import defaultdict
    by_cat = defaultdict(list)
    for a in available:
        by_cat[a.get('category', 'Other')].append(a)

    cat_sections = ''
    for cat, cats in by_cat.items():
        cat_cards = '\n'.join(article_card(a, lang) for a in cats)
        cat_sections += f'''
    <section class="blog-category-section">
      <h2 class="blog-category-title">{cat}</h2>
      <div class="article-grid">{cat_cards}
      </div>
    </section>'''

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{tpl} | {t['siteName']}</title>
  <meta name="description" content="{"酚醛树脂配件领域专业博客" if lang=="zh" else "Expert knowledge on phenolic resin parts"}">
  <link rel="alternate" hreflang="zh" href="../../pages/zh/blog.html">
  <link rel="alternate" hreflang="en" href="../../pages/en/blog.html">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/style.css">
  <link rel="stylesheet" href="../../assets/css/blog.css">
</head>
<body>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-inner">
        <a href="../../{"index_en.html" if lang!="zh" else "index.html"}" class="navbar-brand">
          <div class="navbar-logo">L</div><span>{t['siteName']}</span>
        </a>
        <div class="navbar-nav">
          <a href="../../{"index_en.html" if lang!="zh" else "index.html"}">{t['home']}</a>
          <a href="blog.html" class="active">{t['blog']}</a>
          <a href="../../{"index_en.html" if lang!="zh" else "index.html"}#products">{t['products']}</a>
          <a href="../../{"index_en.html" if lang!="zh" else "index.html"}#contact">{t['contact']}</a>
        </div>
        <div class="navbar-right">
          <div class="lang-switcher"></div>
          <button class="hamburger"><span></span><span></span><span></span></button>
        </div>
      </div>
    </div>
    <div class="mobile-nav">
      <a href="../../{"index_en.html" if lang!="zh" else "index.html"}">{t['home']}</a>
      <a href="blog.html">{t['blog']}</a>
      <a href="../../{"index_en.html" if lang!="zh" else "index.html"}#products">{t['products']}</a>
      <a href="../../{"index_en.html" if lang!="zh" else "index.html"}#contact">{t['contact']}</a>
    </div>
  </nav>

  <main class="blog-main">
    <div class="container">
      <header class="blog-page-header">
        <h1 class="blog-page-title">{tpl}</h1>
        <p class="blog-page-desc">{"酚醛树脂配件领域专业内容，从入门到精通" if lang=="zh" else "Expert knowledge on phenolic resin parts"}</p>
      </header>
      <section class="all-articles">
        <div class="article-grid">{cards}
        </div>
      </section>
{cat_sections}
    </div>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand">
          <div class="footer-logo">L</div>
          <div>
            <div class="footer-site-name">{t['siteName']}</div>
            <div class="footer-author">{t.get('authorTitle', t.get('author', 'Liu'))}</div>
          </div>
        </div>
        <div class="footer-links">
          <a href="../../{"index_en.html" if lang!="zh" else "index.html"}">{t['home']}</a>
          <a href="blog.html">{t['blog']}</a>
          <a href="../../{"index_en.html" if lang!="zh" else "index.html"}#products">{t['products']}</a>
          <a href="../../{"index_en.html" if lang!="zh" else "index.html"}#contact">{t['contact']}</a>
        </div>
        <div class="footer-copy">&copy; {datetime.now().year} {t['siteName']}</div>
      </div>
    </div>
  </footer>
  <script src="../../assets/js/main.js"></script>
</body>
</html>'''

    out = BASE / 'pages' / lang / 'blog.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f'  [OK] pages/{lang}/blog.html ({len(html)//1024}KB)')


# ── Single article HTML ─────────────────────────
def build_article_html(data, lang):
    filepath = BASE / data[lang]
    if filepath.exists():
        return
    slug = data['slug']
    title = data.get(f'title{lang.capitalize()}') or data.get('title', '')
    cat = data.get('category', '')
    tags = data.get('tags', [])
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    rt = data.get('readtime', 8)
    excerpt = data.get('excerpt', '')
    t = T.get(lang, T['en'])

    # hreflang alternates
    hreflangs = '\n  '.join(
        f'<link rel="alternate" hreflang="{l}" href="../{l}/{slug}.html">'
        for l in ['zh', 'en'] if data.get(l)
    )

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {t['siteName']}</title>
  <meta name="description" content="{excerpt}">
  {hreflangs}
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Serif+SC:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/style.css">
  <link rel="stylesheet" href="../../assets/css/post.css">
</head>
<body>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-inner">
        <a href="../../{"index_en.html" if lang!="zh" else "index.html"}" class="navbar-brand">
          <div class="navbar-logo">L</div><span>{t['siteName']}</span>
        </a>
        <div class="navbar-nav">
          <a href="../../{"index_en.html" if lang!="zh" else "index.html"}">{t['home']}</a>
          <a href="../../pages/{lang}/blog.html">{t['blog']}</a>
          <a href="../../{"index_en.html" if lang!="zh" else "index.html"}#products">{t['products']}</a>
          <a href="../../{"index_en.html" if lang!="zh" else "index.html"}#contact">{t['contact']}</a>
        </div>
        <div class="navbar-right"><div class="lang-switcher"></div><button class="hamburger"><span></span><span></span><span></span></button></div>
      </div>
    </div>
    <div class="mobile-nav">
      <a href="../../{"index_en.html" if lang!="zh" else "index.html"}">{t['home']}</a>
      <a href="../../pages/{lang}/blog.html">{t['blog']}</a>
      <a href="../../{"index_en.html" if lang!="zh" else "index.html"}#products">{t['products']}</a>
      <a href="../../{"index_en.html" if lang!="zh" else "index.html"}#contact">{t['contact']}</a>
    </div>
  </nav>
  <main class="post-layout">
    <div class="container"><div class="post-grid">
      <article class="post-main">
        <header class="post-header">
          <div class="post-meta-top"><span class="post-category">{cat}</span><span class="post-date">{date}</span><span class="post-readtime">{"阅读约" if lang=="zh" else "Read for"} {rt} {"分钟" if lang=="zh" else "min"}</span></div>
          <h1 class="post-title">{title}</h1>
          <div class="post-author-row"><div class="post-author-avatar">L</div><div><div class="post-author-name">{t["author"]}</div><div class="post-author-bio">{"酚醛树脂配件十五年从业者" if lang=="zh" else "15 Years in Phenolic Resin Parts"}</div></div></div>
        </header>
        <div class="post-body">
          <p>{excerpt}</p>
          <p><em>{"内容由 AI 自动生成（提示：编辑此文件替换为实际内容）" if lang=="zh" else "Content auto-generated by AI. Replace with actual content."}</em></p>
        </div>
        <footer class="post-footer"><div class="post-tags">{"".join(f'<span class="post-tag">{tag}</span>' for tag in tags)}</div></footer>
      </article>
      <aside class="post-sidebar">
        <div class="sidebar-card"><div class="sidebar-card-title">{"博客目录" if lang=="zh" else "Blog Index"}</div><div class="sidebar-nav-list">
          <a href="01-phenolic-basics.html" class="sidebar-nav-item">{"酚醛树脂基础" if lang=="zh" else "Phenolic Resin Basics"}</a>
          <a href="02-material-selection.html" class="sidebar-nav-item">{"材料选择" if lang=="zh" else "Material Selection"}</a>
          <a href="03-mold-design.html" class="sidebar-nav-item">{"模具设计" if lang=="zh" else "Mold Design"}</a>
        </div></div>
      </aside>
    </div></div>
  </main>
  <footer class="site-footer"><div class="container"><div class="footer-inner"><div class="footer-brand"><div class="footer-logo">L</div><div><div class="footer-site-name">{t["siteName"]}</div><div class="footer-author">{"酚醛树脂配件十五年从业者" if lang=="zh" else "15 Years in Phenolic Resin Parts"}</div></div></div><div class="footer-copy">&copy; {datetime.now().year} {t["siteName"]}</div></div></div></footer>
  <script src="../../assets/js/main.js"></script>
</body>
</html>'''
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(html, encoding='utf-8')
    print(f'  [NEW] {filepath.relative_to(BASE)}')


# ── Index pages ────────────────────────────────
def build_index(articles, lang):
    """生成首页（zh=en 特殊处理，其他语种生成 lang/index.html）"""
    t = T.get(lang, T['en'])
    site_lang = 'zh' if lang == 'zh' else 'en'

    # Hero title (ZH has special chars, EN has different structure)
    if lang == 'zh':
        hero_title_html = '十年深耕，<br>专注酚醛树脂配件。'
    else:
        hero_title_html = "15 Years of Focus on<br>Phenolic Resin Parts."

    # News cards (top 6 articles with fallback)
    news_cards = '\n'.join(news_card(a, lang) for a in articles[:6] if a.get(lang) or a.get('en') or a.get('zh'))

    # Inject article list as JS (for main.js to render news dynamically)
    article_list_js = build_manifest_js(articles, lang)

    # Article list injection script tag
    article_inject = f'\n  <script>window.__ARTICLES__ = {article_list_js};</script>\n'

    # Index file path
    if lang == 'zh':
        index_path = BASE / 'index.html'
    elif lang == 'en':
        index_path = BASE / 'index_en.html'
    else:
        index_path = BASE / f'pages/{lang}/index.html'

    # Read existing index for zh/en to preserve structure
    if index_path.exists():
        html = index_path.read_text(encoding='utf-8')
        # Inject article list
        if '<script>window.__ARTICLES__' not in html:
            body_end = html.rfind('</body>')
            if body_end > 0:
                html = html[:body_end] + article_inject + html[body_end:]
        # Also update the news cards section
        news_patterns = [
            r'(<section[^>]*id=["\']news["\'][^>]*>.*?<div class=["\']news-grid["\']>)(.*?)(</div>\s*</section>)',
        ]
        for pat in news_patterns:
            m = re.search(pat, html, re.DOTALL)
            if m:
                html = html[:m.start(2)] + '\n' + news_cards + '\n        ' + html[m.end(2):]
                print(f'  [OK] news section updated in {index_path.name}')
                break
        index_path.write_text(html, encoding='utf-8')
        print(f'  [OK] {index_path.name} ({len(html)//1024}KB)')

    else:
        # Create simple index for other languages
        print(f'  [SKIP] {index_path} does not exist yet, creating...')
        simple_html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t['siteName']}</title>
  <meta name="description" content="{"酚醛树脂配件专业博客" if lang=="zh" else "Expert phenolic resin parts blog"}">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-inner">
        <a href="index.html" class="navbar-brand"><div class="navbar-logo">L</div><span>{t['siteName']}</span></a>
        <div class="navbar-nav">
          <a href="index.html" class="active">{t['home']}</a>
          <a href="pages/{lang}/blog.html">{t['blog']}</a>
        </div>
        <div class="navbar-right"><div class="lang-switcher"></div><button class="hamburger"><span></span><span></span><span></span></button></div>
      </div>
    </div>
  </nav>
  <section id="news" style="padding:80px 0;">
    <div class="container">
      <h2>{t['newsTitle']}</h2>
      <div class="news-grid">{news_cards}
      </div>
      <p><a href="pages/{lang}/blog.html">{t['newsAll']}</a></p>
    </div>
  </section>
  <script>window.__ARTICLES__ = {article_list_js};</script>
  <script src="../../assets/js/main.js"></script>
</body>
</html>'''
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(simple_html, encoding='utf-8')
        print(f'  [NEW] {index_path} ({len(simple_html)//1024}KB)')


# ── Sitemap ────────────────────────────────────
def build_sitemap(articles, base_url):
    today = datetime.now().strftime('%Y-%m-%d')
    urls = [
        {'loc': f'{base_url}/', 'prio': '1.0', 'freq': 'daily'},
        {'loc': f'{base_url}/pages/zh/blog.html', 'prio': '0.9', 'freq': 'weekly'},
        {'loc': f'{base_url}/pages/en/blog.html', 'prio': '0.9', 'freq': 'weekly'},
        {'loc': f'{base_url}/index_en.html', 'prio': '0.9', 'freq': 'weekly'},
    ]
    for a in articles:
        slug = a['slug']
        for lang, key in [('zh', 'zh'), ('en', 'en'), ('ja', 'ja'), ('ko', 'ko'),
                           ('ru', 'ru'), ('es', 'es'), ('fr', 'fr'), ('it', 'it'), ('th', 'th'), ('vi', 'vi')]:
            if a.get(key):
                urls.append({'loc': f'{base_url}/posts/{lang}/{a[key]}', 'prio': '0.7', 'freq': 'monthly', 'date': a.get('date', today)})

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        dt = f'<lastmod>{u.get("date", today)}</lastmod>' if 'date' in u else ''
        xml_lines.append(f'  <url><loc>{u["loc"]}</loc>{dt}<changefreq>{u["freq"]}</changefreq><priority>{u["prio"]}</priority></url>')
    xml_lines.append('</urlset>')

    (BASE / 'sitemap.xml').write_text('\n'.join(xml_lines), encoding='utf-8')
    print(f'  [OK] sitemap.xml ({len(urls)} URLs)')


# ── Feed ───────────────────────────────────────
def build_feed(articles, base_url, site_name):
    items = []
    for a in sorted(articles, key=lambda x: x.get('date', ''), reverse=True)[:15]:
        slug = a['slug']
        href = f'{base_url}/posts/zh/{a["zh"]}' if a.get('zh') else ''
        dt = datetime.strptime(a.get('date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').strftime('%a, %d %b %Y %H:%M:%S +0000')
        items.append(f'''  <item>
    <title><![CDATA[{a["title"]}]]></title>
    <link>{href}</link>
    <guid isPermaLink="true">{href}</guid>
    <pubDate>{dt}</pubDate>
    <description><![CDATA[{a.get("excerpt","")}]]></description>
    <category>{a.get("category","")}</category>
  </item>''')

    now = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{site_name}</title>
    <link>{base_url}</link>
    <description>酚醛树脂配件专业博客</description>
    <language>zh-cn</language>
    <lastBuildDate>{now}</lastBuildDate>
    <atom:link href="{base_url}/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>'''
    (BASE / 'feed.xml').write_text(xml, encoding='utf-8')
    print(f'  [OK] feed.xml')


# ── Language names (for hreflang) ─────────────
LANG_NAMES = {
    'zh': 'zh-CN', 'en': 'en-US', 'ja': 'ja-JP', 'ko': 'ko-KR',
    'ru': 'ru-RU', 'es': 'es-ES', 'fr': 'fr-FR', 'it': 'it-IT',
    'th': 'th-TH', 'vi': 'vi-VN',
}


# ── Main ───────────────────────────────────────
def main():
    print(f'\n--- Liu Blog Build v2 | {datetime.now().strftime("%Y-%m-%d %H:%M")} ---')

    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    articles = manifest['articles']
    site = manifest['site']
    base_url = site.get('baseUrl', 'https://liublog.example.com')

    print(f'\n[{len(articles)} articles loaded]\n')

    # 1. Generate blog pages for all langs
    print('=== Blog Listing Pages ===')
    for lang in LANGS:
        build_blog_page(articles, lang)

    # 2. Update index pages (zh + en use existing, others create simple)
    print('\n=== Index Pages ===')
    build_index(articles, 'zh')      # update existing index.html
    build_index(articles, 'en')      # update existing index_en.html
    # Other languages: build simple landing pages (no existing files to update)
    for lang in ['ja', 'ko', 'ru', 'es', 'fr', 'it', 'th', 'vi']:
        p = BASE / f'pages/{lang}/index.html'
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            # Create a simple landing page with news
            article_list_js = build_manifest_js(articles, lang)
            news_cards = '\n'.join(news_card(a, lang) for a in articles[:6]
                                   if a.get(lang) or a.get('en') or a.get('zh'))
            t = T.get(lang, T['en'])
            simple_html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t['siteName']}</title>
  <meta name="description" content="酚醛树脂配件专业博客">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-inner">
        <a href="index.html" class="navbar-brand"><div class="navbar-logo">L</div><span>{t['siteName']}</span></a>
        <div class="navbar-nav">
          <a href="index.html" class="active">{t['home']}</a>
          <a href="pages/{lang}/blog.html">{t['blog']}</a>
        </div>
        <div class="navbar-right"><div class="lang-switcher"></div><button class="hamburger"><span></span><span></span><span></span></button></div>
      </div>
    </div>
  </nav>
  <section id="news" style="padding:80px 0;background:#F4F6F8;">
    <div class="container">
      <h2 style="text-align:center;margin-bottom:40px;color:#1B4F72;">{t['newsTitle']}</h2>
      <div class="news-grid">{news_cards}
      </div>
      <p style="text-align:center;margin-top:32px;"><a href="pages/{lang}/blog.html" style="color:#C8882B;font-weight:600;">{t['newsAll']}</a></p>
    </div>
  </section>
  <script>window.__ARTICLES__ = {article_list_js};</script>
  <script src="../../assets/js/main.js"></script>
</body>
</html>'''
            p.write_text(simple_html, encoding='utf-8')
            print(f'  [NEW] pages/{lang}/index.html ({len(simple_html)//1024}KB)')

    # 3. Generate new article stubs (for missing zh/en articles)
    print('\n=== Article Stubs ===')
    for a in articles:
        for lang in ['zh', 'en']:
            if a.get(lang):
                build_article_html(a, lang)

    # 4. SEO
    print('\n=== SEO ===')
    build_sitemap(articles, base_url)
    build_feed(articles, base_url, site.get('name', "刘的博客"))

    print(f'\nDone. {datetime.now().strftime("%H:%M:%S")}')


if __name__ == '__main__':
    main()
