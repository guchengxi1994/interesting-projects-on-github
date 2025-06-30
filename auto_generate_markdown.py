import json
from pathlib import Path
from urllib.parse import quote_plus

INPUT_JSON = "categories.json"
OUTPUT_MD = "README.md"

# 默认图标配置
default_icons = {
    "Languages": "🔠",
    "Databases": "📦",
    "Frameworks & SDKs": "🧱",
    "Storage Systems": "💾",
    "Messaging & Streaming": "📨",
    "Large Models": "🧠📦",
    "Computer Vision": "👁️",
    "AI Agents": "🧠",
    "Natural Language Processing": "💬",
    "AI Tools & Frameworks": "🛠️🤖",
    "AI Applications": "🤖📱",
    "Web Frameworks": "🌐",
    "Mobile Development": "📱",
    "Frontend & Mobile Applications": "🖥️",
    "UI Component Libraries": "🧩",
    "Build & Bundling": "📦",
    "Testing & Quality": "✅",
    "CI/CD & GitOps": "🔁",
    "Observability": "📈",
    "Cryptography": "🔐",
    "Vulnerability Scanning": "🛡️",
    "Identity & Access Management": "🧑‍💼",
    "Secure Coding": "🧪",
    "Smart Contracts": "📜",
    "Blockchain Infrastructure": "⛓️",
    "DeFi & NFTs": "💰",
    "Web3 Tooling": "🧰",
    "Game Engines": "🎮",
    "Real-Time Rendering": "🖼️",
    "Interactive Media": "🎨",
    "Physics & Simulation": "🧲",
    "CRM / ERP / CMS": "🏢",
    "Low-Code Platforms": "📉",
    "Business Intelligence": "📊",
    "Workflow Automation": "🔄",
    "Tutorials & Guides": "📘",
    "Documentation": "📄",
    "Best Practices & Cheat Sheets": "🧾",
    "Courses & Workshops": "🎓",
    "Machine Learning Datasets": "📚",
    "Benchmark Suites": "📏",
    "Domain-Specific Data": "📂",
    "Synthetic Data": "🧬",
}

badge_colors = [
    "blue",
    "green",
    "orange",
    "red",
    "yellow",
    "purple",
    "pink",
    "brightgreen",
    "lightgrey",
]


def anchor_name(title: str) -> str:
    return (
        title.lower()
        .replace(" ", "-")
        .replace("/", "")
        .replace(":", "")
        .replace(",", "")
        .replace(".", "")
        .strip("-")
        .replace("--", "-")
    )


def safe_badge_label(label: str) -> str:
    return quote_plus(label).replace("-", "--")


def render_topics(topics: list, max_length=3) -> str:
    if not topics:
        return ""
    badges = []
    for i, topic in enumerate(topics[:max_length]):
        color = badge_colors[i % len(badge_colors)]
        safe_topic = safe_badge_label(topic)
        badges.append(
            f"![{topic}](https://img.shields.io/badge/{safe_topic}-{color}?style=flat-square)"
        )
    return " " + " ".join(badges)


def generate_markdown(data: dict) -> str:
    md = ["---\n", "## 🔗 Quick Navigation\n"]

    for first_cat, first_meta in data.items():
        icon = "📁"
        md.append(f"### {icon} {first_cat}")
        subcats = first_meta.get("subcategories", {})
        for second_cat in subcats:
            icon2 = default_icons.get(second_cat, "📁")
            anchor = anchor_name(f"{first_cat}-{second_cat}")
            md.append(f"- [{icon2} {second_cat}](#{anchor})")
        md.append("")

    md.append("---\n\n## 📚 Categories\n")

    for first_cat, first_meta in data.items():
        icon = "📁"
        md.append(f"### {icon} {first_cat}\n")
        subcats = first_meta.get("subcategories", {})
        for second_cat, second_meta in subcats.items():
            anchor = anchor_name(f"{first_cat}-{second_cat}")
            icon2 = default_icons.get(second_cat, "📁")
            md.append(f'<a name="{anchor}"></a>')
            md.append(f"<details>\n  <summary>{icon2} {second_cat}</summary>\n")
            for proj in second_meta.get("projects", []):
                url = proj.get("url") or proj.get("html_url", "")
                name = proj.get("fullname", proj.get("name", ""))
                desc = (proj.get("description") or "").strip() or "No description."
                topics = render_topics(proj.get("topics", []))
                md.append(f"  - [{name}]({url}) – {desc}{topics}")
            md.append("</details>\n")

        md.append("")

    return "\n".join(md)


markdown_template = """
# 🚀 Interesting Projects on GitHub

## 👋 About Me

I'm a full-stack developer proficient in **Java**, **Python**, and **Go**, with some hands-on experience in **Rust**. On the frontend side, I mainly use **Flutter**, and I also have basic knowledge of **JavaScript** and **TypeScript**.

My academic background is in **Artificial Intelligence**, which I studied during my postgraduate education. I'm passionate about exploring cutting-edge AI tools, frameworks, and applications.

This repository is a curated collection of **interesting, inspiring, or technically impressive projects** I've come across on GitHub. I use this space to track and organize them across different fields.


{{markdown_content}}

---

## 📝 How to Use

You can explore each category and check out the linked repositories. I'll continue updating this list as I find more interesting projects.

Feel free to **star** the repository if you find it useful or inspiring!

---

> Made with ❤️ by a curious full-stack developer and AI enthusiast.

*If you want to generate your own project list, you can read my codes to generate it*.
```powershell
python get_all_stars.py # generate all your stars
python filter_stars.py # filter your stars
python auto_category.py # generate category content
python auto_generate_markdown.py # generate markdown
```

"""


def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        categorized_projects = json.load(f)

    markdown = generate_markdown(categorized_projects)
    md = markdown_template.replace("{{markdown_content}}", markdown)
    Path(OUTPUT_MD).write_text(md, encoding="utf-8")
    print(f"✅ 已生成 Markdown 文件: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
