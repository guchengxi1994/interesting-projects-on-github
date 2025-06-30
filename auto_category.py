from openai import OpenAI
import os
import json
from tqdm import tqdm

model = OpenAI(
    api_key=os.environ.get("APIKEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

categories = {
    "Artificial Intelligence & Machine Learning": {
        "desc": "End-to-end AI/ML ecosystem: from foundational models to production-ready applications.",
        "subcategories": {
            "AI Agents": {
                "desc": "Agents, tools, and environments for AI-powered agents."
            },
            "Research": {"desc": "Research papers, datasets, and code repositories."},
            "Large Models": {
                "desc": "Training frameworks, inference engines, and model hubs."
            },
            "Computer Vision": {
                "desc": "Detection, segmentation, generation, and video understanding."
            },
            "Natural Language Processing": {
                "desc": "Vector search, language understanding, and multimodal models."
            },
            "AI Platforms & Tools": {
                "desc": "Libraries, SDKs, and MLOps pipelines for AI development."
            },
            "AI Applications": {
                "desc": "Ready-to-deploy AI-powered solutions for chatbots, recommendation, and analytics."
            },
        },
    },
    "Frontend & Mobile Development": {
        "desc": "User-facing experiences across web, mobile, and desktop environments.",
        "subcategories": {
            "Development Framework": {
                "desc": "React, Vue, Svelte, and full-stack meta-frameworks."
            },
            "Frontend & Mobile Applications": {
                "desc": "some frontend applications"
            },
            "UI Component Libraries": {
                "desc": "Design systems, component kits, and accessibility tools."
            },
        },
    },
    "Infrastructure & Data": {
        "desc": "Core building blocks for any software system: databases, storage, messaging, and data infrastructure.",
        "subcategories": {
            "Databases": {
                "desc": "Relational, vector, graph, and time-series databases."
            },
            "Storage Systems": {
                "desc": "Object storage, distributed filesystems, and data lakes."
            },
            "Messaging & Streaming": {
                "desc": "Event buses, task queues, and stream-processing platforms."
            },
            "Frameworks & SDKs":{
                "desc": "Frameworks and SDKs for building applications."
            },
            "Languages": {
                "desc": "Development languages and tools."
            }
        },
    },
    "Developer Tooling & DevOps": {
        "desc": "Toolchains that accelerate development, testing, deployment, and observability.",
        "subcategories": {
            "Build & Bundling": {
                "desc": "Webpack, Vite, esbuild, and Rust-based compilers."
            },
            "Testing & Quality": {
                "desc": "Unit, E2E, performance, and security testing suites."
            },
            "CI/CD & GitOps": {
                "desc": "GitHub Actions, ArgoCD, and infrastructure-as-code."
            },
            "Observability": {
                "desc": "Logging, metrics, tracing, and error-tracking platforms."
            },
        },
    },
    "Security & Privacy": {
        "desc": "Tooling and libraries for securing applications, data, and infrastructure.",
        "subcategories": {
            "Cryptography": {
                "desc": "Encryption, hashing, and zero-knowledge proof libraries."
            },
            "Vulnerability Scanning": {
                "desc": "SAST, DAST, and dependency-checking tools."
            },
            "Identity & Access Management": {
                "desc": "OAuth2, OpenID Connect, and SSO solutions."
            },
            "Secure Coding": {
                "desc": "Static analyzers, linters, and secret scanners."
            },
        },
    },
    "Web3 & Blockchain": {
        "desc": "Decentralized systems, smart contracts, and blockchain infrastructure.",
        "subcategories": {
            "Smart Contracts": {
                "desc": "Solidity, Vyper, Rust (Solana), Move (Aptos)."
            },
            "Blockchain Infrastructure": {
                "desc": "Nodes, wallets, and consensus clients."
            },
            "DeFi & NFTs": {"desc": "DEXs, lending protocols, and token standards."},
            "Web3 Tooling": {"desc": "SDKs, explorers, and developer frameworks."},
        },
    },
    "Fun Projects": {
        "desc": "some fun projects, such as games, rendering, and more.",
        "subcategories": {
            "Game Engines": {"desc": "Unity, Unreal, Godot, and custom engines."},
            "Real-Time Rendering": {"desc": "Vulkan, Metal, DirectX, and WebGPU."},
            "Interactive Media": {
                "desc": "VR/AR frameworks and creative coding tools."
            },
            "Physics & Simulation": {
                "desc": "Physics engines and procedural generation."
            },
        },
    },
    "Enterprise & Low-Code": {
        "desc": "Mature, production-grade systems for business automation.",
        "subcategories": {
            "CRM / ERP / CMS": {"desc": "Odoo, ERPNext, and mature CMS platforms."},
            "Low-Code Platforms": {
                "desc": "Appsmith, ToolJet, and internal-tool builders."
            },
            "Business Intelligence": {
                "desc": "Metabase, Superset, and data-visualization suites."
            },
            "Workflow Automation": {
                "desc": "Zapier alternatives and robotic-process automation."
            },
        },
    },
    "Learning Resources": {
        "desc": "Tutorials, documentation, and community-driven knowledge bases.",
        "subcategories": {
            "Tutorials & Guides": {"desc": "Step-by-step project walkthroughs."},
            "Documentation": {"desc": "Official docs, API references, and handbooks."},
            "Best Practices & Cheat Sheets": {
                "desc": "Wikis, cheatsheets, and proven engineering conventions."
            },
            "Courses & Workshops": {
                "desc": "Interactive learning platforms and MOOCs."
            },
        },
    },
    "Datasets": {
        "desc": "Curated collections of data for training, benchmarking, and research.",
        "subcategories": {
            "Machine Learning Datasets": {
                "desc": "Image, text, audio, and multimodal corpora."
            },
            "Benchmark Suites": {
                "desc": "Standardized evaluation datasets and leaderboards."
            },
            "Domain-Specific Data": {
                "desc": "Finance, healthcare, geospatial, and IoT datasets."
            },
            "Synthetic Data": {
                "desc": "Generated datasets for privacy-preserving research."
            },
        },
    },
}


projects = json.load(open("all_starred_simplified.json", "r", encoding="utf-8"))


def classify_project(project, categories):
    prompt = f"""
你是一个开源项目分类助手，请根据每个项目的“名称、描述、主题（topics）”将其归入最匹配的分类中。

以下是完整的分类体系（包含一级分类描述和二级分类描述）：
{json.dumps(categories, indent=2, ensure_ascii=False)}

分类规则如下：

1. 你必须从所有二级分类中选择一个最合适的分类，并**仅返回该分类名称字符串**。
2. 但如果该项目明显只属于以下这些一级分类本身：
   - "Developer Tooling & DevOps"
   - "Security & Privacy"
   - "Web3 & Blockchain"
   - "Gaming & Graphics"
   - "Learning Resources"
   - "Datasets"
   则可以直接返回一级分类名称（不选取其子类）。
3. `topics` 若为空数组 (`[]`)，请忽略该字段；
   `description` 若为空字符串或为 null，也请忽略；
   仅在字段有内容时用于辅助判断。
4. 优先根据 `topics` 判断，其次参考 `name` 和 `description`。
5. 如果无法确定该项目属于任何分类，请返回："无匹配，需人工确认"。

项目信息如下：
- 名称: {project['name']}
- 描述: {project['description']}
- 主题: {project['topics']}

请注意：
- **只返回最终分类名称字符串（例如："Large Models" 或 "Datasets"）**；
- 不要附加任何解释、标点或额外内容。
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
