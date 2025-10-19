from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ---------------- CONFIGURATION ----------------
SITE_URL = "https://beta.uicommercial.com/sign-in"  # 🔹 Replace with your login page URL
EMAIL_SELECTOR = "input[name='email']"
PASSWORD_SELECTOR = "input[name='password']"
LOGIN_BUTTON_SELECTOR = "button[type='submit']"

EMAIL = "ziaour@apexholdings.com"        # 🔹 Your login email
PASSWORD = "UIC_979400"         # 🔹 Your login password

HEADLESS = False  # Set True to run without opening Chrome
TIMEOUT = 15      # seconds to wait for elements
# ------------------------------------------------

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    if HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def login(driver):
    driver.get(SITE_URL)
    wait = WebDriverWait(driver, TIMEOUT)

    # Wait for and fill email
    email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EMAIL_SELECTOR)))
    email_input.clear()
    email_input.send_keys(EMAIL)

    # Wait for and fill password
    password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, PASSWORD_SELECTOR)))
    password_input.clear()
    password_input.send_keys(PASSWORD)

    # Click login button
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR)))
    login_button.click()

    # Optional: wait for a post-login element (e.g., dashboard)
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.dashboard")))


def main():
    driver = create_driver()
    try:
        login(driver)
        print("✅ Logged in successfully!")
        if not HEADLESS:
            print("Keeping browser open for 10 seconds...")
            time.sleep(100)
    except Exception as e:
        print("❌ Login failed:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
