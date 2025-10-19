from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ---------------- CONFIGURATION ----------------
LOGIN_URL = "http://10.20.100.16:3081/login"
UPLOAD_URL = "http://10.20.100.16:3081/order/hm"

USER_ID = "101846"
PASSWORD = "101846"

PDF_FILES = [
    r"C:\Users\forhad.ahmed\Downloads\h_m\202282_PurchaseOrder_20240903_075305.PDF",
    r"C:\Users\forhad.ahmed\Downloads\h_m\202282_SizePerColourBreakdown_20240903_075305.PDF",
    r"C:\Users\forhad.ahmed\Downloads\h_m\202282_TotalCountryBreakdown_20240903_075305.PDF"
]

EMAIL_SELECTOR = "input[name='userId']"
PASSWORD_SELECTOR = "input[name='password']"
LOGIN_BUTTON_SELECTOR = "button[type='submit']"

UPLOAD_SELECTOR = "input[type='file']"
EXTRACTION_DONE_SELECTOR = "div.success"
SUBMIT_BUTTON_SELECTOR = "button#submit"

TIMEOUT = 30


def login_and_upload_pdfs():
    # Initialize Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        # ---------- LOGIN ----------
        driver.get(LOGIN_URL)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EMAIL_SELECTOR))).send_keys(USER_ID)
        driver.find_element(By.CSS_SELECTOR, PASSWORD_SELECTOR).send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR).click()

        # Wait until URL changes or some post-login element appears
        wait.until(lambda d: d.current_url != LOGIN_URL)
        print("✅ Login successful")

        # ---------- NAVIGATE DIRECTLY TO UPLOAD PAGE ----------
        driver.get(UPLOAD_URL)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, UPLOAD_SELECTOR)))
        print("✅ Navigated to upload page")

        # ---------- UPLOAD PDFs ----------
        upload_input = driver.find_element(By.CSS_SELECTOR, UPLOAD_SELECTOR)
        upload_input.send_keys("\n".join(PDF_FILES))  # Upload all PDFs
        print(f"✅ Uploaded {len(PDF_FILES)} PDFs")

        # ---------- WAIT FOR EXTRACTION ----------
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, EXTRACTION_DONE_SELECTOR)))
        print("✅ PDF extraction completed")

        # ---------- CLICK SUBMIT ----------
        driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR).click()
        print("✅ Submission completed")

        # Optional: wait a few seconds to ensure process completes
        time.sleep(2)

    finally:
        driver.quit()


if __name__ == "__main__":
    login_and_upload_pdfs()
