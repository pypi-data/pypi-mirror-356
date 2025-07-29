from .imports_and_instrument_token import *

def upstox_auth_code():
    # Inputs
    client_id = creds["auth"]["client_id"]
    client_pass = creds["auth"]["client_pass"]
    client_pin = creds["auth"]["client_pin"]

    url = (
        "https://api-v2.upstox.com/login/authorization/dialog?"
        "response_type=code&client_id=247b0045-94bc-4733-b3df-1452102032aa"
        "&redirect_uri=https://www.tradewithamit.com"
    )

    # Setup Chrome
    options = Options()
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for page to load
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

# Step 1: Enter Mobile Number
    username_input_xpath = '//*[@id="mobileNum"]'
    username_input_element = driver.find_element(By.XPATH, username_input_xpath)
    username_input_element.clear()
    username_input_element.send_keys(client_id)
    
    # Step 2: Press Get OTP button
    get_otp_button_xpath = '//*[@id="getOtp"]'
    get_otp_element = driver.find_element(By.XPATH, get_otp_button_xpath)
    get_otp_element.click()

# Step 3: Enter TOTP
    client_pass = pyotp.TOTP(client_pass).now()
    password_input_xpath = '//*[@id="otpNum"]'
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, password_input_xpath))
)
    password_input_element = driver.find_element(By.XPATH, password_input_xpath)
    password_input_element.clear()
    password_input_element.send_keys(client_pass)
    
    # Step 4: Press Continue button
    continue_button_xpath = '//*[@id="continueBtn"]'
    continue_button_element = driver.find_element(By.XPATH, continue_button_xpath)
    continue_button_element.click()

# Step 5: Enter PIN
    pin_input_xpath = '//*[@id="pinCode"]'
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, pin_input_xpath))
)
    pin_input_element = driver.find_element(By.XPATH, pin_input_xpath)
    pin_input_element.clear()
    pin_input_element.send_keys(client_pin)

    # Step 6: Get the Original URL
    original_url = driver.current_url

    # Step 7: Press the Continue button
    pin_continue_button_xpath = '//*[@id="pinContinueBtn"]'
    pin_continue_button_element = driver.find_element(By.XPATH, pin_continue_button_xpath)
    pin_continue_button_element.click()

# Step 8: Wait for redirect & get auth code
    WebDriverWait(driver, 30).until(EC.url_changes(original_url))
    redirected_url = driver.current_url
    redirected_url = redirected_url.split("?code=")
    code_for_auth = redirected_url[1]
    print(code_for_auth)

    driver.quit()

    return code_for_auth