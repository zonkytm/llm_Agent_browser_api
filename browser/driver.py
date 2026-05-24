import time

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config import DEBUG_PORT
from logger import Colors, log


# ── selectors ────────────────────────────────────────────────────────────────

INPUT_SELECTORS = [
    'div[contenteditable="true"]',
    "textarea",
    '[role="textbox"]',
    ".ql-editor",
    ".ProseMirror",
]

RESPONSE_SELECTORS = [
    ".ds-assistant-message-main-content",
    ".ds-markdown",
    '[class*="assistant-message"]',
    '[class*="message-content"]',
    '[class*="markdown"]',
    ".message-content",
    ".chat-message-content",
]

THINKING_SELECTORS = [
    '[class*="thinking"]',
    '[class*="loading"]',
    '[class*="generating"]',
    ".ds-spinner",
    '[class*="spinner"]',
    '[class*="dots"]',
    'svg[class*="spin"]',
]


from urllib.parse import urlparse

# ── connect ───────────────────────────────────────────────────────────────────

def connect(model_choice: str) -> webdriver.Chrome:
    log(f"Connecting Selenium for {model_choice}...", Colors.CYAN)
    try:
        chromedriver_autoinstaller.install()
    except Exception as e:
        log(f"Warning: chromedriver-autoinstaller failed: {e}. Attempting to continue...", Colors.YELLOW)

    options = Options()
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{DEBUG_PORT}")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options)
    _wait_for_tab(driver, model_choice)
    _wait_for_input(driver)

    log("Selenium connected", Colors.GREEN)
    return driver


def _wait_for_tab(driver: webdriver.Chrome, model_choice: str, timeout=20):
    from config import MODELS
    target_url = MODELS.get(model_choice, {}).get("url", "")
    
    # Keyword for matching (e.g., 'kimi' from 'kimi.la' or 'deepseek' from 'deepseek.com')
    keyword = model_choice.lower()
    
    log(f"Looking for tab containing '{keyword}'...", Colors.CYAN)
    for _ in range(timeout * 2):
        for handle in driver.window_handles:
            try:
                driver.switch_to.window(handle)
                url = driver.execute_script("return window.location.href").lower()
                if keyword in url:
                    return
            except Exception:
                pass
        time.sleep(0.5)
    raise RuntimeError(f"Tab for {model_choice} (keyword: {keyword}) not found")


def _wait_for_input(driver: webdriver.Chrome, attempts=40):
    log("Waiting for input ready...", Colors.CYAN)
    for _ in range(attempts):
        el = find_input(driver)
        if el and el.is_displayed():
            return
        time.sleep(0.5)


# ── input helpers ─────────────────────────────────────────────────────────────

def find_input(driver: webdriver.Chrome):
    for selector in INPUT_SELECTORS:
        for el in driver.find_elements(By.CSS_SELECTOR, selector):
            try:
                if el.is_displayed() and el.is_enabled() and el.rect["height"] >= 20:
                    return el
            except Exception:
                pass

    # fallback: placeholder / aria-label
    for div in driver.find_elements(By.TAG_NAME, "div"):
        try:
            combined = (
                (div.get_attribute("placeholder") or "") + " " +
                (div.get_attribute("aria-label") or "")
            ).lower()
            if "message" in combined or "deepseek" in combined:
                return div
        except Exception:
            pass

    return None


def insert_text(driver: webdriver.Chrome, text: str):
    el = find_input(driver)
    if not el:
        raise RuntimeError("Input not found before insert")

    driver.execute_script("arguments[0].focus();", el)
    time.sleep(0.3)

    is_contenteditable = driver.execute_script(
        "return arguments[0].contentEditable === 'true';", el
    )

    if is_contenteditable:
        driver.execute_script(
            """
            const el = arguments[0], text = arguments[1];
            el.focus();
            el.innerText = '';
            el.dispatchEvent(new InputEvent('input', {bubbles:true, cancelable:true, inputType:'deleteContentBackward'}));
            el.innerText = text;
            const range = document.createRange(), sel = window.getSelection();
            range.selectNodeContents(el);
            range.collapse(false);
            sel.removeAllRanges();
            sel.addRange(range);
            el.dispatchEvent(new Event('focus', {bubbles:true}));
            el.dispatchEvent(new InputEvent('input', {bubbles:true, cancelable:true, inputType:'insertText', data:text}));
            el.dispatchEvent(new Event('change', {bubbles:true}));
            """,
            el, text,
        )
    else:
        driver.execute_script(
            """
            const el = arguments[0];
            const niv = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            niv.call(el, arguments[1]);
            el.dispatchEvent(new Event('input', {bubbles:true}));
            el.dispatchEvent(new Event('change', {bubbles:true}));
            """,
            el, text,
        )

    time.sleep(0.5)

    fresh = find_input(driver)
    if not fresh:
        raise RuntimeError("Input disappeared after insert")

    current = driver.execute_script(
        "return arguments[0].textContent || arguments[0].value || '';", fresh
    )
    if len(current.strip()) < 1:
        raise RuntimeError("Text not inserted")


def send_message(driver: webdriver.Chrome, text: str):
    log("\nSending message...\n", Colors.CYAN)

    # wait for input
    for _ in range(20):
        if find_input(driver):
            break
        time.sleep(0.5)
    else:
        raise RuntimeError("DeepSeek input not found")

    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", find_input(driver))
    except Exception:
        pass

    time.sleep(0.5)
    insert_text(driver, text)
    log("Text inserted", Colors.GREEN)
    time.sleep(0.5)

    try:
        find_input(driver).click()
    except Exception:
        pass

    time.sleep(0.3)
    _submit(driver)
    time.sleep(3)


def _submit(driver: webdriver.Chrome):
    # attempt 1: newline key
    try:
        find_input(driver).send_keys("\n")
        return
    except Exception:
        pass

    # attempt 2: JS keyboard event
    try:
        driver.execute_script(
            """
            arguments[0].dispatchEvent(new KeyboardEvent('keydown', {
                bubbles:true, cancelable:true,
                key:'Enter', code:'Enter', which:13, keyCode:13
            }));
            """,
            find_input(driver),
        )
        return
    except Exception:
        pass

    # attempt 3: submit button by selector
    try:
        btn = driver.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="Send message"], button[type="submit"], button.send-button',
        )
        btn.click()
        return
    except Exception:
        pass

    # attempt 4: any visible button with send/svg
    try:
        driver.execute_script(
            """
            for (const btn of document.querySelectorAll('button')) {
                const r = btn.getBoundingClientRect();
                if (r.width > 0 && r.height > 0) {
                    const t = (btn.textContent || '').toLowerCase();
                    const a = (btn.getAttribute('aria-label') || '').toLowerCase();
                    if (t.includes('send') || a.includes('send') || btn.querySelector('svg')) {
                        btn.click(); break;
                    }
                }
            }
            """
        )
    except Exception:
        pass
