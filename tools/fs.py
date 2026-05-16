import os


def list_dir(path: str) -> str:
    if not os.path.exists(path):
        return f"[ERROR]\nPath not found:\n{path}"
    try:
        entries = []
        for name in os.listdir(path)[:200]:
            full = os.path.join(path, name)
            entries.append(f"[DIR] {name}" if os.path.isdir(full) else f"[FILE] {name}")
        return "[RESULT]\n" + "\n".join(entries)
    except Exception as e:
        return f"[ERROR]\n{e}"


def read_file(path: str) -> str:
    if not os.path.exists(path):
        return f"[ERROR]\nFile not found:\n{path}"
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return "[RESULT]\n" + f.read(6000)
    except Exception as e:
        return f"[ERROR]\n{e}"


def write_file(path: str, content: str) -> str:
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"[RESULT]\nFile written:\n{path}"
    except Exception as e:
        return f"[ERROR]\n{e}"
