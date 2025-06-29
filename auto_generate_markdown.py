import json
from pathlib import Path

INPUT_JSON = "categories.json"
OUTPUT_MD = "generated_projects.md"

default_icons = {
    "Languages": "🔠",
    "Frameworks": "🧱",
    "Database": "📦",
    "AI Frameworks": "🧱",
    "Object Detector": "⚙️",
    "AI Agents": "🧠",
    "Large Models": "🧠📦",
    "AI Applications": "🤖📱",
    "UI kit": "📊",
    "CRM / ERP / CMS": "📦",
    "Lowcode Platforms": "📦",
    "Dart/Flutter Tools": "🦋",
    "Easy Work Tools": "🛠️",
    "Datasets": "📚",
    "DevOps / Tools": "⚙️",
}


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


def generate_markdown(data: dict) -> str:
    md = ["---\n", "## 🔗 Quick Navigation\n"]

    # Quick Navigation
    for first_cat, subcats in data.items():
        md.append(f"### {first_cat}")
        if isinstance(subcats, dict):
            for second_cat in subcats:
                icon = default_icons.get(second_cat, "📁")
                anchor = anchor_name(second_cat)
                md.append(f"- [{icon} {second_cat}](#{anchor})")
        md.append("")

    md.append("---\n\n## 📚 Categories\n")

    for first_cat, subcats in data.items():
        md.append(f"### {first_cat}\n")
        if isinstance(subcats, dict):
            for second_cat, projects in subcats.items():
                anchor = anchor_name(second_cat)
                icon = default_icons.get(second_cat, "📁")

                md.append(f'<a name="{anchor}"></a>')
                if second_cat.lower() in [
                    "datasets",
                    "devops-tools",
                    "experimental-fun-projects",
                    "guides-handbooks-tutorials",
                ]:
                    # 一级分类展示，无需折叠
                    for proj in projects:
                        url = proj.get("url", proj.get("html_url", ""))
                        name = proj.get("name", "")
                        desc = (
                            proj.get("description") or ""
                        ).strip() or "No description."
                        md.append(f"- [{name}]({url}) – {desc}")
                else:
                    md.append(f"<details>\n  <summary>{icon} {second_cat}</summary>\n")
                    for proj in projects:
                        url = proj.get("url", proj.get("html_url", ""))
                        name = proj.get("name", "")
                        desc = (
                            proj.get("description") or ""
                        ).strip() or "No description."
                        md.append(f"  - [{name}]({url}) – {desc}")
                    md.append("</details>\n")
        md.append("")
    return "\n".join(md)


def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        categorized_projects = json.load(f)

    markdown = generate_markdown(categorized_projects)
    Path(OUTPUT_MD).write_text(markdown, encoding="utf-8")
    print(f"✅ 已生成 Markdown 文件: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
