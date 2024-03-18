import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup


def get_date_with_selenium(url, language='English'):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
        )

        language_found = False
        for button in buttons:
            if button.text.strip().lower() == language.lower():
                button.click()
                language_found = True
                break

        if not language_found:
            print(f"Language '{language}' not found.")
            return

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-v-32f18d34]")))

        required_inputs = driver.find_elements(By.XPATH, "//input[@required]")
        for input_element in required_inputs:
            label_element = input_element.find_element(By.XPATH, "..//label")
            label_text = label_element.text.strip()
            if "first name" in label_text.lower():
                input_element.send_keys("John")
            elif "last name" in label_text.lower():
                input_element.send_keys("Doe")
            elif "date of birth" in label_text.lower():
                input_element.send_keys("01/01/2000")
            elif "last four of ssn" in label_text.lower():
                input_element.send_keys("1234")

        all_filled = all(input_element.get_attribute("value") for input_element in required_inputs)

        if all_filled:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                 "//button[@class='button white--text v-btn v-btn--contained theme--light v-size--default public-blue button-normal']")))
            if button.is_enabled():
                button.click()
            else:
                print("Button is not enabled")
        else:
            print("Not all required input fields are filled")

        time.sleep(5)
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
        )
        for button in buttons:
            if button.text.strip().lower() == "new appointment":
                button.click()
                break

        WebDriverWait(driver, 10).until(EC.staleness_of(button))
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
        )
        for button in buttons:
            if button.text.strip().lower() == "service not listed or my license is not eligible":
                button.click()
                break

        WebDriverWait(driver, 10).until(EC.staleness_of(button))
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
        )
        for button in buttons:
            if button.text.strip().lower() == "no":
                button.click()
                break

        WebDriverWait(driver, 10).until(EC.staleness_of(button))
        interact_with_inputs(driver)
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
        )
        for button in buttons:
            if button.text.strip().lower().find("next") != -1:
                button.click()
                break
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        date_elements = soup.find('div', string='Next Available Date')
        next_date = date_elements.find_next_sibling(string=True).strip()
        return next_date

    except TimeoutException:
        print("Timeout exception")



    finally:
        # driver.quit()
        pass


def interact_with_inputs(driver):
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
    print(get_date_with_selenium(url))
