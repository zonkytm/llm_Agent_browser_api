import os
import shutil
import socket
import subprocess
import time
from config import CHROME_PATH, DEBUG_PORT, DEBUG_PROFILE_ROOT, ORIGINAL_PROFILE
from logger import Colors, log

def copy_profile():
    """Initialize and save Chrome profile for LLM authentication"""
    log("Initializing LLM profile...", Colors.CYAN)
    
    # Clean previous profile
    if os.path.exists(DEBUG_PROFILE_ROOT):
        shutil.rmtree(DEBUG_PROFILE_ROOT, ignore_errors=True)
    
    # Create new profile directory
    os.makedirs(DEBUG_PROFILE_ROOT, exist_ok=True)
    
    # Copy essential profile data
    ignore = shutil.ignore_patterns(
        "History*", "Web Data*", "Login Data*", "Cookies*",
        "Visited Links*", "Current Session*", "Current Tabs*",
        "Last Session*", "Last Tabs*"
    )
    
    shutil.copytree(
        ORIGINAL_PROFILE,
        os.path.join(DEBUG_PROFILE_ROOT, "Default"),
        ignore=ignore,
        dirs_exist_ok=True
    )
    
    log("LLM profile initialized", Colors.GREEN)

def get_profile_path():
    """Return path to saved LLM profile"""
    return os.path.join(DEBUG_PROFILE_ROOT, "Default")