from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from imessage_reader import fetch_data
from datetime import date, timedelta
from selenium import webdriver
from pandas import *
import numpy as np
import requests
import hashlib
import time

PATH = "/Users/cfho/Desktop/git/Selenium/selenium/chromedriver"
GOOGLE_URL = "https://www.google.com/"
RANDOMMER_API_KEY = "89a27eb105ab432bbd02f9a2bb6212ff"
RANDOMMER_URL = "https://randommer.io/api/Name"
START_DATE = date(1950, 1, 1)
END_DATE = date(2005, 1, 1)

# get i number of full names, returns a json file
def get_names(i):
    randommer_headers = {
        "X-Api-Key": RANDOMMER_API_KEY
    }
    randommer_params = {
        "nameType": "fullname",
        "quantity": i
    }
    randommer_response = requests.get(url=RANDOMMER_URL, params=randommer_params, headers=randommer_headers)
    return randommer_response.json()

def get_dates(i):
    dates_bet = END_DATE - START_DATE
    total_days = dates_bet.days
    randays = np.random.choice(total_days, i, replace=False)
    res = [(START_DATE + timedelta(days=int(day))).strftime("%B/%d/%Y") for day in randays]
    return res

names = get_names(1)
name_parts = [name.split() for name in names]
first_names = [name[0] for name in name_parts]
last_names = [name[1] for name in name_parts]
name_hashes = [hashlib.sha256(name.encode()).hexdigest() for name in names]
usernames = [first_names[i]+last_names[i]+name_hashes[i][:4] for i in range(len(first_names))]
passwords = [name_hash[1:9] for name_hash in name_hashes]
birthdates = get_dates(1)

df = DataFrame({'First Name': first_names, 'Last Name': last_names, 'Username': usernames, 'Password': passwords, 'SHA-256 Hash': name_hashes, 'Birthdate':birthdates})
df.to_csv('data.csv', index=False)

data_csv = read_csv("data.csv")
data = { index : {"Username":row["Username"], "First Name":row["First Name"], "Last Name":row["Last Name"], "Password":row["Password"], 'Birthdate':row["Birthdate"]} for index, row in data_csv.iterrows()}

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.get(GOOGLE_URL)

sign_in_button = driver.find_element(By.XPATH, '//*[@id="gb"]/div/div[2]/a')
sign_in_button.click()
time.sleep(0.2)

create_account_button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div/button/span')
create_account_button.click()
time.sleep(0.2)

personal_use_button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div/ul/li[1]/span[2]')
personal_use_button.click()

first_name_field = driver.find_element(By.XPATH, '//*[@id="firstName"]')
first_name_field.send_keys(data[0]["First Name"])
last_name_field = driver.find_element(By.XPATH, '//*[@id="lastName"]')
last_name_field.send_keys(data[0]["Last Name"])
time.sleep(1)
next_button = driver.find_element(By.XPATH, '//*[@id="collectNameNext"]/div/button/span')
next_button.click()
time.sleep(1)

month_field = driver.find_element(By.XPATH, f'//*[@id="month"]/option[text()="{data[0]["Birthdate"].split("/")[0]}"]')
month_field.click()
day_field = driver.find_element(By.XPATH, '//*[@id="day"]')
day_field.send_keys(data[0]["Birthdate"].split("/")[1])
year_field = driver.find_element(By.XPATH, '//*[@id="year"]')
year_field.send_keys(data[0]["Birthdate"].split("/")[2])
gender_field = driver.find_element(By.XPATH, '//*[@id="gender"]/option[text()="Rather not say"]')
gender_field.click()

next_button = driver.find_element(By.XPATH, '//*[@id="birthdaygenderNext"]/div/button/span')
next_button.click()
time.sleep(1)

own_email_radio = driver.find_element(By.XPATH, '//*[@id="selectionc2"]')
own_email_radio.click()
email_field = driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input')
email_field.send_keys(data[0]['Username'])
next_button = driver.find_element(By.XPATH, '//*[@id="next"]/div/button/span')
next_button.click()
time.sleep(1)

password_field = driver.find_element(By.XPATH, '//*[@id="passwd"]/div[1]/div/div[1]/input')
password_field.send_keys(data[0]['Password'])
password_confirm_field = driver.find_element(By.XPATH, '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input')
password_confirm_field.send_keys(data[0]['Password'])
next_button = driver.find_element(By.XPATH, '//*[@id="createpasswordNext"]/div/button/span')
next_button.click()
time.sleep(1)

phone__field = driver.find_element(By.XPATH, '//*[@id="phoneNumberId"]')
phone__field.send_keys("")
next_button = driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div/div/div/button/span')
next_button.click()
time.sleep(10)


def sort_messages(sub_li):
    sub_li.sort(key = lambda x: x[2])
    return sub_li

DB_PATH = "/Users/cfho/Library/Messages/chat.db"
fd = fetch_data.FetchData(DB_PATH)
my_data = fd.get_messages()
messages = []
for data in my_data:
    messages.append(list(data))
messages = sort_messages(messages)
print(messages[-1:][0][1])

verification_field = driver.find_element(By.XPATH, '//*[@id="code"]')
verification_field.send_keys(messages[-1:][0][1])
next_button = driver.find_element(By.XPATH, '//*[@id="next"]/div/button/span')
next_button.click()