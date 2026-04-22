#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
刘的博客 · 自动化构建脚本
用法:
  python build.py              # 生成所有页面（默认）
  python build.py --article    # 生成首页/列表页（不改文章）
  python build.py --init       # 初始化新文章模板（需配合 --id 参数）

工作流程：
  1. 读取 manifest.json（单一数据源）
  2. 生成/更新 posts/zh/ 和 posts/en/ 下的文章 HTML
  3. 生成 pages/zh/blog.html 和 pages/en/blog.html
  4. 更新 index.html 和 index_en.html 中的行业资讯区块
  5. 生成 sitemap.xml 和 feed.xml（SEO）
"""

import json, re, os, sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.resolve()
MANIFEST = BASE / "manifest.json"
OUTPUT_DIR = BASE

# ──────────────────────────────────────────────
# 辅助：渲染 HTML 片段
# ──────────────────────────────────────────────

def article_card(data, lang="zh", size=8):
    """生成文章卡片 HTML"""
    slug = data["slug"]
    href = f'posts/{lang}/{data[lang] or data["en"] or "index.html"}' if data.get(lang) or data.get("en") else "#"
    if href.endswith(".html") and not os.path.exists(BASE / href):
        href = "#"
    category = data.get("category", "")
    date = data.get("date", "")
    readtime = data.get("readtime", 8)
    excerpt = data.get("excerpt", "")
    title = data.get(f"titleEn") if lang != "zh" and data.get(f"titleEn") else data.get("title", "")

    return f'''
    <a href="../../{href}" class="article-card">
      <div class="article-card-inner">
        <div class="article-card-meta">
          <span class="article-card-category">{category}</span>
          <span class="article-card-date">{date}</span>
        </div>
        <h3 class="article-card-title">{title}</h3>
        <p class="article-card-excerpt">{excerpt}</p>
        <div class="article-card-footer">
          <span class="article-card-readtime">阅读约 {readtime} 分钟</span>
          <span class="article-card-arrow">→</span>
        </div>
      </div>
    </a>'''

def news_card(data, lang="zh"):
    """生成首页行业资讯小卡片"""
    slug = data["slug"]
    href = f'posts/{lang}/{data[lang] or data["en"] or "index.html"}' if data.get(lang) or data.get("en") else "#"
    if href.endswith(".html") and not os.path.exists(BASE / href):
        href = "#"
    category = data.get("category", "")
    date = data.get("date", "")
    readtime = data.get("readtime", 8)
    title = data.get(f"titleEn") if lang != "zh" and data.get(f"titleEn") else data.get("title", "")
    excerpt = data.get("excerpt", "")

    return f'''
        <a href="{href}" class="news-card">
          <div class="news-card-meta">
            <span class="news-card-category">{category}</span>
            <span class="news-card-date">{date}</span>
          </div>
          <h3 class="news-card-title">{title}</h3>
          <p class="news-card-excerpt">{excerpt[:60]}…</p>
          <span class="news-card-cta">阅读 {readtime}min →</span>
        </a>'''


# ──────────────────────────────────────────────
# 生成博客列表页 pages/zh/blog.html / pages/en/blog.html
# ──────────────────────────────────────────────

def build_blog_page(articles, lang="zh"):
    """生成完整的博客列表页（包含 header + 文章网格 + footer）"""
    site_title = "刘的博客" if lang == "zh" else "Liu's Blog"
    blog_title = "全部文章" if lang == "zh" else "All Articles"

    # 按分类分组
    from collections import defaultdict
    by_cat = defaultdict(list)
    for a in articles:
        cat = a.get("category", "未分类")
        by_cat[cat].append(a)

    # 文章卡片（全部）
    all_cards = "\n".join(
        article_card(a, lang) for a in articles
        if a.get(lang) or a.get("en")
    )

    # 分类小节
    category_sections = ""
    for cat, cats in by_cat.items():
        cat_cards = "\n".join(
            article_card(a, lang) for a in cats
            if a.get(lang) or a.get("en")
        )
        category_sections += f'''
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
  <title>{blog_title} | {site_title}</title>
  <meta name="description" content="{"刘的博客全部文章，涵盖酚醛树脂配件入门、选型指南、技术深潜、行业观察等。" if lang == "zh" else "All articles on phenolic resin parts, technical guides and industry insights."}">
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
        <a href="../../index.html" class="navbar-brand">
          <div class="navbar-logo">L</div>
          <span>{site_title}</span>
        </a>
        <div class="navbar-nav">
          <a href="../../index.html">首页</a>
          <a href="blog.html" class="active">博客</a>
          <a href="../../index.html#products">产品</a>
          <a href="../../index.html#contact">联系</a>
        </div>
        <div class="navbar-right">
          <div class="lang-switcher"></div>
          <button class="hamburger"><span></span><span></span><span></span></button>
        </div>
      </div>
    </div>
    <div class="mobile-nav">
      <a href="../../index.html">首页</a>
      <a href="blog.html">博客</a>
      <a href="../../index.html#products">产品</a>
      <a href="../../index.html#contact">联系</a>
    </div>
  </nav>

  <main class="blog-main">
    <div class="container">
      <header class="blog-page-header">
        <h1 class="blog-page-title">{blog_title}</h1>
        <p class="blog-page-desc">{"酚醛树脂配件领域专业内容，从入门到精通" if lang == "zh" else "Expert knowledge on phenolic resin parts"}</p>
      </header>

      <section class="all-articles">
        <h2 class="visually-hidden">{"全部文章" if lang == "zh" else "All Articles"}</h2>
        <div class="article-grid">{all_cards}
        </div>
      </section>

{category_sections}
    </div>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand">
          <div class="footer-logo">L</div>
          <div>
            <div class="footer-site-name">{site_title}</div>
            <div class="footer-author">{"酚醛树脂配件十五年从业者" if lang == "zh" else "15 Years in Phenolic Resin Parts"}</div>
          </div>
        </div>
        <div class="footer-links">
          <a href="../../index.html">{"首页" if lang == "zh" else "Home"}</a>
          <a href="blog.html">{"博客" if lang == "zh" else "Blog"}</a>
          <a href="../../index.html#products">{"产品" if lang == "zh" else "Products"}</a>
          <a href="../../index.html#contact">{"联系" if lang == "zh" else "Contact"}</a>
        </div>
        <div class="footer-copy">
          &copy; {datetime.now().year} {site_title} · {"华玲机械" if lang == "zh" else "Hualing Machinery"}
        </div>
      </div>
    </div>
  </footer>

  <script src="../../assets/js/main.js"></script>
</body>
</html>'''

    out_path = OUTPUT_DIR / f"pages/{lang}/blog.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✅ {out_path.relative_to(BASE)}")


# ──────────────────────────────────────────────
# 更新首页行业资讯区块
# ──────────────────────────────────────────────

def update_index_news(articles, lang="zh"):
    """找到并替换 index.html 中 id="news" 区块的内容"""
    index_file = OUTPUT_DIR / ("index_en.html" if lang != "zh" else "index.html")

    # 读取现有首页
    html = index_file.read_text(encoding="utf-8")

    # 生成新内容
    featured = [a for a in articles if a.get(lang) or a.get("en")]
    if not featured:
        return
    top3 = featured[:3]
    cards = "\n".join(news_card(a, lang) for a in top3)

    # 在 html 中找 <section id="news"> 或类似区块
    # 先尝试找包含 news 或 行业资讯 的 section
    patterns = [
        r'(<section[^>]*id=["\']news["\'][^>]*>)(.*?)(</section>)',
        r'(<section[^>]*id=["\']articles["\'][^>]*>)(.*?)(</section>)',
        r'(<section[^>]*class=["\'][^"\']*news[^"\']*["\'][^>]*>)(.*?)(</section>)',
        r'(<section[^>]*class=["\'][^"\']*articles[^"\']*["\'][^>]*>)(.*?)(</section>)',
    ]
    replaced = False
    for pat in patterns:
        m = re.search(pat, html, re.DOTALL)
        if m:
            new_block = m.group(1) + "\n          <div class=\"news-grid\">" + cards + "\n          </div>\n        " + m.group(3)
            html = html[:m.start()] + new_block + html[m.end():]
            print(f"  ✅ 首页 [{lang}] news section updated via pattern: {pat[:50]}")
            replaced = True
            break

    if not replaced:
        # fallback: 找 <!-- NEWS_START --> 和 <!-- NEWS_END --> 注释
        start_marker = "<!-- NEWS_START -->"
        end_marker = "<!-- NEWS_END -->"
        if start_marker in html and end_marker in html:
            s = html.find(start_marker) + len(start_marker)
            e = html.find(end_marker)
            html = html[:s] + "\n          <div class=\"news-grid\">" + cards + "\n          </div>\n        " + html[e:]
            print(f"  ✅ 首页 [{lang}] news section updated via markers")
            replaced = True

    if not replaced:
        print(f"  ⚠️  首页 [{lang}] — 未找到 news 区块，无法自动更新。请手动添加标记：")
        print(f"     在 <section> 标签里添加 <!-- NEWS_START -->...<!-- NEWS_END -->")

    index_file.write_text(html, encoding="utf-8")


# ──────────────────────────────────────────────
# 生成 sitemap.xml
# ──────────────────────────────────────────────

def build_sitemap(articles, site):
    base = site.get("baseUrl", "https://liublog.example.com")
    today = datetime.now().strftime("%Y-%m-%d")

    urls = [
        {"loc": base + "/", "priority": "1.0", "changefreq": "daily"},
        {"loc": base + "/pages/zh/blog.html", "priority": "0.9", "changefreq": "weekly"},
        {"loc": base + "/pages/en/blog.html", "priority": "0.9", "changefreq": "weekly"},
        {"loc": base + "/index_en.html", "priority": "0.9", "changefreq": "weekly"},
    ]
    for a in articles:
        slug = a["slug"]
        if a.get("zh"):
            urls.append({"loc": f"{base}/posts/zh/{slug}.html", "priority": "0.8", "changefreq": "monthly", "date": a.get("date", today)})
        if a.get("en"):
            urls.append({"loc": f"{base}/posts/en/{slug}.html", "priority": "0.8", "changefreq": "monthly", "date": a.get("date", today)})

    url_tags = []
    for u in urls:
        dt = u.get("date", today)
        date_tag = f'<lastmod>{dt}</lastmod>' if dt else ''
        url_tags.append(
            f'  <url>\n    <loc>{u["loc"]}</loc>\n    {date_tag}\n'
            f'    <changefreq>{u["changefreq"]}</changefreq>\n'
            f'    <priority>{u["priority"]}</priority>\n  </url>'
        )

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(url_tags)}
</urlset>'''

    out = OUTPUT_DIR / "sitemap.xml"
    out.write_text(xml, encoding="utf-8")
    print(f"  ✅ sitemap.xml")


# ──────────────────────────────────────────────
# 生成 RSS feed
# ──────────────────────────────────────────────

def build_feed(articles, site):
    base = site.get("baseUrl", "https://liublog.example.com")
    name = site.get("name", "刘的博客")
    today = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    items = []
    for a in sorted(articles, key=lambda x: x.get("date", ""), reverse=True)[:10]:
        slug = a["slug"]
        href_zh = f"{base}/posts/zh/{slug}.html" if a.get("zh") else ""
        href_en = f"{base}/posts/en/{slug}.html" if a.get("en") else ""
        dt = datetime.strptime(a.get("date", today), "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S +0000")
        items.append(f'''  <item>
    <title>{a["title"]}</title>
    <link>{href_zh}</link>
    <guid isPermaLink="true">{href_zh}</guid>
    <pubDate>{dt}</pubDate>
    <description><![CDATA[{a.get("excerpt", "")}]]></description>
    <category>{a.get("category", "")}</category>
  </item>''')

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{name}</title>
    <link>{base}</link>
    <description>{"酚醛树脂配件领域专业博客" if "酚醛" in name else name}</description>
    <language>{"zh-cn" if site.get("lang") == "zh" else "en-us"}</language>
    <lastBuildDate>{today}</lastBuildDate>
    <atom:link href="{base}/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>'''

    out = OUTPUT_DIR / "feed.xml"
    out.write_text(xml, encoding="utf-8")
    print(f"  ✅ feed.xml")


# ──────────────────────────────────────────────
# 生成单篇文章 HTML（从模板）
# ──────────────────────────────────────────────

def build_article(article_data, lang="zh"):
    """生成单篇文章页面（如果文件不存在，则从模板生成）"""
    filepath = OUTPUT_DIR / article_data[lang]
    if filepath.exists():
        return  # 已有文章不覆盖

    a = article_data
    title = a.get("title", "") if lang == "zh" else a.get("titleEn", a.get("title", ""))
    category = a.get("category", "")
    tags = a.get("tags", [])
    date = a.get("date", datetime.now().strftime("%Y-%m-%d"))
    readtime = a.get("readtime", 8)
    excerpt = a.get("excerpt", "")
    slug = a.get("slug", "")

    # hreflang alternates
    hreflangs = f'''
  <link rel="alternate" hreflang="zh" href="../zh/{slug}.html">
  <link rel="alternate" hreflang="en" href="../en/{slug}.html">
  <link rel="alternate" hreflang="x-default" href="../en/{slug}.html">'''

    body_content = f'''
      <div class="post-body">
        <p>{excerpt}</p>
        <p><em>{"内容待生成（AI写作入口）" if lang == "zh" else "Content to be generated by AI"}</em></p>
      </div>'''

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {"刘的博客" if lang == "zh" else "Liu's Blog"}</title>
  <meta name="description" content="{excerpt}">
{hreflangs}
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Serif+SC:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/style.css">
  <link rel="stylesheet" href="../../assets/css/post.css">
</head>
<body>
  <nav class="navbar"><div class="container"><div class="navbar-inner"><a href="../../index.html" class="navbar-brand"><div class="navbar-logo">L</div><span>{"刘的博客" if lang == "zh" else "Liu's Blog"}</span></a><div class="navbar-nav"><a href="../../index.html">{"首页" if lang == "zh" else "Home"}</a><a href="../../pages/zh/blog.html">{"博客" if lang == "zh" else "Blog"}</a><a href="../../index.html#products">{"产品" if lang == "zh" else "Products"}</a><a href="../../index.html#contact">{"联系" if lang == "zh" else "Contact"}</a></div><div class="navbar-right"><div class="lang-switcher"></div><button class="hamburger"><span></span><span></span><span></span></button></div></div></div><div class="mobile-nav"><a href="../../index.html">{"首页" if lang == "zh" else "Home"}</a><a href="../../pages/zh/blog.html">{"博客" if lang == "zh" else "Blog"}</a><a href="../../index.html#products">{"产品" if lang == "zh" else "Products"}</a><a href="../../index.html#contact">{"联系" if lang == "zh" else "Contact"}</a></div></nav>

  <main class="post-layout"><div class="container"><div class="post-grid">
    <article class="post-main">
      <header class="post-header">
        <div class="post-meta-top"><span class="post-category">{category}</span><span class="post-date">{date}</span><span class="post-readtime">{"阅读约" if lang == "zh" else "Read for"} {readtime} {"分钟" if lang == "zh" else "min"}</span></div>
        <h1 class="post-title">{title}</h1>
        <div class="post-author-row"><div class="post-author-avatar">{"刘" if lang == "zh" else "L"}</div><div><div class="post-author-name">{"刘" if lang == "zh" else "Liu"}</div><div class="post-author-bio">{"酚醛树脂配件十五年从业者" if lang == "zh" else "15 Years in Phenolic Resin Parts"}</div></div></div>
      </header>
{body_content}
      <footer class="post-footer"><div class="post-tags">{"".join(f'<span class="post-tag">{t}</span>' for t in tags)}</div></footer>
    </article>
    <aside class="post-sidebar">
      <div class="sidebar-card"><div class="sidebar-card-title">{"博客目录" if lang == "zh" else "Blog Index"}</div><div class="sidebar-nav-list">
        <a href="01-phenolic-basics.html" class="sidebar-nav-item">{"酚醛树脂基础知识" if lang == "zh" else "Phenolic Resin Basics"}</a>
        <a href="02-material-selection.html" class="sidebar-nav-item">{"材料选择指南" if lang == "zh" else "Material Selection Guide"}</a>
        <a href="03-mold-design.html" class="sidebar-nav-item">{"模具设计要点" if lang == "zh" else "Mold Design"}</a>
      </div></div>
      <div class="sidebar-card"><div class="sidebar-card-title">{"分享文章" if lang == "zh" else "Share"}</div><div class="sidebar-share-btns"><button class="sidebar-share-btn" onclick="navigator.share({{title:document.title,url:location.href}})">{"分享" if lang == "zh" else "Share"}</button></div></div>
    </aside>
  </div></div></main>

  <footer class="site-footer"><div class="container"><div class="footer-inner"><div class="footer-brand"><div class="footer-logo">L</div><div><div class="footer-site-name">{"刘的博客" if lang == "zh" else "Liu's Blog"}</div><div class="footer-author">{"酚醛树脂配件十五年从业者" if lang == "zh" else "15 Years in Phenolic Resin Parts"}</div></div></div><div class="footer-links"><a href="../../index.html">{"首页" if lang == "zh" else "Home"}</a><a href="../../pages/zh/blog.html">{"博客" if lang == "zh" else "Blog"}</a><a href="../../index.html#products">{"产品" if lang == "zh" else "Products"}</a><a href="../../index.html#contact">{"联系" if lang == "zh" else "Contact"}</a></div><div class="footer-copy">&copy; {datetime.now().year} {"刘的博客 · 华玲机械" if lang == "zh" else "Liu's Blog · Hualing Machinery"}</div></div></div></footer>

  <script src="../../assets/js/main.js"></script>
</body>
</html>'''

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(html, encoding="utf-8")
    print(f"  ✅ Created: {filepath.relative_to(BASE)}  ({'ZH' if lang=='zh' else 'EN'})")


# ──────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────

def main():
    mode = "full"
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    print(f"\n🔧 刘的博客 Build Script — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    articles = manifest["articles"]
    site = manifest["site"]

    print(f"\n📋 Manifest loaded: {len(articles)} articles")

    if mode == "--init":
        # 生成新文章模板
        next_id = str(max(int(a["id"]) for a in articles) + 1).zfill(2)
        slug = input(f"Article slug (e.g. my-new-topic): ").strip()
        title = input(f"Title (ZH): ").strip()
        title_en = input(f"Title (EN): ").strip()
        category = input(f"Category [入门手册/技术深潜/行业观察/选型指南]: ").strip() or "行业观察"
        tags = input(f"Tags (comma-separated): ").strip()
        excerpt = input(f"Excerpt: ").strip()
        new_article = {
            "id": next_id,
            "slug": slug,
            "title": title,
            "titleEn": title_en,
            "category": category,
            "tags": [t.strip() for t in tags.split(",")],
            "date": datetime.now().strftime("%Y-%m-%d"),
            "readtime": 8,
            "excerpt": excerpt,
            "zh": f"posts/zh/{next_id}-{slug}.html",
            "en": None,
            "ja": None,
            "ko": None,
            "featured": False
        }
        articles.append(new_article)
        manifest["articles"] = articles
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        build_article(new_article, "zh")
        print(f"\n✅ Template created! Now edit posts/zh/{next_id}-{slug}.html with actual content.")
        print(f"   Then run: python build.py --article")
        return

    # 1. 生成文章（仅不存在的新文章）
    print("\n📝 Article files...")
    zh_count = en_count = 0
    for a in articles:
        if a.get("zh"):
            build_article(a, "zh")
            zh_count += 1
        if a.get("en"):
            build_article(a, "en")
            en_count += 1
    print(f"   Articles: {zh_count} ZH, {en_count} EN")

    # 2. 生成博客列表页
    print("\n📄 Blog listing pages...")
    build_blog_page(articles, "zh")
    build_blog_page(articles, "en")

    # 3. 更新首页行业资讯
    print("\n🏠 Updating index pages...")
    update_index_news(articles, "zh")
    update_index_news(articles, "en")

    # 4. SEO 文件
    print("\n🔍 SEO files...")
    build_sitemap(articles, site)
    build_feed(articles, site)

    print(f"\n✅ Build complete! {datetime.now().strftime('%H:%M:%S')}")
    print(f"   Run `python build.py --init` to add a new article interactively.")
    print(f"   Run `python build.py --article` after manually editing article HTML files.")


if __name__ == "__main__":
    main()
