import os
import json

BASE_PATH = "app/modules"

CORE_FILES = [
    "app/main.py",
    "app/database.py",
    "app/dependencies.py",
]


def read_core_files():
    files_data = []

    for path in CORE_FILES:
        path = os.path.normpath(path)

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            files_data.append({
                "path": path,
                "content": content
            })

    return files_data


def read_python_files():
    files_data = []

    for root, _, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                path = os.path.normpath(path)

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
    filename = os.path.basename(path)

    if filename in {"main.py", "database.py", "dependencies.py"}:
        return "core"

    if "users" in parts:
        return "users"

    if "image_analysis" in parts:
        return "image_analysis"

    return "other"


def priority(path: str) -> int:
    filename = os.path.basename(path)

    if filename in {"main.py", "database.py", "dependencies.py"}:
        return 0

    if "router" in filename:
        return 1

    if "service" in filename:
        return 2

    if "schemas" in filename:
        return 3

    if "models" in filename:
        return 4

    return 5


def summarize_code(code: str) -> str:
    lines = code.split("\n")
    summary = []

    for line in lines:
        stripped = line.strip()

        if (
            stripped.startswith("@")
            or stripped.startswith("def ")
            or stripped.startswith("class ")
        ):
            summary.append(stripped)

    if not summary:
        summary = [line.strip() for line in lines[:5] if line.strip()]

    return "\n".join(summary[:15])


def limit_code(code: str, max_chars=1500) -> str:
    return code[:max_chars]


def build_context(files):
    core_files = read_core_files()
    all_files = core_files + files

    output = {
        "project": "cloud-to-local-ai-platform",
        "modules": {}
    }

    for f in all_files:
        module = detect_module(f["path"])

        if module not in output["modules"]:
            output["modules"][module] = []

        output["modules"][module].append({
            "file": f["path"],
            "priority": priority(f["path"]),
            "summary": summarize_code(f["content"]),
            "code": limit_code(remove_comments(f["content"]).strip())
        })

    # ordenar arquivos dentro de cada módulo
    for module in output["modules"]:
        output["modules"][module].sort(key=lambda x: x["priority"])

    # garantir core primeiro e resto ordenado
    output["modules"] = dict(sorted(
        output["modules"].items(),
        key=lambda x: (0 if x[0] == "core" else 1, x[0])
    ))

    return output


if __name__ == "__main__":
    files = read_python_files()
    context = build_context(files)

    with open("context.json", "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2)

    print("context.json gerado com sucesso")