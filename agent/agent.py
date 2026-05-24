from selenium import webdriver

from browser.driver import send_message
from browser.response import stream_response
from logger import Colors, log
from tools import execute


MAX_TOOL_ROUNDS = 10


def init(driver: webdriver.Chrome, system_prompt: str):
    log("\nInitializing agent...\n", Colors.CYAN, bold=True)
    send_message(driver, system_prompt)
    stream_response(driver)
    log("\n✅ Agent initialized\n", Colors.GREEN, bold=True)


def run_turn(driver: webdriver.Chrome, user_input: str, model_name: str):
    send_message(driver, user_input)
    print(f"\n{Colors.BOLD}{Colors.GREEN}{model_name}:{Colors.RESET}\n", end="", flush=True)
    response = stream_response(driver)

    for _ in range(MAX_TOOL_ROUNDS):
        tool_result = execute(response)
        if not tool_result:
            break

        log("\n=============== TOOL RESULT ===============\n", Colors.CYAN)
        print(tool_result)

        send_message(driver, tool_result)
        print(f"\n{Colors.BOLD}{Colors.GREEN}{model_name}:{Colors.RESET}\n", end="", flush=True)
        response = stream_response(driver)
