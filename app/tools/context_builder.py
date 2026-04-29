import os
import re
import json

BASE_PATH = "app/modules"


def read_python_files():
    files_data = []

    for root, _, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                files_data.append({
                    "path": path,
                    "content": content
                })

    return files_data


def remove_comments(code: str) -> str:
    result = []
    in_string = False
    string_char = ""

    for line in code.split("\n"):
        new_line = ""
        i = 0

        while i < len(line):
            char = line[i]

            if char in ('"', "'"):
                if not in_string:
                    in_string = True
                    string_char = char
                elif string_char == char:
                    in_string = False

            if not in_string and char == "#":
                break

            new_line += char
            i += 1

        result.append(new_line)

    return "\n".join(result)


def detect_module(path: str) -> str:
    parts = path.split(os.sep)
    if "users" in parts:
        return "users"
    if "image_analysis" in parts:
        return "image_analysis"
    return "other"


def priority(path: str) -> int:
    if "router" in path:
        return 1
    if "service" in path:
        return 2
    if "schemas" in path:
        return 3
    if "models" in path:
        return 4
    return 5


def summarize_code(code: str) -> str:
    lines = code.split("\n")
    summary = []

    for i, line in enumerate(lines):
        line = line.strip()

        if line.startswith("@router"):
            summary.append(line)

        if line.startswith("def ") or line.startswith("class "):
            summary.append(line)

    return "\n".join(summary[:15])

def limit_code(code: str, max_chars=1500) -> str:
    return code[:max_chars]


def build_context(files):
    output = {
        "project": "cloud-to-local-ai-platform",
        "modules": {}
    }

    for f in files:
        module = detect_module(f["path"])

        if module not in output["modules"]:
            output["modules"][module] = []

        output["modules"][module].append({
            "file": f["path"],
            "priority": priority(f["path"]),
            "summary": summarize_code(f["content"]),
            "code": remove_comments(f["content"]).strip()
        })

    for module in output["modules"]:
        output["modules"][module].sort(key=lambda x: x["priority"])

    return output


if __name__ == "__main__":
    files = read_python_files()
    context = build_context(files)

    with open("context.json", "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2)

    print("context.json gerado com sucesso")
