import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from time import sleep

# # # # # # # # #
TWITTER = "https://twitter.com/home"
SPEEDTEST = "https://www.speedtest.net/"
TWITTER_EMAIL = "[your twitter email]"
TWITTER_NAME = "[your twitter account name]"
TWITTER_PASSWORD = "[your twitter password]"
# # # # # # # # #


class InternetSpeedTwitterBot:
    def __init__(self):
        # replace `path` with path for chromedriver.exe, e.g. "D:/Users/user/ChromeDriver/chromedriver.exe"
        self.service = Service(r"[path]")
        self.driver = webdriver.Chrome(service=self.service)
        self.current_upload = 0
        self.current_download = 0

    def get_internet_speed(self):
        """Opens speedtest website and performs it"""
        self.driver.get(url=SPEEDTEST)
        ui.WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, f'//*[@id="onetrust-accept-btn-handler"]'))).click()
        ui.WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, f'//*[@id="container"]/div/div[3]/div/div/'
                                                  f'div/div[2]/div[3]/div[1]/a/span[4]'))).click()

        sleep(60)
        try:
            self.current_download = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div/div[3]/div/div/div/'
                                                                       f'div[2]/div[3]/div[3]/div/div[3]/div/div/'
                                                                       f'div[2]/div[1]/div[1]/div/div[2]/span').text
            self.current_upload = self.driver.find_element(By.XPATH, f'//*[@id="container"]/div/div[3]/div/div/div/'
                                                                     f'div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/'
                                                                     f'div[1]/div[2]/div/div[2]/span').text
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def whine_out_loud(self):
        """Logs into Twitter and tweets about things"""
        self.driver.get(url=TWITTER)
        name = False
        password = False
        ui.WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, f'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/'
                                                  f'div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/'
                                                  f'input'))).send_keys(TWITTER_EMAIL, Keys.ENTER)
        sleep(10)

        while not password:
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                   f'2]/div/div/div[2]/div[2]/div[1]/div/div/div['
                                                   f'3]/div/label/div/div[2]/div[1]/input').send_keys(
                    TWITTER_PASSWORD, Keys.ENTER)
                password = True
            except selenium.common.exceptions.NoSuchElementException:
                while not name:
                    try:
                        self.driver.find_element(By.XPATH,
                                                 f'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div['
                                                 f'2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input').send_keys(
                            TWITTER_NAME, Keys.ENTER)
                        name = True
                    except selenium.common.exceptions.NoSuchElementException:
                        pass
                    sleep(10)

        sleep(10)

        try:
            ui.WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, f'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/'
                                                      f'div[1]/div/div/div/div[1]/div'))).click()
        except TimeoutException:
            pass

        ui.WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, f'//*[@id="react-root"]/div/div/div[2]/'
                                                  'header/div/div/div/div[1]/div[3]/a'))).click()
        sleep(5)
        self.driver.find_element(By.XPATH, f'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/'
                                           f'div[3]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/'
                                           f'div[2]/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/'
                                           f'div').send_keys(Keys.ENTER,
                                                             f"My download speed right now is {self.current_download}"
                                                             f"Mbps and upload speed is {self.current_upload}Mbps.CYA")
        try:
            ui.WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, f'//*[@id="layers"]/div[2]/div/div/div/div/'
                                                      f'div/div[2]/div[2]/div/div/div/div/div[2]/div[2]'))).click()
        except TimeoutException:
            pass
        self.driver.find_element(By.XPATH, f'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/'
                                           f'div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]/'
                                           f'div/span/span').click()
        self.driver.close()


if __name__ == '__main__':
    test = InternetSpeedTwitterBot()
    test.get_internet_speed()
    test.whine_out_loud()
