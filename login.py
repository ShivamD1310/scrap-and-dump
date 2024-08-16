from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os


def main():
    # Fetch the credentials from environment variables
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    # Print the credentials for debugging purposes
    print(f"USERNAME: {username}")
    print(f"PASSWORD: {password}")

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(30)
    driver.get('https://www.screener.in/login/?')


    email = driver.find_element(By.NAME,'username')
    email.send_keys(username)

    pas = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[2]/form/div[2]/input')
    pas.send_keys(password)

    search = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[2]/form/button')
    search.click()


if __name__ == "__main__":
    main()
