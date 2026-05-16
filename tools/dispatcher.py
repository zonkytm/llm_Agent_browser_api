import re

from logger import Colors, log
from tools.fs import list_dir, read_file, write_file


def execute(response: str) -> str | None:
    response = response.replace("\r\n", "\n").replace("\r", "\n")

    m = re.search(r"\[LIST_DIR\]\s*(.+)", response)
    if m:
        path = m.group(1).strip()
        log(f"\n🛠 LIST_DIR: {path}\n", Colors.YELLOW)
        return list_dir(path)

    m = re.search(r"\[READ_FILE\]\s*(.+)", response)
    if m:
        path = m.group(1).strip()
        log(f"\n🛠 READ_FILE: {path}\n", Colors.YELLOW)
        return read_file(path)

    # WRITE_FILE — handle slight formatting variations from the model
    m = (
        re.search(r"\[WRITE_FILE\]\s*([^\n]+)\n+\s*CONTENT:\s*\n([\s\S]+)", response)
        or re.search(r"\[WRITE_FILE\]\s*([^\n]+)\s+CONTENT:\s*\n([\s\S]+)", response)
        or re.search(r"\[WRITE_FILE\]\s*([^\n]+).*?CONTENT:\s*\n?([\s\S]+)", response, re.DOTALL)
    )
    if m:
        path, content = m.group(1).strip(), m.group(2).rstrip()
        log(f"\n🛠 WRITE_FILE: {path}\n", Colors.YELLOW)
        return write_file(path, content)

    return None
