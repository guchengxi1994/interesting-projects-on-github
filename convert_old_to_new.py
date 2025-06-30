import json
from pathlib import Path

INPUT_FILE = "old_categories.json"
OUTPUT_FILE = "categories.json"


def convert_structure(old_data):
    new_data = {}

    for first_cat, subcats in old_data.items():
        # 如果是直接是列表，说明是无二级分类的一级分类（如 Datasets）
        if isinstance(subcats, list):
            new_data[first_cat] = {
                "desc": "TODO",
                "subcategories": {"__root__": {"projects": subcats}},
            }
        # 有二级分类
        elif isinstance(subcats, dict):
            new_data[first_cat] = {"desc": "TODO", "subcategories": {}}
            for second_cat, projects in subcats.items():
                new_data[first_cat]["subcategories"][second_cat] = {
                    "desc": "TODO",
                    "projects": projects,
                }
        else:
            print(f"⚠️ 跳过未知类型的分类：{first_cat}")

    return new_data


def main():
    old_path = Path(INPUT_FILE)
    if not old_path.exists():
        print(f"❌ 找不到文件：{INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        old_data = json.load(f)

    new_data = convert_structure(old_data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)

    print(f"✅ 已保存新格式文件为：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
