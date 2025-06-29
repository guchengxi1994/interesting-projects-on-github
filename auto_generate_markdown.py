import json
from pathlib import Path

INPUT_JSON = "categories.json"
OUTPUT_MD = "generated_projects.md"

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

def render_topics(topics: list) -> str:
    """渲染标签小块"""
    tag_template = '<span style="background:#d4f4dd; color:#207544; border-radius:4px; padding:2px 6px; font-size:0.85em;">{}</span>'
    return " ".join([tag_template.format(t) for t in topics[:10]])  # 最多展示10个标签，防止太长

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
                        desc = (proj.get("description") or "").strip() or "No description."
                        topics = render_topics(proj.get("topics", []))
                        md.append(f"- [{name}]({url}) – {desc} {topics}")
                else:
                    md.append(f"<details>\n  <summary>{icon2} {second_cat}</summary>\n")
                    for proj in projects:
                        url = proj.get("url") or proj.get("html_url", "")
                        name = proj.get("fullname", proj.get("name", ""))
                        desc = (proj.get("description") or "").strip() or "No description."
                        topics = render_topics(proj.get("topics", []))
                        md.append(f"  - [{name}]({url}) – {desc} {topics}")
                    md.append("</details>\n")

        md.append("")  # 分类之间空行

    return "\n".join(md)

def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        categorized_projects = json.load(f)

    markdown = generate_markdown(categorized_projects)
    Path(OUTPUT_MD).write_text(markdown, encoding="utf-8")
    print(f"✅ 已生成 Markdown 文件: {OUTPUT_MD}")

if __name__ == "__main__":
    main()
