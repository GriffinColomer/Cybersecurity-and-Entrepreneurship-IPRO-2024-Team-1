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

def test_keep_browser_open():
    for password in potential_passwords:
        try:
            # Refresh the login page for each attempt
            # driver.refresh()
            # sleep(1)

            # Locate the password field and login button for each attempt

            login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")

            # Clear the password field before sending keys
            password_field.clear()
            password_field.send_keys(password)
            login_button.click()

            # Wait for the login button to disappear or any other login success indicator
            WebDriverWait(driver, 0).until(EC.invisibility_of_element(login_button))
            print(f"Success with password: {password}")
            break  # Exit the loop on success
        except TimeoutException:
            print(f"Failed with password: {password}")
        except NoSuchElementException:
            print("Login elements not found, checking next password or ending test.")
            break

    # find_clickable_ancestor_and_click("//span[contains(text(), 'Admin Password')]")
    # driver.find_element(By.XPATH, "//*[contains(text(), 'Admin Password')]/..")
    #this needs to run twice lmao
    find_clickable_ancestor_and_click("//*[contains(text(), 'Admin Password')]/..")
    find_clickable_ancestor_and_click("//*[contains(text(), 'Admin Password')]/..")

    reset_password()


    # Locate the element containing "Admin Password"
    # admin_password_span = driver.find_element(By.XPATH, "//span[contains(text(), 'Admin Password')]")

    # Navigate to a higher ancestor that is expected to be clickable.
    # This example uses `ancestor::li` to go up to the nearest <li> ancestor.
    # Adjust the tag name based on your specific case or use '*' for any element type.
    # clickable_ancestor = driver.find_element(By.XPATH, "//span[contains(text(), 'Admin Password')]/ancestor::li[1]")

    # Now, try clicking on the found ancestor
    # clickable_ancestor.click()

    userInput = input("Press 1 then enter to quit: ")
    while userInput != "1":
        pass

    driver.quit()


def reset_password():
    oldpass = "IPROsecure"
    newpass = "IPRO123"
    password_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")

    oldused = False
    for password_input in password_fields:
        if not oldused:
            password_input.send_keys(oldpass)
            oldused = True
            pass

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

test_keep_browser_open()