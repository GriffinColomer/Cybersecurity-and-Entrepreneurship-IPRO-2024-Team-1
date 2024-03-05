from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def has_password_field(IP, driver):
    url = f'http://{IP}'
    try:
        driver.get(url)
        # Wait for the page to load
        sleep(2)
        # Check for the presence of a password input field
        password_field = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        if password_field:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    s = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver

# Example usage
driver = init_driver()
IP = "192.168.1.1"
print(has_password_field(IP, driver))
driver.quit()
