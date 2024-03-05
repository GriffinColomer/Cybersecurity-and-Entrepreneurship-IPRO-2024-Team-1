from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def has_password_field(driver, ip):
    print("Currently attempting to log in to", ip)
    try:
        driver.get(f'http://{ip}')
        sleep(1)
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")

        if password_field:
            print('password field found')
            return True
        else:
            print('password field not found')
            return False
    except Exception as e:
        print(f"An error occurred while attempting to log in to {ip}: {e}")
        return False


def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    s = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver

#pass in an ip and it will try to find the password field
driver = init_driver()
print("Method has begun to try to reset password of ", '192.168.8.1')
has_password_field(driver, '192.168.8.1')
driver.quit()

