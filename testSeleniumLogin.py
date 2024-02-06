import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def test_keep_browser_open():
    options = webdriver.ChromeOptions()

    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get('https://practicetestautomation.com/practice-test-login/')

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys(actual_username)
    password_field.send_keys(actual_password)

    # WebElement?

    loginButton = driver.find_element(By.ID, "submit")
    loginButton.click();

    userInput = input("Press 1 then enter")
    while (userInput != "1"):
        pass

    driver.quit()

actual_username = "student"
actual_password = "Password123"
test_keep_browser_open()