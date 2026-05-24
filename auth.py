import subprocess
import time
from config import CHROME_PATH, MASTER_PROFILE, MODELS
from browser.launcher import kill_chrome
from logger import Colors, log

def run_auth():
    log("Starting Auth Mode...", Colors.CYAN, bold=True)
    kill_chrome()
    
    log(f"Using Master Profile: {MASTER_PROFILE}", Colors.YELLOW)
    log("Opening all LLM sites for authentication...", Colors.CYAN)
    
    urls = [model["url"] for model in MODELS.values()]
    
    cmd = [
        CHROME_PATH,
        f"--user-data-dir={MASTER_PROFILE}",
        "--new-window",
    ] + urls
    
    log(f"Executing: {' '.join(cmd)}", Colors.CYAN)
    subprocess.Popen(cmd)
    
    log("\n" + "="*50, Colors.GREEN)
    log("AUTH MODE ACTIVE", Colors.GREEN, bold=True)
    log("1. Log in to all opened LLM sites.", Colors.GREEN)
    log("2. Close the browser window when finished.", Colors.GREEN)
    log("="*50 + "\n", Colors.GREEN)

if __name__ == "__main__":
    run_auth()
