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

    s = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver


# # Path to the JSON file
# json_file_path = 'Backend_Scripts/localIP.json'
#
# # Read the JSON data from the file
# with open(json_file_path, 'r') as file:
#     json_data = json.load(file)
#
# # Extract IP addresses
# ip_addresses = [device["IP"] for device in json_data.values()]
#
# # List to store responsive IP addresses
# responsive_ips = []
#
#
# # Loop through each IP address
# for ip in ip_addresses:
#     url = f'http://{ip}'
#     try:
#         # Send a GET request to the IP address
#         response = requests.get(url, timeout=5)
#         # Check if the request was successful
#         if response.status_code == 200:
#             print(f'Successfully accessed {url}')
#             responsive_ips.append(ip)
#             print(f'total list of responsive ips is {responsive_ips}')
#         else:
#             print(f'Failed to access {url} - Status code: {response.status_code}')
#     except requests.exceptions.RequestException as e:
#         # Handle any exceptions that occur
#         print(f'Error accessing {url} - {e}')



def attempt_login(driver, ip):
    print("Currently attempting to log in to", ip)
    global last_tried_password
    try:
        driver.get(f'http://{ip}')
        sleep(1)
        potential_passwords = ["pass", "pass1", "pass2", "IPROSECURE", "IPROsecure", "am i there yet"]
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")

        for password in potential_passwords:
            try:
                login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
                password_field.clear()
                password_field.send_keys(password)
                login_button.click()
                last_tried_password = password
                WebDriverWait(driver, 1).until(EC.invisibility_of_element(login_button))
                print(f"Success with password: {password}")
                return True
            except TimeoutException:
                print(f"Failed with password: {password}")
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

    password_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
    found_password_fields = False

    # Loop until password fields are found or a maximum number of attempts is reached
    max_attempts = 10
    attempts = 0
    while not found_password_fields and attempts < max_attempts:
        find_clickable_ancestor_and_click("//*[contains(text(), 'Admin Password')]/..")
        attempts += 1

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
    sleep(15)



def find_clickable_ancestor_and_click(start_element_xpath):
    max_attempts = 10  # Prevents infinite loops
    attempts = 0
    current_element_xpath = start_element_xpath

    # WebDriverWait(driver, 1).until(EC.invisibility_of_element(password_field))
    while attempts < max_attempts: # Searches for the desired element, opening menus to search for it
        try:
            # Try finding the current element
            element = driver.find_element(By.XPATH, current_element_xpath)
            # Attempt to click the element
            element.click()
            sleep(1)
            print("Clicked on element:", current_element_xpath)
            return True  # Successfully clicked
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

#
# for ip in responsive_ips:
#     if attempt_login(driver, ip):
#         find_pass_reset_page()
# driver.quit()

