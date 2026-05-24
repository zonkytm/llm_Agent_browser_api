import os
import shutil
import socket
import subprocess
import time

from config import CHROME_PATH, DEBUG_PORT, DEBUG_PROFILE_ROOT, MASTER_PROFILE, MODELS
from logger import Colors, log


def kill_chrome():
    log("☠ Killing Chrome...", Colors.YELLOW)
    os.system("taskkill /F /IM chrome.exe >nul 2>&1")
    time.sleep(2)


def copy_profile():
    log("Copying Master Profile to Debug...", Colors.CYAN)

    if not os.path.exists(MASTER_PROFILE):
        log(f"⚠ Master Profile not found at {MASTER_PROFILE}. Creating empty one.", Colors.YELLOW)
        os.makedirs(MASTER_PROFILE, exist_ok=True)

    if os.path.exists(DEBUG_PROFILE_ROOT):
        # We try to remove only if it's not the same as MASTER_PROFILE (safety)
        if os.path.abspath(DEBUG_PROFILE_ROOT) != os.path.abspath(MASTER_PROFILE):
            shutil.rmtree(DEBUG_PROFILE_ROOT, ignore_errors=True)

    os.makedirs(DEBUG_PROFILE_ROOT, exist_ok=True)

    # We copy everything from Master to Debug. 
    # Usually, the profile is in the root or in "Default" subfolder.
    # Selenium's --user-data-dir expects the root where "Default" lives or the profile itself.
    
    # Check if Master has a "Default" folder
    master_default = os.path.join(MASTER_PROFILE, "Default")
    if os.path.exists(master_default):
        shutil.copytree(MASTER_PROFILE, DEBUG_PROFILE_ROOT, dirs_exist_ok=True)
    else:
        # If it doesn't, maybe the Master itself IS the profile data.
        # But Chrome usually creates a "Default" folder inside user-data-dir.
        shutil.copytree(MASTER_PROFILE, DEBUG_PROFILE_ROOT, dirs_exist_ok=True)

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


def launch_chrome(model_choice):
    url = MODELS.get(model_choice, {}).get("url", MODELS["deepseek"]["url"])
    log(f"Launching Chrome for {model_choice} at {url}...", Colors.CYAN)

    cmd = [
        CHROME_PATH,
        f"--remote-debugging-port={DEBUG_PORT}",
        "--remote-debugging-address=127.0.0.1",
        f"--user-data-dir={DEBUG_PROFILE_ROOT}",
        "--new-window",
        url,
    ]

    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not _wait_debug_port():
        raise RuntimeError("Debug-port did not open in time")
