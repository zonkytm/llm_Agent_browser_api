from agent import init, run_turn
from browser import connect, copy_profile, kill_chrome, launch_chrome
from logger import Colors, log


def chat_loop(driver):
    log("\nDEEPSEEK CODE AGENT READY\n", Colors.GREEN, bold=True)

    while True:
        try:
            user_input = input(f"{Colors.BOLD}{Colors.MAGENTA}Вы: {Colors.RESET}")

            if user_input.lower() in ("exit", "quit"):
                break

            if not user_input.strip():
                continue

            run_turn(driver, user_input)

        except Exception as e:
            log(f"\n❌ Error:\n{e}\n", Colors.RED)


def main():
    try:
        kill_chrome()
        copy_profile()
        launch_chrome()
        driver = connect()
        init(driver)
        chat_loop(driver)
    except Exception as e:
        log(f"\n❌ CRITICAL ERROR:\n{e}", Colors.RED, bold=True)

    input("\nPress ENTER to exit...")


if __name__ == "__main__":
    main()
