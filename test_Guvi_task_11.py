# Import required libraries
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Helper function: Launch browser
# This function is reused in all test cases
def launch_browser():
    service =Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver

# TEST CASE 1: Validate Login Button URL
def test_valid_url():  # Test to validate that clicking the Login button redirects the user to the Sign-in page
    driver = launch_browser()
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.guvi.in/") #open guvi homepage
    log_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    ) # click on login button
    log_btn.click()

    wait.until(EC.url_contains("sign-in")) # Validate that URL contains 'sign-in'

    assert driver.current_url.startswith("https://www.guvi.in/sign-in")

    driver.quit() #Close Browser

# TEST CASE 2: Validate Username & Password Fields
def test_valid_input_field(): #Test to validate that Username and Password input fields are visible and enabled
    driver = launch_browser()
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.guvi.in/sign-in") ## Open Sign-in page directly

    # Locate Username and Password fields
    username = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    password = wait.until(EC.visibility_of_element_located((By.ID, "password")))


    # Assert fields are displayed and enabled
    assert username.is_displayed() and username.is_enabled()
    time.sleep(5)
    assert password.is_displayed() and password.is_enabled()

    driver.quit() #Close browser

# TEST CASE 3: Validate Submit Button
def test_validate_submit_button(): #Test to validate that Submit button is visible and enabled on login page
    driver = launch_browser()
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.guvi.in/sign-in/")

    # Locate Submit button
    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    )
    # Assert Submit button state
    assert submit_btn.is_displayed()
    assert submit_btn.is_enabled()

    driver.quit() #Close Browser


# TEST CASE 4:POSITIVE Login
def test_positive_login(): #Test to validate successful login using valid Username and Password
    driver = launch_browser()
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.guvi.in/sign-in/") #Launch Website

    # Enter valid credentials
    username = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    password = wait.until(EC.visibility_of_element_located((By.ID, "password")))

    username.send_keys()
    password.send_keys()

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    )
    submit_btn.click() # Click Submit

    time.sleep(3)


    # Assert login success by checking URL change
    assert "guvi" in driver.current_url.lower()

    driver.quit() #Close browser

# TEST CASE 5: NEGATIVE Login – Invalid Credentials
def test_login_invalid_credentials(): #Test to validate error message is displayed when invalid credentials are entered
    driver = launch_browser()
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.guvi.in/sign-in/") #launch browser

    # Enter invalid credentials
    username = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    password = wait.until(EC.visibility_of_element_located((By.ID, "password")))

    username.send_keys("invalid@gmail.com")
    password.send_keys("wrongpassword")

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    )
    submit_btn.click() #Click submit button

    time.sleep(2)

    # ASSERT 1: Error message shown
    error_msg = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "invalid-feedback"))
    )
    assert error_msg.is_displayed()

    # Validate user stays on login page
    assert "sign-in" in driver.current_url

    driver.quit() #close browser

# TEST CASE 6: NEGATIVE Login – Empty Credentials
def test_login_empty_credentials(): #Test to validate error message appears when Submit is clicked with empty fields
    driver = launch_browser()
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.guvi.in/sign-in/") #launch browser

    submit_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    )
    submit_btn.click() # Click Submit without entering data

    time.sleep(2)
    # Validate validation messages exist
    error_messages = driver.find_elements(By.CLASS_NAME, "invalid-feedback")
    assert len(error_messages) > 0

    driver.quit() #close browser


