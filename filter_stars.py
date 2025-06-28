import json
import glob
import os
from tqdm import tqdm

input_dir = "./starred_repos"  # 替换为你的目录路径
output_file = "all_starred_simplified.json"

all_repos = []

files = sorted(glob.glob(os.path.join(input_dir, "starred_page_*.json")))

for file_path in tqdm(files, desc="Processing JSON files"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for repo in data:
            all_repos.append(
                {
                    "name": repo.get("name"),
                    "fullname": repo.get("full_name"),
                    "url": repo.get("html_url"),
                    "topics": repo.get("topics", []),
                    "description": repo.get("description", ""),
                }
            )

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_repos, f, indent=2, ensure_ascii=False)

print(f"✅ 共提取 {len(all_repos)} 个项目，写入 {output_file}")
