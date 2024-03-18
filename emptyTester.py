import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup


def click_button(driver, text):
    buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
    )
    for button in buttons:
        if button.text.strip().lower().find(text) != -1:
            button.click()
            break


def wait_until_present(driver, by, locator):
    return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((by, locator)))


def get_date_with_selenium(url, language='English'):
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument("--start-maximized")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        buttons = wait_until_present(driver, By.TAG_NAME, "button")
        language_found = False
        for button in buttons:
            if button.text.strip().lower() == language.lower():
                button.click()
                language_found = True
                break

        if not language_found:
            print(f"Language '{language}' not found.")
            return

        wait_until_present(driver, By.XPATH, "//div[@data-v-32f18d34]")

        required_inputs = driver.find_elements(By.XPATH, "//input[@required]")
        for input_element in required_inputs:
            label_element = input_element.find_element(By.XPATH, "..//label")
            label_text = label_element.text.strip().lower()
            if "first name" in label_text:
                input_element.send_keys("John")
            elif "last name" in label_text:
                input_element.send_keys("Doe")
            elif "date of birth" in label_text:
                input_element.send_keys("01/01/2000")
            elif "last four of ssn" in label_text:
                input_element.send_keys("1234")

        all_filled = all(input_element.get_attribute("value") for input_element in required_inputs)

        if all_filled:
            click_button(driver, "log on")
        else:
            print("Not all required input fields are filled")

        time.sleep(5)
        click_button(driver, "new appointment")
        click_button(driver, "service not listed or my license is not eligible")
        click_button(driver, "no")

        interact_with_inputs(driver)

        click_button(driver, "next")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        date_elements = soup.find('div', string='Next Available Date')
        next_date = date_elements.find_next_sibling(string=True).strip()
        print(f"Next available date: {next_date}")




    except TimeoutException:
        print("Timeout exception")

    finally:
        driver.quit()


def interact_with_inputs(driver):
    time.sleep(10)
    menucards = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "menucard")))
    menucard = menucards[1]
    input_elements = menucard.find_elements(By.XPATH, ".//input")
    for input_element in input_elements:
        placeholder_text = input_element.get_attribute("placeholder")
        if placeholder_text == "#####":
            input_element.send_keys("75040")
            break
    required_inputs = driver.find_elements(By.XPATH, "//input[@required]")
    for input_element in required_inputs:
        label_element = input_element.find_element(By.XPATH, "..//label")
        label_text = label_element.text.strip()
        if "email" in label_text.lower():
            input_element.send_keys("temp@gmail.com")
        elif "verify email" in label_text.lower():
            input_element.send_keys("temp@gmail.com")
        elif "home phone" in label_text.lower():
            input_element.send_keys("4699105330")
    all_filled = True
    for input_element in required_inputs:
        if not input_element.get_attribute("value"):
            all_filled = False
            break
    if not all_filled:
        print("Some required fields are missing.")


if __name__ == '__main__':
    url = 'https://public.txdpsscheduler.com/'
    get_date_with_selenium(url)
