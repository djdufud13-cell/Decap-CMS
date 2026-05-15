#!/usr/bin/env python3
import json, re, sys

content = open(r"C:\Users\Administrator\.qclaw\workspace\liudeboke-blog\feishu_records.json", encoding="utf-8").read()
data = json.loads(content)

pending = []
for r in data.get("records", []):
    f = r.get("fields", {})
    status = f.get("审阅状态", "")
    upload_status = f.get("是否上传", "")
    title = f.get("文章标题", "")
    score_match = re.search(r'Score:\s*(\d+)/100', f.get("修改意见", ""))
    score = int(score_match.group(1)) if score_match else 0
    
    if status == "已通过" and upload_status == "待上传":
        pending.append({
            "record_id": r.get("record_id"),
            "title": title,
            "score": score,
            "keyword": f.get("目标关键词", ""),
            "article_num": f.get("文章序号", ""),
            "body": f.get("文章正文", "")
        })

pending.sort(key=lambda x: x["score"], reverse=True)

print(f"Found {len(pending)} articles pending upload:\n")
for i, a in enumerate(pending, 1):
    print(f"=== Article {i} ===")
    print(f"Score: {a['score']}/100")
    print(f"Title: {a['title']}")
    print(f"Record ID: {a['record_id']}")
    print(f"Keywords: {a['keyword']}")
    print(f"Body length: {len(a['body'])} chars")
    print()

if len(pending) >= 2:
    import json
    top2 = pending[:2]
    with open(r"C:\Users\Administrator\.qclaw\workspace\liudeboke-blog\top2_articles.json", "w", encoding="utf-8") as f:
        json.dump(top2, f, ensure_ascii=False, indent=2)
    print("Saved top 2 articles to top2_articles.json")
