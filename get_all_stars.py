import requests
import json
import os

# 配置项
output_dir = "./starred_repos"
per_page = 30

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

page = 1
total_count = 0

while True:
    url = f"https://api.github.com/users/guchengxi1994/starred?per_page={per_page}&page={page}"
    response = requests.get(url)
    data = response.json()

    if not data:
        print("✅ 所有页面已完成")
        break

    # 写入 JSON 文件
    file_path = os.path.join(output_dir, f"starred_page_{page}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ 已写入：{file_path}（共 {len(data)} 条）")
    total_count += len(data)
    page += 1

print(f"\n🎉 总共写入 {total_count} 个项目，分为 {page - 1} 个文件")
