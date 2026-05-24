from agent import init, run_turn
from browser import connect, copy_profile, kill_chrome, launch_chrome
from config import MODELS
from logger import Colors, log


def chat_loop(driver, model_name):
    log(f"\n{model_name.upper()} CODE AGENT READY\n", Colors.GREEN, bold=True)

    while True:
        try:
            user_input = input(f"{Colors.BOLD}{Colors.MAGENTA}Вы: {Colors.RESET}")

            if user_input.lower() in ("exit", "quit"):
                break

            if not user_input.strip():
                continue

            run_turn(driver, user_input, model_name)

        except Exception as e:
            log(f"\n❌ Error:\n{e}\n", Colors.RED)


def main():
    try:
        # Model selection
        print("\nAvailable models:")
        for key, model in MODELS.items():
            print(f"  - {key}: {model['name']}")
        
        model_choice = input("\nChoose model (deepseek/kimi/qwen): ").lower().strip()
        
        if model_choice not in MODELS:
            print("Invalid choice, defaulting to deepseek")
            model_choice = "deepseek"
            
        model_name = MODELS[model_choice]["name"]
        system_prompt = MODELS[model_choice]["system_prompt"]

        kill_chrome()
        copy_profile()
        launch_chrome(model_choice)
        driver = connect(model_choice)
        
        init(driver, system_prompt)
        chat_loop(driver, model_name)
    except Exception as e:
        log(f"\n❌ CRITICAL ERROR:\n{e}", Colors.RED, bold=True)

    input("\nPress ENTER to exit...")


if __name__ == "__main__":
    main()
