import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(filename="app.log", level=logging.DEBUG)
BOT_TOKEN = os.getenv('BOT_TOKEN')


def sent_telegram(mess, chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={mess}"
    requests.get(url)  # відправляє повідомлення


def get_medoc_version():
    url = 'https://medoc.ua/download'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    version_element = soup.find('span', class_='date')
    if version_element:
        return version_element.text.strip()
    else:
        logging.error("Version element not found")
        return None


if __name__ == "__main__":
    string_date = get_medoc_version()

    if string_date:
        with open('data_value.txt', 'r') as file:
            previous_date = file.read().strip()
            date_object = datetime.strptime(previous_date, "%d.%m.%Y")

        if datetime.strptime(string_date, "%d.%m.%Y") != date_object:
            with open('data_value.txt', 'w', encoding='utf-8') as file:
                file.write(string_date)
            sent_telegram(f'New version of medoc {string_date}', "344289734")


# from datetime import datetime
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# TOKEN = "609113382:AAF4OABFmQ_cwDGqwoXSdSjeqVV8rUsRXB0"
#
#
# def sent_telegram(mess, chat_id):
#     url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={mess}"
#     # print(requests.get(url).json())  # this sends the message
#
#
# if __name__ == "__main__":
#     driver = webdriver.Chrome()
#     driver.get('https://medoc.ua/download')
#
#     version_locator = (
#         '/html/body/div/section/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div[1]/div[1]/div[2]/div['
#         '2]/a/span[2]')
#
#     version_locator_data = driver.find_element(By.XPATH, version_locator)
#     string_date = version_locator_data.text
#
#     with open('data_value.txt', 'r') as file:
#         previous_date = file.read().strip()
#         date_object = datetime.strptime(previous_date, "%d.%m.%Y")
#         # print(version_locator_data.text)
#
#     if datetime.strptime(string_date, "%d.%m.%Y") == date_object:
#         pass
#     else:
#         with open('data_value.txt', 'w', encoding='utf-8') as file:
#             file.write(string_date)
#             sent_telegram('New version of medoc ' + string_date, "344289734")
