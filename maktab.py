from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from time import sleep
from dotenv import load_dotenv
import os
import requests


# import re


class Course:
    def __init__(self, url, course_name, user, password):
        self.user = user
        self.password = password
        self.url = url
        self.name = course_name
        self.all_links = []

        self.driver = webdriver.Chrome()
        self.driver.get(self.url)

    def login(self):
        delay = 10  # seconds
        try:
            WebDriverWait(self.driver, delay).until(ec.presence_of_element_located((By.ID, 'login'))).click()
            user = WebDriverWait(self.driver, delay).until(ec.presence_of_element_located((By.ID, 'tessera')))
            user.send_keys(self.user)
            user.send_keys(Keys.ENTER)
            password = WebDriverWait(self.driver, delay).until(ec.presence_of_element_located((By.ID, 'password')))
            password.send_keys(self.password)
            password.send_keys(Keys.ENTER)
            print("[Success] Logged in successfully!")
        except TimeoutException:
            print("[Error] Logging in took too much time...")

    def get_ep_links(self):
        sleep(10)
        print('[Getting Links] Saving all eps links...')
        all_sections = self.driver.find_elements(
            By.XPATH, '//*[@id="__layout"]/section/section/section/section[2]/div/div/div/section/div/div/div')
        for i, se in enumerate(all_sections, 1):
            # Uncomment to download season 4 and more
            # if i > 3:
                title = se.find_element(
                    By.XPATH,
                    f'//*[@id="__layout"]/section/section/section/section[2]/div/div/div/section/div/div/div[{i}]/section/div/div/div[1]/span[2]').text
                print(title)
                self.all_links.append((title, [
                    j.get_attribute("href") for j in (se.find_elements(
                        By.XPATH,
                        f'//*[@id="__layout"]/section/section/section/section[2]/div/div/div/section/div/div/div[{i}]/div/a'))
                ]))
        print('[Getting Links] Saved all eps links!')

    def download_eps(self):
        try:
            os.mkdir(self.name)
        except OSError as error:
            print(error)

        for i, se in enumerate(self.all_links, 1):
            for ep in se[1]:
                print('[Finding] Looking for download link')
                self.driver.get(ep)
                chances = 0
                while chances < 15:
                    try:
                        src = self.driver.find_elements(By.TAG_NAME, 'source')[0].get_attribute('src')
                        break
                    except:
                        sleep(1)
                        chances += 1
                if chances < 15:
                    print('[Downloading] ', src[src.find('&name=') + 6:])
                    while True:
                        try:
                            r = requests.get(src)
                            with open(f"./{self.name}/{src[src.find('&name=') + 6:]}", 'wb') as f:
                                f.write(r.content)
                            print('[Downloaded] ', src[src.find('&name=') + 6:])
                            break
                        except:
                            continue


if __name__ == '__main__':
    load_dotenv()
    auth = [os.getenv("TESSERA"), os.getenv("PASSWORD"), ]
    course = [os.getenv("COURSE_NAME"), os.getenv("URL"), ]

    scraper = Course(course[1], course[0], auth[0], auth[1])
    scraper.login()
    scraper.get_ep_links()
    scraper.download_eps()
    input('Downloads Finished, Press ENTER...')
