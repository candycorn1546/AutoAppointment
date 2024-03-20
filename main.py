import os
import time

from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def click_button(driver, text): # Clicks a button with the specified text
    buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
    )
    for button in buttons:
        if button.text.strip().lower().find(text) != -1:
            button.click()
            break


def wait_until_present(driver, by, locator): # Waits until an element is present
    return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((by, locator)))


def get_date_with_selenium(url, language='English'): # Gets the next available date and time
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument("--start-maximized")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36")
    options.add_argument('--no-sandbox')
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        buttons = wait_until_present(driver, By.TAG_NAME, "button") # Wait until the buttons are present
        language_found = False
        for button in buttons:
            if button.text.strip().lower() == language.lower():
                button.click()
                language_found = True
                break

        if not language_found:
            print(f"Language '{language}' not found.")
            return

        wait_until_present(driver, By.XPATH, "//div[@data-v-32f18d34]") # Wait until the div is present

        required_inputs = driver.find_elements(By.XPATH, "//input[@required]") # Find all required input fields
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

        all_filled = all(input_element.get_attribute("value") for input_element in required_inputs) # Check if all required input fields are filled

        if all_filled:
            click_button(driver, "log on")
            time.sleep(2)
            click_button(driver, "ok")
            click_button(driver, "log on")
        else:
            print("Not all required input fields are filled")

        time.sleep(5)
        click_button(driver, "new appointment") # Click the new appointment button
        click_button(driver, "service not listed or my license is not eligible") # Click the service not listed button
        click_button(driver, "no") # Click the no button

        interact_with_inputs(driver) # Interact with the input fields

        click_button(driver, "next") # Click the next button
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        date_elements = soup.find('div', string='Next Available Date') # Find the next available date
        next_date = date_elements.find_next_sibling(string=True).strip()
        div_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='pa-2 mx-3 my-3 text-center card blue lighten-2']"))
        )
        div_element.click() # Click the div element
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        date_elements = soup.find('div', class_='text-center font-weight-medium mt-5')
        appointment_time = date_elements.text.strip() # Get the appointment time
        return next_date, appointment_time # Return the next available date and time





    except TimeoutException:
        print("Timeout exception")

    finally:
        driver.quit()


def interact_with_inputs(driver): # Interacts with the input fields
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


def send_email(appointment_date, appointment_time): # Sends an email
    sender_email = "sendfrompysms@outlook.com"
    receiver_email = "vyfrommo@gmail.com"
    password = os.getenv("PASSWORD")

    if password is None:
        print("Error: Password not found in environment variables.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "NEW APPOINTMENT DATE AVAILABLE!"
    msg['X-Priority'] = '1'

    body = (f"New appointment date available: {appointment_date} at {appointment_time}!"
            f"\n\nGo to https://public.txdpsscheduler.com/ to schedule an appointment.")

    msg.attach(MIMEText(body, 'plain'))

    smtp_server = "smtp.office365.com"
    smtp_port = 587

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    load_dotenv() # Load environment variables
    url = 'https://public.txdpsscheduler.com/' # URL to check for appointments
    current_date = '4/17/2025' # Current date
    count = 0
    while count < 5:
        appointment_date, appointment_time = get_date_with_selenium(url)
        current_date = datetime.strptime(current_date, "%m/%d/%Y")
        appointment_date = datetime.strptime(appointment_date, "%m/%d/%Y")
        if appointment_date.date() < current_date.date(): # If the appointment date is earlier than the current date
            send_email(appointment_date.strftime('%Y-%m-%d'), appointment_time) # Send an email
            current_date = appointment_date # Update the current date

        time.sleep(300)
        count += 1
