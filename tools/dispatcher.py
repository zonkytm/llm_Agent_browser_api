import re

from logger import Colors, log
from tools.fs import list_dir, read_file, write_file, delete_path, move_path, search_files, run_command


def execute(response: str) -> str | None:
    response = response.replace("\r\n", "\n").replace("\r", "\n")

    # 1. LIST_DIR
    m = re.search(r"\[LIST_DIR\]\s*(.+)", response)
    if m:
        path = m.group(1).strip()
        log(f"\n🛠 LIST_DIR: {path}\n", Colors.YELLOW)
        return list_dir(path)

    # 2. READ_FILE
    m = re.search(r"\[READ_FILE\]\s*(.+)", response)
    if m:
        path = m.group(1).strip()
        log(f"\n🛠 READ_FILE: {path}\n", Colors.YELLOW)
        return read_file(path)

    # 3. WRITE_FILE
    m = (
        re.search(r"\[WRITE_FILE\]\s*([^\n]+)\n+\s*CONTENT:\s*\n([\s\S]+)", response)
        or re.search(r"\[WRITE_FILE\]\s*([^\n]+)\s+CONTENT:\s*\n([\s\S]+)", response)
        or re.search(r"\[WRITE_FILE\]\s*([^\n]+).*?CONTENT:\s*\n?([\s\S]+)", response, re.DOTALL)
    )
    if m:
        path, content = m.group(1).strip(), m.group(2).rstrip()
        log(f"\n🛠 WRITE_FILE: {path}\n", Colors.YELLOW)
        return write_file(path, content)

    # 4. DELETE
    m = re.search(r"\[DELETE\]\s*(.+)", response)
    if m:
        path = m.group(1).strip()
        log(f"\n🛠 DELETE: {path}\n", Colors.YELLOW)
        return delete_path(path)

    # 5. MOVE
    m = re.search(r"\[MOVE\]\s*(.+)\s+TO\s+(.+)", response)
    if m:
        src, dst = m.group(1).strip(), m.group(2).strip()
        log(f"\n🛠 MOVE: {src} -> {dst}\n", Colors.YELLOW)
        return move_path(src, dst)

    # 6. SEARCH
    m = re.search(r"\[SEARCH\]\s*(.+)", response)
    if m:
        pattern = m.group(1).strip()
        log(f"\n🛠 SEARCH: {pattern}\n", Colors.YELLOW)
        return search_files(pattern)

    # 7. RUN
    m = re.search(r"\[RUN\]\s*(.+)", response)
    if m:
        cmd = m.group(1).strip()
        log(f"\n🛠 RUN: {cmd}\n", Colors.YELLOW)
        return run_command(cmd)

    return None
