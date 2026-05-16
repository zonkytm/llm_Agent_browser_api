import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from browser.driver import RESPONSE_SELECTORS, THINKING_SELECTORS
from logger import Colors, log


def get_last_response_el(driver: webdriver.Chrome):
    for selector in RESPONSE_SELECTORS:
        try:
            els = driver.find_elements(By.CSS_SELECTOR, selector)
            if els:
                return els[-1]
        except Exception:
            pass
    return None


def is_generating(driver: webdriver.Chrome) -> bool:
    for selector in THINKING_SELECTORS:
        for el in driver.find_elements(By.CSS_SELECTOR, selector):
            try:
                if el.is_displayed():
                    return True
            except Exception:
                pass

    for btn in driver.find_elements(By.CSS_SELECTOR, 'button[aria-label*="Stop"], button[aria-label*="stop"]'):
        try:
            if btn.is_displayed():
                return True
        except Exception:
            pass

    try:
        result = driver.execute_script(
            """
            for (const btn of document.querySelectorAll('button')) {
                const t = (btn.textContent || '').toLowerCase().trim();
                if (t === 'stop' || t === 'остановить') return true;
            }
            return false;
            """
        )
        if result:
            return True
    except Exception:
        pass

    return False


def stream_response(driver: webdriver.Chrome) -> str:
    printed_text = ""
    stable_ticks = 0
    got_first_char = False

    STABLE_TICKS_NEEDED = 10   # ~3 sec of stability (tick = 0.3 sec)
    MAX_WAIT_START = 60
    MAX_TOTAL = 300

    start_time = time.time()

    while True:
        time.sleep(0.3)
        elapsed = time.time() - start_time

        if elapsed > MAX_TOTAL:
            log("\n⚠ MAX_TOTAL exceeded\n", Colors.YELLOW)
            break

        el = get_last_response_el(driver)

        if el is None:
            if not got_first_char and elapsed > MAX_WAIT_START:
                log("\n⚠ No response element found\n", Colors.YELLOW)
                break
            continue

        try:
            current_text = driver.execute_script(
                "return arguments[0].innerText || arguments[0].textContent || '';", el
            )
        except Exception:
            continue

        current_text = (current_text or "").strip()

        if current_text and not got_first_char:
            got_first_char = True

        if not got_first_char:
            if elapsed > MAX_WAIT_START:
                log("\n⚠ Timeout waiting for first char\n", Colors.YELLOW)
                break
            continue

        if len(current_text) > len(printed_text):
            print(current_text[len(printed_text):], end="", flush=True)
            printed_text = current_text
            stable_ticks = 0
        else:
            if is_generating(driver):
                stable_ticks = 0
            else:
                stable_ticks += 1
                if stable_ticks >= STABLE_TICKS_NEEDED:
                    break

    print("\n")
    return printed_text
