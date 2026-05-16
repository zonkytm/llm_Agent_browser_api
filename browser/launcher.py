import os
import shutil
import socket
import subprocess
import time

from config import CHROME_PATH, DEBUG_PORT, DEBUG_PROFILE_ROOT, DEEPSEEK_URL, ORIGINAL_PROFILE
from logger import Colors, log


def kill_chrome():
    log("☠ Killing Chrome...", Colors.YELLOW)
    os.system("taskkill /F /IM chrome.exe >nul 2>&1")
    time.sleep(2)


def copy_profile():
    log("Copying Chrome profile...", Colors.CYAN)

    if os.path.exists(DEBUG_PROFILE_ROOT):
        shutil.rmtree(DEBUG_PROFILE_ROOT, ignore_errors=True)

    os.makedirs(DEBUG_PROFILE_ROOT, exist_ok=True)

    ignore = shutil.ignore_patterns(
        "History*", "Web Data*", "Login Data*", "Cookies*",
        "Visited Links*", "Current Session*", "Current Tabs*",
        "Last Session*", "Last Tabs*"
    )

    shutil.copytree(
        ORIGINAL_PROFILE,
        os.path.join(DEBUG_PROFILE_ROOT, "Default"),
        ignore=ignore,
        dirs_exist_ok=True,
    )

    log("Profile copied", Colors.GREEN)


def _wait_debug_port(timeout=30) -> bool:
    log("Waiting debug-port...", Colors.CYAN)
    start = time.time()
    while time.time() - start < timeout:
        try:
            s = socket.create_connection(("127.0.0.1", int(DEBUG_PORT)), timeout=1)
            s.close()
            return True
        except OSError:
            time.sleep(0.5)
    return False


def launch_chrome():
    log("Launching Chrome...", Colors.CYAN)

    cmd = [
        CHROME_PATH,
        f"--remote-debugging-port={DEBUG_PORT}",
        "--remote-debugging-address=127.0.0.1",
        f"--user-data-dir={DEBUG_PROFILE_ROOT}",
        "--new-window",
        DEEPSEEK_URL,
    ]

    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not _wait_debug_port():
        raise RuntimeError("Debug-port did not open in time")
