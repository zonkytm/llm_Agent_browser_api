import os
import shutil
import subprocess
import glob


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


def delete_path(path: str) -> str:
    try:
        if not os.path.exists(path):
            return f"[ERROR]\nPath not found: {path}"
        if os.path.isdir(path):
            shutil.rmtree(path)
            return f"[RESULT]\nDirectory deleted: {path}"
        else:
            os.remove(path)
            return f"[RESULT]\nFile deleted: {path}"
    except Exception as e:
        return f"[ERROR]\n{e}"


def move_path(src: str, dst: str) -> str:
    try:
        shutil.move(src, dst)
        return f"[RESULT]\nMoved from {src} to {dst}"
    except Exception as e:
        return f"[ERROR]\n{e}"


def search_files(pattern: str, root_dir: str = ".") -> str:
    try:
        # Recursive glob search
        files = glob.glob(os.path.join(root_dir, pattern), recursive=True)
        if not files:
            return "[RESULT]\nNo matches found."
        return "[RESULT]\n" + "\n".join(files[:100])
    except Exception as e:
        return f"[ERROR]\n{e}"


def run_command(command: str) -> str:
    try:
        # Use shell=True for convenience, but be aware of security in production
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="ignore"
        )
        output = result.stdout + result.stderr
        return f"[RESULT]\nExit Code: {result.returncode}\nOutput:\n{output}"
    except subprocess.TimeoutExpired:
        return "[ERROR]\nCommand timed out after 30 seconds."
    except Exception as e:
        return f"[ERROR]\n{e}"
