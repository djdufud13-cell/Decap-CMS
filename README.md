# 刘的博客 · 内容维护手册

## 核心原则：一切以 `manifest.json` 为数据源

**不要直接修改 `index.html`、`pages/zh/blog.html`、`index_en.html`**  
这三个文件由 `build.py` 自动生成，每次运行会自动更新文章列表和行业资讯区块。

---

## 方法一：手动添加新文章（最简单）

### 第一步：写文章
在 `posts/zh/` 目录下创建新 HTML 文件，命名规范：

```
posts/zh/07-my-topic.html
posts/en/07-my-topic.html   ← 英文版（可选）
```

参考现有文章的结构（参考 `posts/zh/04-quality-control.html`）。

### 第二步：注册到 manifest.json

打开 `manifest.json`，在 `articles` 数组末尾添加：

```json
{
  "id": "07",
  "slug": "my-topic",
  "title": "你的文章标题",
  "titleEn": "Your Article Title in English",
  "category": "行业观察",
  "tags": ["标签1", "标签2"],
  "date": "2026-04-16",
  "readtime": 8,
  "excerpt": "文章摘要，控制在100字以内",
  "zh": "posts/zh/07-my-topic.html",
  "en": "posts/en/07-my-topic.html",
  "featured": false
}
```

### 第三步：运行构建脚本

```
python build.py
```

**自动完成的事情：**
- ✅ `pages/zh/blog.html` — 博客列表页自动出现新文章
- ✅ `pages/en/blog.html` — 英文列表页自动更新
- ✅ `index.html` — 首页行业资讯区块自动更新（显示最新3篇）
- ✅ `sitemap.xml` — 百度/Google SEO 自动收录
- ✅ `feed.xml` — RSS 订阅源更新

---

## 方法二：让 AI 自动写作（推荐）

直接把下面的提示词发给 AI 助手即可：

```
帮我写一篇关于 [你的主题] 的博客文章。

要求：
1. 标题：[建议的标题]
2. 分类：从"入门手册"、"技术深潜"、"行业观察"、"选型指南"中选一个
3. 包含3~5个带小标题的章节，内容专业实用
4. 结尾有 CTA（引导联系华玲机械）
5. 语言风格：专业但不晦涩，适合工厂采购和工程师阅读

生成后请保存到 posts/zh/07-my-topic.html
然后帮我注册到 manifest.json
最后运行 python build.py 更新页面
```

---

## 方法三：命令行交互模式（高级用户）

```bash
# 交互式添加新文章（自动引导输入标题/分类等）
python build.py --init
```

会提示你输入文章信息，自动生成：
- `manifest.json` 条目
- `posts/zh/XX-slug.html` 空白模板

---

## SEO 最佳实践

1. **每篇文章的 `excerpt`** 是搜索引擎摘要，请控制在 80~120 字
2. **`date`** 是文章发布日期，影响 Google 抓取优先级
3. **`featured: true`** 的文章会优先出现在首页
4. **`tags`** 会被渲染为文章底部的标签，利于内链和 SEO
5. 运行 `build.py` 后，`sitemap.xml` 会自动更新，提交到：
   - [百度搜索资源平台](https://ziyuan.baidu.com) → Sitemap 提交
   - [Google Search Console](https://search.google.com) → Sitemap 提交

---

## 文件结构说明

```
liu-blog/
├── manifest.json          ← 唯一数据源，文章元数据在这里维护
├── build.py               ← 自动化构建脚本
├── index.html             ← 首页（由 build.py 自动更新）
├── index_en.html          ← 英文首页（由 build.py 自动更新）
├── sitemap.xml            ← SEO 站点地图（由 build.py 自动更新）
├── feed.xml               ← RSS 订阅源（由 build.py 自动更新）
├── posts/
│   ├── zh/
│   │   ├── 01-phenolic-basics.html
│   │   ├── 02-material-selection.html
│   │   └── ...
│   └── en/
│       ├── 01-phenolic-basics.html
│       └── ...
├── pages/
│   ├── zh/blog.html       ← 中文博客列表（由 build.py 自动更新）
│   └── en/blog.html       ← 英文博客列表（由 build.py 自动更新）
└── assets/
    ├── css/
    └── js/
```

---

## 故障排除

**Q: `python build.py` 报错？**  
A: 确保安装了 Python 3.6+，直接在 `liu-blog/` 目录下运行命令。

**Q: 首页文章没有更新？**  
A: 检查 `manifest.json` 中该文章的 `zh` 字段路径是否正确，文件是否存在。

**Q: 英文文章不想写，能自动翻译吗？**  
A: 可以把中文文章发给 AI，附上提示："请翻译成英文，保持技术术语准确"。

**Q: 如何删除一篇文章？**  
A: 从 `manifest.json` 中删除条目，注释掉或删除 HTML 文件，然后运行 `python build.py`。
