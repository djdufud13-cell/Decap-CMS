"""
第十轮：接入Google Analytics + Search Console + 部署Decap CMS后台
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import shutil
import re

base = Path(r'C:\Users\Administrator\.qclaw\workspace\liu-blog')

print("=" * 60)
print("第十轮：数据分析 + CMS后台")
print("=" * 60)

# ============================================================
# PART 1: Google Analytics + Search Console
# ============================================================
print("\n📊 PART 1: 数据分析接入\n")

# 【需要用户填入自己的ID】
GA_MEASUREMENT_ID = "G-XXXXXXXXXX"   # ← 替换为你的 GA4 Measurement ID
GSC_VERIFICATION = "XXXXXXXXXXXXXXXXXXXXXXXX"  # ← 替换为你的 Search Console 验证码

GA_SCRIPT = f"""
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA_MEASUREMENT_ID}');
  </script>
"""

GSC_META = f'\n  <meta name="google-site-verification" content="{GSC_VERIFICATION}">\n'

# 找到所有HTML文件（排除admin目录）
html_files = []
for f in base.rglob("*.html"):
    if "admin" not in str(f) and ".corrupted" not in str(f):
        html_files.append(f)

print(f"  扫描到 {len(html_files)} 个HTML文件")

# 插入GA脚本到<head>末尾
# 插入GSC meta到<head>
inserted_ga = 0
inserted_gsc = 0

for f in html_files:
    content = f.read_text(encoding='utf-8')
    modified = False

    # 检查是否已有GA
    if 'googletagmanager.com/gtag/js' not in content:
        # 找到</head>位置
        if '</head>' in content:
            content = content.replace('</head>', GA_SCRIPT + '\n</head>', 1)
            modified = True
            inserted_ga += 1

    # 检查是否已有GSC
    if 'google-site-verification' not in content:
        if '</head>' in content:
            content = content.replace('</head>', GSC_META + '</head>', 1)
            modified = True
            inserted_gsc += 1

    if modified:
        f.write_text(content, encoding='utf-8')

print(f"  ✅ GA脚本: 已插入 {inserted_ga} 个文件")
print(f"  ✅ GSC验证: 已插入 {inserted_gsc} 个文件")

# ============================================================
# PART 2: Decap CMS 后台
# ============================================================
print("\n🛠️ PART 2: Decap CMS 后台部署\n")

admin_dir = base / "admin"
admin_dir.mkdir(exist_ok=True)

# 2a. admin/index.html
admin_html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>刘的博客 - 内容管理</title>
  <!-- Decap CMS -->
  <script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"></script>
  <style>
    /* 匹配博客暖橙配色 */
    .css-1m3lUt { --color-primary: #E87722 !important; }
    body { font-family: 'Noto Sans SC', 'PingFang SC', sans-serif; }
  </style>
</head>
<body>
  <!-- Decap CMS会自动加载config.yml -->
</body>
</html>
"""

# 2b. admin/config.yml - 完整内容配置
config_yml = """# Decap CMS 配置
# 刘的博客 - 内容管理系统
#
# 【重要】部署说明：
#   方案A - 使用GitHub后端（推荐）：
#     1. 把整个liu-blog项目push到GitHub仓库
#     2. 在Netlify/Vercel连接该仓库并开启Identity功能
#     3. 把下面的 backend.type 改为 "netlify"
#     4. 发布网站后就可以通过 /admin/ 管理内容了
#
#   方案B - 使用本地后端（仅测试）：
#     当前设置为 local 后端，可在本地预览
#     真实部署时需要改用GitHub后端
#
# 【内容更新后】
#   每次在CMS中发布内容后，需要：
#   1. 本地更新文件（CMS会自动写回）
#   2. 重新生成HTML页面（运行 build.py）
#   3. 提交到GitHub自动部署

backend:
  name: local
  # ↓↓↓ 换成GitHub后端时使用这个配置 ↓↓↓ #
  # name: git-gateway
  # repo: your-username/liu-blog        # 改为你的GitHub仓库
  # branch: main
  # site_domain: liublog.example.com    # 改为你的域名

local_backend: true   # 允许本地预览（仅测试用）

# ============================================================
# 媒体文件设置
# ============================================================
media_folder: "assets/images"
public_folder: "/assets/images"

# ============================================================
# 博客文章集合
# ============================================================
collections:

  # ── 中文博客文章 ──
  - name: "posts-zh"
    label: "中文文章"
    label_singular: "中文文章"
    folder: "posts/zh"
    create: true
    slug: "{{slug}}"
    extension: html
    format: html
    fields:
      - { label: "标题", name: "title", widget: "string" }
      - { label: "发布日期", name: "date", widget: "datetime", format: "YYYY-MM-DD" }
      - { label: "作者", name: "author", widget: "string", default: "刘工" }
      - { label: "摘要", name: "excerpt", widget: "text" }
      - { label: "标签（用逗号分隔）", name: "tags", widget: "string", default: "" }
      - { label: "封面图片", name: "cover", widget: "image", required: false }
      - { label: "文章内容（HTML）", name: "body", widget: "markdown" }

  # ── 英文博客文章 ──
  - name: "posts-en"
    label: "English Posts"
    label_singular: "English Post"
    folder: "posts/en"
    create: true
    slug: "{{slug}}"
    extension: html
    format: html
    fields:
      - { label: "Title", name: "title", widget: "string" }
      - { label: "Date", name: "date", widget: "datetime", format: "YYYY-MM-DD" }
      - { label: "Author", name: "author", widget: "string", default: "Liu" }
      - { label: "Excerpt", name: "excerpt", widget: "text" }
      - { label: "Tags (comma separated)", name: "tags", widget: "string", default: "" }
      - { label: "Cover Image", name: "cover", widget: "image", required: false }
      - { label: "Content (HTML)", name: "body", widget: "markdown" }

  # ── 新闻资讯 ──
  - name: "news"
    label: "新闻资讯"
    label_singular: "新闻"
    folder: "news"
    create: true
    slug: "{{slug}}"
    extension: html
    format: html
    fields:
      - { label: "标题", name: "title", widget: "string" }
      - { label: "发布日期", name: "date", widget: "datetime", format: "YYYY-MM-DD" }
      - { label: "类型", name: "type", widget: "select", options: ["行业新闻", "技术动态", "产品发布", "展会信息"] }
      - { label: "摘要", name: "excerpt", widget: "text" }
      - { label: "内容", name: "body", widget: "markdown" }
      - { label: "来源", name: "source", widget: "string", required: false }
"""

# 2c. 创建 news 目录
news_dir = base / "news"
news_dir.mkdir(exist_ok=True)

# 2d. 创建示例文章
sample_news_zh = """---
title: 酚醛树脂市场2026年持续增长
date: 2026-04-18
type: 行业新闻
excerpt: 全球酚醛树脂市场预计将在2026年达到新的高度，受益于汽车轻量化和电子电气行业的快速发展。
source: 华玲机械整理
---
# 酚醛树脂市场动态

酚醛树脂作为一种重要的热固性塑料，在汽车、电子电气、机械设备等领域有着广泛应用...

<!--more-->
"""

sample_news_en = """---
title: Phenolic Resin Market Continues Growth in 2026
date: 2026-04-18
type: Industry News
excerpt: The global phenolic resin market is expected to reach new heights in 2026, driven by automotive lightweighting and rapid development in electrical electronics.
source: Liu's Blog
---
# Phenolic Resin Market Update

Phenolic resin, as an important thermosetting plastic, has wide applications...

<!--more-->
"""

# 写入文件
admin_index = admin_dir / "index.html"
admin_config = admin_dir / "config.yml"

admin_index.write_text(admin_html, encoding='utf-8')
admin_config.write_text(config_yml, encoding='utf-8')

# 示例新闻
(sample_news_zh).encode('utf-8')
zh_news = news_dir / "2026-04-18-market-growth.html"
zh_news.write_text(sample_news_zh, encoding='utf-8')

en_news = news_dir / "2026-04-18-market-growth.html"
en_news.write_text(sample_news_en, encoding='utf-8')

# 2e. admin/README.md - 部署说明
readme_content = """# 刘的博客 - CMS后台说明

## 🏠 本地预览CMS

1. 安装 Node.js（如果还没装）
2. 进入 admin 目录：`cd admin`
3. 启动本地后端：`npx decap-server`（保持运行）
4. 用浏览器打开：`http://localhost:8080/admin/`
5. 你就可以在浏览器里管理文章了！

## 🚀 生产部署（推荐：Netlify）

### 步骤1：推送到GitHub
```bash
cd liu-blog
git init
git add .
git commit -m "刘的博客 - 初始版本"
git branch -M main
git remote add origin https://github.com/你的用户名/liu-blog.git
git push -u origin main
```

### 步骤2：在Netlify部署
1. 打开 https://netlify.com
2. 用GitHub登录
3. 点击 "Add new site" → "Import an existing project"
4. 选择你的GitHub仓库
5. 构建设置：
   - **Build command**: `python build.py`（可选，如果你的build.py是静态生成的话）
   - **Publish directory**: `.`（根目录）
6. 点击 "Deploy"

### 步骤3：开启Identity
1. 在Netlify后台 → Site settings → Identity
2. 点击 "Enable Identity"
3. Registration → Invite only（只允许你邀请的人）
4. 给你的邮箱发邀请链接

### 步骤4：更新CMS配置
把 `admin/config.yml` 中的 backend 改为：
```yaml
backend:
  name: git-gateway
  repo: 你的用户名/liu-blog
  branch: main
```

### 步骤5：配置正式域名
1. Netlify后台 → Domain management → Add custom domain
2. 添加你的域名（如 liublog.com）
3. 配置SSL证书（Netlify自动申请）
4. 更新CMS的 `site_domain`

## 📱 日常使用

### 发布文章流程
1. 打开 `你的域名/admin/`
2. 用邮箱登录
3. 点击 "中文文章" 或 "English Posts"
4. 点击 "New 中文文章"
5. 填写标题、内容、标签
6. 点击 "Publish"
7. Netlify自动构建并发布！

### AI自动生成内容
配合 content-factory skill，可以实现：
- 自动抓取行业新闻 → 生成摘要
- 批量生成多语言文章
- 定时更新内容

## 📊 接入数据分析

### Google Analytics
1. 打开 https://analytics.google.com
2. 创建账号 → 创建媒体资源
3. 获取 Measurement ID（如 G-XXXXXXXXXX）
4. 替换 `index.html` 和 `index_en.html` 中的 `G-XXXXXXXXXX`

### Google Search Console
1. 打开 https://search.google.com/search-console
2. 添加你的网站域名
3. 选择"HTML标记"验证方式
4. 复制验证码，替换文件中的 `XXXXXXXXXXXXXXXXXXXXXXXX`
"""

readme_file = admin_dir / "README.md"
readme_file.write_text(readme_content, encoding='utf-8')

# ============================================================
# PART 3: 更新 build.py 使其支持文章列表
# ============================================================
print("\n🔨 PART 3: 更新构建脚本支持CMS文章列表\n")

build_py = base / "build.py"
if build_py.exists():
    build_content = build_py.read_text(encoding='utf-8')
    # 添加posts列表更新功能
    if "POSTS_ZH" not in build_content:
        print("  ℹ️ build.py 已存在，将在后续完善")
    else:
        print("  ℹ️ build.py 已包含POSTS逻辑")

# ============================================================
# PART 4: 生成部署清单
# ============================================================
print("\n✅ 部署完成！\n")

print("=" * 60)
print("📋 部署清单")
print("=" * 60)
print("""
已创建的文件：
  ✅ admin/index.html          — CMS管理后台入口
  ✅ admin/config.yml          — CMS内容配置
  ✅ admin/README.md            — 详细部署说明
  ✅ news/2026-04-18-*.html    — 示例新闻文章

已插入到所有HTML文件：
  ✅ Google Analytics (gtag.js)
  ✅ Google Search Console 验证标签

============================================================
⚠️  接下来你需要做的（第1步）：
============================================================

1️⃣  获取 Google Analytics Measurement ID
    → https://analytics.google.com → 创建账号 → 获取 G-XXXXXXXXXX

2️⃣  获取 Google Search Console 验证码
    → https://search.google.com/search-console → 添加网站 → HTML标签

3️⃣  替换代码中的占位符
    → index.html 和 index_en.html 中的：
      G-XXXXXXXXXX → 你的GA ID
      XXXXXXXXXXXXXXXXXX → 你的GSC验证码

4️⃣  本地预览CMS（可选）
    → cd admin
    → npx decap-server
    → 浏览器打开 http://localhost:8080/admin/

5️⃣  部署到GitHub + Netlify（推荐）
    → 查看 admin/README.md 的详细步骤

============================================================
""")
