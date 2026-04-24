# liu-blog Agent 工作手册

> 本手册供其他 AI Agent 查阅，拿到此项目的任何 Agent 只需读这一份文件即可上岗。

---

## 一、项目速查

| 项目 | 值 |
|------|-----|
| **项目名** | 刘的博客（华玲机械背景，专业内容博客） |
| **主题** | 酚醛树脂（胶木/Bakelite）机械配件，15年行业经验 |
| **仓库** | `djdufud13-cell/Decap-CMS`（main 分支） |
| **本地工作区** | `C:\Users\Administrator\.qclaw\workspace\liu-blog\` |
| **Netlify 地址** | `https://dazzling-sprite-4c4e02.netlify.app` |
| **CMS 入口** | `https://dazzling-sprite-4c4e02.netlify.app/admin/` |
| **CMS 账号** | `15503295692@163.com` |
| **联系邮箱** | `15503295692@163.com` |
| **联系电话** | `+86 155 0329 5692` |
| **公司地址** | 河北省衡水市桃城区富强北街 |
| **Cron 任务** | Job ID `85239a85-e123-4ce5-99b9-38def3b38639`（每日胶木资讯日报） |

---

## 二、核心发布流程

### 原理
```
AI 生成文章 → git add . && git commit && git push → Netlify 自动部署 → 1-2分钟上线
```

### 标准 git 命令
```powershell
cd C:\Users\Administrator\.qclaw\workspace\liu-blog
git add .
git commit -m "feat: 文章标题"
git push origin main
```

---

## 三、文章目录规范

| 语言 | 目录 | 命名规则 |
|------|------|---------|
| 中文 | `posts/zh/` | `07-title.html`（序号-英文标题.html） |
| 英文 | `posts/en/` | `07-title.html` |
| 资讯 | `news/` | `YYYY-MM-DD-title.html` |
| 列表页 | `posts/zh/index.html` | 中文文章列表 |
| 列表页 | `posts/en/index.html` | 英文文章列表 |

**现有最大序号（截至2026-04-24）：**
- 中文：06（下一首为 07）
- 英文：03（04-06 待翻译）

---

## 四、HTML 文章模板

每篇文章必须是完整的独立 HTML 文件，包含以下结构：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>文章标题 - 刘的博客</title>
  <meta name="description" content="摘要，100-150字">
  <meta name="keywords" content="关键词1, 关键词2, 酚醛树脂">
  <link rel="canonical" href="https://dazzling-sprite-4c4e02.netlify.app/posts/zh/文件名.html">
  <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
  <nav class="navbar">
    <div class="container nav-inner">
      <a href="../../index.html" class="nav-brand">刘的博客</a>
      <a href="../../posts/zh/index.html" class="btn-outline" style="font-size:0.85rem;">← 返回文章列表</a>
    </div>
  </nav>
  <main class="container" style="max-width:800px;padding:60px 20px;">
    <article>
      <header style="margin-bottom:40px;">
        <div style="font-size:0.85rem;color:var(--text-light);margin-bottom:12px;">
          <span>2026-04-24</span> · <span>作者：刘工</span> · <span>阅读约5分钟</span>
        </div>
        <h1 style="font-size:2rem;line-height:1.4;color:var(--text-dark);">文章标题</h1>
        <p style="font-size:1.05rem;color:var(--text-muted);line-height:1.7;">文章导语摘要。</p>
      </header>
      <div class="article-body" style="line-height:1.9;">
        <h2>第一节标题</h2>
        <p>正文内容...</p>
      </div>
      <footer style="margin-top:60px;padding-top:30px;border-top:1px solid var(--border);">
        <p style="font-size:0.9rem;color:var(--text-light);">
          如有疑问，欢迎联系：
          <a href="mailto:15503295692@163.com">15503295692@163.com</a>
        </p>
      </footer>
    </article>
  </main>
</body>
</html>
```

**必须项：**
- `title` / `description` / `canonical` 三个 meta
- CSS 路径：`../../assets/css/style.css`（相对于 posts/zh/ 或 posts/en/）
- 文件编码：**UTF-8 无 BOM**

---

## 五、文件写入规则（强制）

本项目所有文本文件写入**必须**通过以下脚本执行，不得直接使用 `write` 工具：

```powershell
# 平台检测（必须先执行）
python "D:\Program Files\QClaw\resources\openclaw\config\skills\qclaw-text-file\scripts\write_file.py" --detect

# 写入目标文件（用 --content-file 方式，内容先写临时文件）
python "D:\Program Files\QClaw\resources\openclaw\config\skills\qclaw-text-file\scripts\write_file.py" --path "<目标文件>" --content-file "<临时文件>"

# 临时文件路径（Windows PowerShell）
$env:TEMP\_tw_<文件名>.txt
```

---

## 六、快速触发指令

用户可以直接说以下任一指令，Agent 自动执行完整流程：

| 指令 | 行为 |
|------|------|
| `帮我写一篇关于"xxx"的文章，发布到博客` | 生成中文文章 → 写入文件 → git push |
| `帮我把第X篇中文文章翻译成英文` | 翻译 → 保存到 posts/en/ → git push |
| `搜索今天的酚醛树脂行业新闻，写成资讯发布` | 搜索 → 生成文章 → 写入 news/ → git push |
| `更新文章列表页` | 读取 posts/zh/ 下所有文件 → 更新 index.html 卡片 → git push |

---

## 七、CMS 后台使用（Decap CMS）

**入口：** `https://dazzling-sprite-4c4e02.netlify.app/admin/`

**三个内容集合：**
- `posts-zh`：中文文章（需 .md 格式，现有 .html 文章不在 CMS 中）
- `posts-en`：英文文章
- `news`：新闻资讯

**注意：** 现有 .html 文章不会出现在 CMS 中，如需通过 CMS 管理需转换为 .md 格式。

---

## 八、配色与样式

| 用途 | 色值 |
|------|------|
| 主色（暖橙） | `#E87722` |
| 辅助（浅橙） | `#F4A261` |
| 点缀（薄荷绿） | `#2A9D8F` |
| 背景（暖奶白） | `#FFF8F0` |
| 正文（深棕） | `#3D2B1F` |
| 字体标题 | Noto Serif SC |
| 字体正文 | Noto Sans SC |

---

## 九、SEO 文件

| 文件 | 说明 |
|------|------|
| `sitemap.xml` | 站点地图（27个URL，已验证全部200） |
| `robots.txt` | 爬虫规则，sitemap 指向 `http://149.104.83.199/sitemap.xml` |
| `googlec3c9c9c71fa69540.html` | Google Search Console 验证 |

---

## 十、常见问题

**Q: push 超时怎么办？**
→ 分批提交，每次改动的文件不超过 10 个；或者重试 `git push origin main`

**Q: 页面有缓存？**
→ `Ctrl+Shift+R` 硬刷新；或等待 1-2 分钟 Netlify 部署完成

**Q: 用户问博客后台怎么用？**
→ 引导去 `https://dazzling-sprite-4c4e02.netlify.app/admin/` 登录，三个区域分别管理中文/英文/资讯

**Q: 联系表单在哪查看？**
→ Netlify 后台 → Forms 页面（前提：HTML 表单需加 `data-netlify="true"` 属性）
