import requests
import json
import subprocess
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

potential_passwords = ["pass", "pass1", "pass2", "IPROSECURE", "IPROsecure", "am i there yet"]
password_field = ''

last_tried_password = ''

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    chrome_options.add_argument("--window-size=1920x1080")

    s = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver


def attempt_login(driver, ip):
    print("Currently attempting to log in to", ip)
    global last_tried_password
    try:
        driver.get(f'http://{ip}')
        sleep(1)
        print("made it to the actual router page")
        potential_passwords = ["pass", "pass1", "IPROSECURE", "IPROsecure", "Password123"]
        potential_usernames = ["admin", "user", "student"]
        
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        # Try different methods to find the login button
        login_button = None
        login_button_selectors = [
            "//button[contains(text(), 'Login') or contains(text(), 'Submit')]",
            "//button",
            "button.login-btn",
            "//button[contains(text(), 'og')]",
            "//input[@type='submit']"
        ]
        
        for selector in login_button_selectors:
            try:
                login_button = driver.find_element(By.XPATH, selector)
                break
            except NoSuchElementException:
                pass
        
        if login_button is None:
            print("Login button not found.")
            return False
        
        # Check if username field exists
        try:
            for username in potential_usernames:
                username_field = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[type='username']")
                username_field.clear()
                for password in potential_passwords:
                    try:
                        username_field = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[type='username']")
                        username_field.clear()
                        login_button = driver.find_element(By.XPATH, selector)
                        
                        username_field.send_keys(username)
                        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                        password_field.clear()
                        password_field.send_keys(password)
                        login_button.click()
                        last_tried_password = password
                        
                        # Check for the presence of the popup
                        try:
                            WebDriverWait(driver, 1).until(EC.alert_is_present())
                            alert = driver.switch_to.alert
                            alert.accept()
                            print(f"Failed with username: {username} and password: {password}")
                        except TimeoutException:
                            # Check for the presence of a password field after the login attempt
                            try:
                                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
                                print(f"Failed with username: {username} and password: {password}")
                            except TimeoutException:
                                print(f"Success with username: {username} and password: {password}")
                                return True
                    except NoSuchElementException:
                        print("Login elements not found, checking next password or ending test.")
                        break
        except NoSuchElementException:
            print("No username field found. Proceeding with password attempts.")
            for password in potential_passwords:
                try:
                    password_field.clear()
                    password_field.send_keys(password)
                    login_button.click()
                    last_tried_password = password
                    
                    # Check for the presence of the popup
                    try:
                        WebDriverWait(driver, 3).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        print(f"Failed with password: {password}")
                    except TimeoutException:
                        # Check for the presence of a password field after the login attempt
                        try:
                            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
                            print(f"Failed with password: {password}")
                        except TimeoutException:
                            print(f"Success with password: {password}")
                            return True
                except NoSuchElementException:
                    print("Login elements not found, checking next password or ending test.")
                    break
        return False
    except NoSuchElementException as e:
        print(f"Could not find the password field on {ip}: {e}")
        return False
    except Exception as e:
        print(f"An error occurred while attempting to log in to {ip}: {e}")
        return False

def find_pass_reset_page():
    driver.save_screenshot("screenshot_loggedin.png")
    password_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
    found_password_fields = False

    # Loop until password fields are found or a maximum number of attempts is reached
    max_attempts = 40
    attempts = 0

    while not found_password_fields and attempts < max_attempts:
        # Search for elements containing the text "Security", "Admin Password", "Reset Password", or "Change Password"
        elements_to_click = [
            "//*[contains(text(), 'Security')]/..",
            "//*[contains(text(), 'Admin Password')]/..",
            "//*[contains(text(), 'Reset Password')]/..",
            "//*[contains(text(), 'Change Password')]/.."
        ]

        for element_xpath in elements_to_click:
            if find_clickable_ancestor_and_click(element_xpath):
                attempts += 1
                break

        # Check if password fields are now visible
        password_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        if len(password_fields) > 0:
            found_password_fields = True
            WebDriverWait(driver, 1).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "input[type='password']")))
            reset_password()
        else:
            # Wait a bit before trying again
            sleep(1)

    if not found_password_fields:
        print("Failed to find password fields after multiple attempts.")


def reset_password():
    global last_tried_password
    sleep(0.2)
    oldpass = last_tried_password
    newpass = "IPRO123"
    password_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")

    oldused = False
    for password_input in password_fields:
        if not oldused:
            password_input.send_keys(oldpass)
            oldused = True
            pass
        else:
            password_input.send_keys(newpass)
    driver.save_screenshot("screenshot_passinserted.png")
    sleep(15)



def find_clickable_ancestor_and_click(start_element_xpath):
    max_attempts = 6  # Prevents infinite loops
    attempts = 0
    current_element_xpath = start_element_xpath

    while attempts < max_attempts:  # Searches for the desired element, opening menus to search for it
        try:
            # Store the current URL before clicking
            current_url = driver.current_url

            # Try finding the current element
            element = driver.find_element(By.XPATH, current_element_xpath)
            # Attempt to click the element
            element.click()
            sleep(1)

            # Check if the URL has changed after clicking
            if driver.current_url != current_url:
                print("Clicked on element:", current_element_xpath)
                print("Page redirected after clicking the element.")
                return True  # Successfully clicked and page redirected
            else:
                print("Clicked on element:", current_element_xpath)
                print("Page did not redirect after clicking the element.")
                return False  # Successfully clicked but page did not redirect

        except ElementNotInteractableException:
            # If element is not interactable, modify the XPath to move up to the ancestor
            current_element_xpath += "/.."
            attempts += 1
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break  # Exit on other unexpected errors

    print("Failed to find an interactable ancestor.")
    return False


#pass in an ip and it will try to change the password
driver = init_driver()
def auto_reset_pass(ip):
    print("Method has begun to try to reset password of ", ip)
    if attempt_login(driver, ip):
        find_pass_reset_page()
    driver.quit()


auto_reset_pass('192.168.8.1')
