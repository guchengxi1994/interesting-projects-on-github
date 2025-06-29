from openai import OpenAI
import os
import json
from tqdm import tqdm

model = OpenAI(
    api_key=os.environ.get("APIKEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

categories = {
    "Full-Stack / Web Development": {
        "desc": "包含完整开发工具和框架，包括前后端与数据库",
        "subcategories": {
            "Database": "数据库相关工具和引擎",
            "Languages": "开发使用的主流语言",
            "Frameworks/SDKs": "开发框架或者SDK，如前端或后端框架，例如springboot，flutter等",
        },
    },
    "Artificial Intelligence / Machine Learning": {
        "desc": "与 AI 和机器学习相关的项目",
        "subcategories": {
            "AI Frameworks": "AI模型框架，类似pytorch或tensorflow",
            "Object Detector": "目标检测相关的算法和模型",
            "AI Agents": "具备行动能力的 AI 智能体",
            "Large Models": "大语言模型、多模态模型或大型预训练模型",
            "AI Applications": "基于 AI 的应用程序，如 AI 绘图、对话等",
        },
    },
    "Frontend / UI / Mobile": {
        "desc": "前端界面、UI 库及移动端开发工具",
        "subcategories": {
            "UI kit": "用户界面组件库",
            "Frameworks/SDKs": "前端/移动端生态框架，例如状态管理框架（riverpod），或者缓存框架（hive，isar）等",
            "Applications": "前端或移动端应用模板或示例",
        },
    },
    "DevOps / Tools": {"desc": "DevOps、部署、构建和测试工具", "subcategories": {}},
    "Developer Productivity": {
        "desc": "提升开发效率的工具集",
        "subcategories": {
            "Dart/Flutter Tools": "与 Dart 或 Flutter 相关的辅助工具",
            "Easy Work Tools": "简化重复性工作的开发小工具",
        },
    },
    "Experimental / Fun Projects": {"desc": "有趣或实验性的开源项目", "subcategories": {}},
    "Mature Open Source Projects (CRM / ERP / CMS)": {
        "desc": "成熟的大型开源系统",
        "subcategories": {
            "CRM / ERP / CMS": "客户管理、企业资源管理、内容管理系统",
            "Lowcode Platforms": "低代码开发平台",
        },
    },
    "Guides / Handbooks / Tutorials": {"desc": "教程、开发手册与学习资料", "subcategories": {}},
    "Datasets": {"desc": "可用于训练或评估模型的数据集", "subcategories": {}},
}


projects = json.load(open("all_starred_simplified.json", "r", encoding="utf-8"))


def classify_project(project, categories):
    prompt = f"""
你是一个专业的“开源项目分类助手”，请根据以下信息，将项目准确归入最匹配的分类。

【分类参考信息】
以下是完整的分类体系，每个一级分类包含：
- **分类说明（desc）**：用于辅助理解该分类的边界与适用范围；
- **二级分类（subcategories）**：具体可选的分类标签，部分一级分类无需细分。

分类体系如下：
{json.dumps(categories, indent=2, ensure_ascii=False)}

【分类规则】

1. 你**只能从上述所有“二级分类”中选择一个最匹配的分类名称（字符串）**，并返回该名称。
2. 特殊情况：若项目属于以下一级分类之一，直接返回对应一级分类的名称（无需选择二级分类）：
   - "DevOps / Tools"：与 DevOps、部署、构建、测试等相关
   - "Experimental / Fun Projects"：有趣、实验性、探索性质的项目
   - "Guides / Handbooks / Tutorials"：教程、手册、学习资料
   - "Datasets"：用于训练或评估的数据集
3. 分类判断标准：
   - 优先根据 `topics` 字段判断；
   - 其次参考 `name`（项目名称）；
   - 再次参考 `description`（项目描述）；
   - `topics` 为空数组 `[]` 时忽略该字段；
   - `description` 为空字符串或 `null` 时忽略该字段；
4. 在判断时，请**结合分类说明（desc）理解分类含义**，确保准确归类。
5. 若无任何分类匹配，请返回固定字符串："无匹配，需人工确认"。

【项目信息】

- 名称: {project['name']}
- 描述: {project['description']}
- 主题: {project['topics']}

请仅返回最终分类名称字符串，严禁附加任何解释、分析或格式内容。
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

# 初始化：为每个一级分类建结构
for first_cat, first_cat_info in categories.items():
    result[first_cat] = {
        **{subcat: [] for subcat in first_cat_info.get("subcategories", {})},
        "__root__": [],  # 添加一级分类的直接存储位置
    }

result["未知分类"] = []

for proj in tqdm(projects, desc="分类项目"):
    cls = classify_project(proj, categories)
    found = False

    # ✅ 先检查：是否直接是一级分类（比如 "Datasets"）
    if cls in categories:
        result[cls]["__root__"].append(proj)
        found = True
    else:
        # ✅ 检查是否是某个二级分类
        for first_cat, first_cat_info in categories.items():
            if cls in first_cat_info.get("subcategories", {}):
                result[first_cat][cls].append(proj)
                found = True
                break

    if not found:
        result["未知分类"].append(proj)

    print(f"项目 {proj['name']} 分类为: {cls}")


output_file = "un_sorted_categories.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
