from openai import OpenAI
import os
import json
from tqdm import tqdm

model = OpenAI(
    api_key=os.environ.get("APIKEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

categories = {
    "Full-Stack / Web Development": ["Database"],
    "Artificial Intelligence / Machine Learning": [
        "AI Frameworks",
        "Object Detector",
        "AI Agents",
        "Large Models",
        "AI Applications",
    ],
    "Frontend / UI / Mobile": ["UI kit"],
    "DevOps / Tools": [],
    "Developer Productivity": ["Dart/Flutter Tools", "Easy Work Tools"],
    "Experimental / Fun Projects": [],
    "Mature Open Source Projects (CRM / ERP / CMS)": ["CRM / ERP / CMS"],
    "Guides / Handbooks / Tutorials": [],
    "Datasets": [],
}


projects = json.load(open("all_starred_simplified.json", "r", encoding="utf-8"))


def classify_project(project, categories):
    prompt = f"""
你是一个分类助手。根据项目的名称、描述和主题，判断该项目最合适的二级分类（只能选一个）。
已有的一级分类和对应的二级分类如下：
{json.dumps(categories, indent=2, ensure_ascii=False)}

项目：
名称: {project['name']}
描述: {project['description']}
主题: {project['topics']}

请直接返回该项目对应的二级分类名称，若无匹配则返回 "未知分类",如果是“Guides / Handbooks / Tutorials”或者“Datasets”，直接返回此大类名即可。
"""
    completion = model.chat.completions.create(
        model="qwen-max",
        # model = "moonshot-v1-128k-vision-preview",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": "你是一个分类助手。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    res = completion.choices[0].message.content
    return res


result = {}
for first_cat, subcats in categories.items():
    result[first_cat] = {subcat: [] for subcat in subcats}

result["未知分类"] = []

for proj in tqdm(projects):
    cls = classify_project(proj, categories)
    # 查找一级分类包含该二级分类
    found = False
    for first_cat, subcats in categories.items():
        if cls in subcats:
            result[first_cat][cls].append(proj)
            found = True
            break
    if not found:
        result["未知分类"].append(proj)
    print(f"项目 {proj['name']} 分类为: {cls}")

output_file = "result.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
