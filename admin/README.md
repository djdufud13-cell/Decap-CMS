# 刘的博客 - CMS后台说明

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
