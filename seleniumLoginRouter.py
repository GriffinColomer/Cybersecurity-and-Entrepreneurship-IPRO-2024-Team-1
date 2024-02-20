from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.get('http://192.168.8.1')
sleep(1)
potential_passwords = ["pass", "pass1", "pass2", "IPROSECURE", "IPROsecure", "am i there yet"]
password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
last_tried_password = ''

def crack_login_page():
    global last_tried_password
    for password in potential_passwords:
        try:
            # Locate the password field and login button for each attempt

            login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")

            # Clear the password field before sending keys
            password_field.clear()
            password_field.send_keys(password)
            login_button.click()
            last_tried_password = password

            # Wait for the login button to disappear or any other login success indicator
            WebDriverWait(driver, 0).until(EC.invisibility_of_element(login_button))
            print(f"Success with password: {password}")
            break  # Exit the loop on success
        except TimeoutException:
            print(f"Failed with password: {password}")
        except NoSuchElementException:
            print("Login elements not found, checking next password or ending test.")
            break

    print(f"Success with password: {last_tried_password}")


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



def find_clickable_ancestor_and_click(start_element_xpath):
    max_attempts = 10  # Prevents infinite loops
    attempts = 0
    current_element_xpath = start_element_xpath

    # WebDriverWait(driver, 1).until(EC.invisibility_of_element(password_field))
    while attempts < max_attempts:
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




crack_login_page()
find_pass_reset_page()
userInput = input("Press 1 then enter to quit: ")
while userInput != "1":
    pass

driver.quit()