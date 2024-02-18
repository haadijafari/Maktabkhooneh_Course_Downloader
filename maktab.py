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
        sleep(5)
        all_sections = self.driver.find_elements(
            By.XPATH, '//*[@id="__layout"]/section/section/section/section[2]/div/div/div/section/div/div/div')
        for i, se in enumerate(all_sections, 1):
            title = se.find_element(
                By.XPATH,
                f'//*[@id="__layout"]/section/section/section/section[2]/div/div/div/section/div/div/div[{i}]/section/div/div/div[1]/span[2]').text
            self.all_links.append((title, [
                i.get_attribute("href") for i in (se.find_elements(
                    By.XPATH,
                    '//*[@id="__layout"]/section/section/section/section[2]/div/div/div/section/div/div/div[1]/div/a'))
            ]))

    def download_eps(self):
        try:
            os.mkdir(self.name)
        except OSError as error:
            print(error)

        for i, se in enumerate(self.all_links, 1):
            name_format = f'[Season {i}] Ep'
            for _, ep in enumerate(se[1], 1):
                name = name_format + f'{_:03}'
                self.driver.get(ep)
                src = self.driver.find_element(
                    By.XPATH,
                    '/html/body/div[5]/div/div/div[3]/div[1]/div[1]/video/source[1]').get_attribute(
                    'src')
                r = requests.get(src)
                with open(f"./{self.name}/{src[src.find('&name=') + 6:]}", 'wb') as f:
                    f.write(r.content)


if __name__ == '__main__':
    load_dotenv()
    auth = [os.getenv("TESSERA"), os.getenv("PASSWORD"), ]
    course = [os.getenv("COURSE_NAME"), os.getenv("URL"), ]

    scraper = Course(course[1], course[0], auth[0], auth[1])
    scraper.login()
    scraper.get_ep_links()
    scraper.download_eps()
    input()
