from time import sleep

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def test_keep_browser_open():
    options = webdriver.ChromeOptions()

    options.add_experimental_option("detach", True)



    driver = webdriver.Chrome(options=options)
    driver.get('http://192.168.8.1')
    sleep(1)

    # username_field = driver.find_element(By.ID, "username")
    # password_field = driver.find_element(By.ID, "password")
    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    # username_field.send_keys(actual_username)
    password_field.send_keys(actual_password)

    # WebElement?

    # loginButton = driver.find_element(By.ID, "submit")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
    login_button.click()
    sleep(1)

    # Use XPath to find the <span> element by text, then navigate to its parent
    admin_password_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Admin Password')]/..")

    # To interact with the button, for example, clicking it
    admin_password_button.click()

    userInput = input("Press 1 then enter")
    while (userInput != "1"):
        pass

    driver.quit()

# actual_username = "student"
potential_passwords = ["pass","pass1","pass2","IPROSECURE","IPROsecure"]
actual_password = "IPROsecure"
test_keep_browser_open()
