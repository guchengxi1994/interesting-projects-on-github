import json
from pathlib import Path
from urllib.parse import quote_plus

INPUT_JSON = "categories.json"
OUTPUT_MD = "README.md"

# 默认图标配置
default_icons = {
    "Languages": "🔠",
    "Frameworks": "🧱",
    "Frameworks/SDKs": "🧱",
    "Database": "📦",
    "AI Frameworks": "🧱",
    "Object Detector": "⚙️",
    "AI Agents": "🧠",
    "Large Models": "🧠📦",
    "AI Applications": "🤖📱",
    "UI kit": "📊",
    "Applications": "📱",
    "CRM / ERP / CMS": "📦",
    "Lowcode Platforms": "📦",
    "Dart/Flutter Tools": "🦋",
    "Easy Work Tools": "🛠️",
    "Datasets": "📚",
    "DevOps / Tools": "⚙️",
    "Experimental / Fun Projects": "🧪",
    "Guides / Handbooks / Tutorials": "📘",
    "Developer Productivity": "🧰",
    "Frontend / UI / Mobile": "📱",
    "Mature Open Source Projects (CRM / ERP / CMS)": "🏢",
    "Full-Stack / Web Development": "🌐",
    "Artificial Intelligence / Machine Learning": "🤖",
}

# 标签颜色配置，可自定义
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
    """生成 Markdown 锚点名称"""
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


def render_topics(topics: list, max_length=3) -> str:
    """使用 shields.io 生成标签 Badge"""
    if not topics:
        return ""

    badges = []
    for i, topic in enumerate(topics[:max_length]):  # 最多展示10个
        color = badge_colors[i % len(badge_colors)]
        safe_topic = quote_plus(topic)
        badge = f"![{topic}](https://img.shields.io/badge/{safe_topic}-{color}?style=flat-square)"
        badges.append(badge)

    return " " + " ".join(badges)


def generate_markdown(data: dict) -> str:
    md = ["---\n", "## 🔗 Quick Navigation\n"]

    # Quick Navigation
    for first_cat, subcats in data.items():
        icon = default_icons.get(first_cat, "📁")
        md.append(f"### {icon} {first_cat}")
        if isinstance(subcats, dict):
            for second_cat in subcats:
                icon2 = default_icons.get(second_cat, "📁")
                anchor = anchor_name(f"{first_cat}-{second_cat}")
                md.append(f"- [{icon2} {second_cat}](#{anchor})")
        md.append("")

    md.append("---\n\n## 📚 Categories\n")

    for first_cat, subcats in data.items():
        icon = default_icons.get(first_cat, "📁")
        md.append(f"### {icon} {first_cat}\n")

        if isinstance(subcats, dict):
            for second_cat, projects in subcats.items():
                anchor = anchor_name(f"{first_cat}-{second_cat}")
                icon2 = default_icons.get(second_cat, "📁")

                md.append(f'<a name="{anchor}"></a>')

                if second_cat == "__root__":
                    # 一级分类内的直接项目
                    for proj in projects:
                        url = proj.get("url") or proj.get("html_url", "")
                        name = proj.get("fullname", proj.get("name", ""))
                        desc = (
                            proj.get("description") or ""
                        ).strip() or "No description."
                        topics = render_topics(proj.get("topics", []))
                        md.append(f"- [{name}]({url}) – {desc}{topics}")
                else:
                    md.append(f"<details>\n  <summary>{icon2} {second_cat}</summary>\n")
                    for proj in projects:
                        url = proj.get("url") or proj.get("html_url", "")
                        name = proj.get("fullname", proj.get("name", ""))
                        desc = (
                            proj.get("description") or ""
                        ).strip() or "No description."
                        topics = render_topics(proj.get("topics", []))
                        md.append(f"  - [{name}]({url}) – {desc}{topics}")
                    md.append("</details>\n")

        md.append("")  # 分类之间空行

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
