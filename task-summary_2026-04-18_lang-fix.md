# 语言切换混乱修复 - 2026-04-18

## 问题
- 中文页面(index.html)行业资讯标题显示英文
- 英文页面(index_en.html)新闻分类显示中文
- 语言切换后内容混乱

## 根因
1. `init()` 在页面加载时调用 `applyI18n(localStorage.getItem("liu_blog_lang") || getLang())`，如果 localStorage 存了之前的语言偏好(如'en')，会把中文页面内容覆盖成英文
2. index_en.html 中的新闻分类(category)是中文硬编码，未翻译
3. localStorage 残留旧语言偏好

## 修复
1. 移除 init() 中的 applyI18n() 调用 — 每个HTML文件自带正确语言内容
2. index_en.html 新闻分类翻译: 入门手册→Beginner Guide, 选型指南→Selection Guide, 技术深潜→Technical Deep Dive, 行业观察→Industry Insights
3. init() 中添加 localStorage.removeItem("liu_blog_lang") 清除残留偏好
4. switchLang 改为相对路径跳转(兼容 file:// 协议)

## 文件
- liu-blog/assets/js/main.js — 移除applyI18n调用，清除localStorage，switchLang用相对路径
- liu-blog/index_en.html — 新闻分类中文→英文
