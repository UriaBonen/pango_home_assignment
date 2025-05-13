from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import driver


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def send_text(self, by, value, text):
        field = self.find_element(by, value)
        field.clear()
        field.send_keys(text)

    def click_element(self, by, value):
        element = self.wait_for_element(by, value)  # Wait for element to be visible
        element.click()  # Perform the click action
