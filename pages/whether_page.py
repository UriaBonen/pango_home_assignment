import re
from ast import Bytes

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class WeatherPage(BasePage):
    quick_lock_element = "qlook"

    def get_q_look_data(self):
        q_look = self.driver.find_element(By.ID, self.quick_lock_element)
        data = q_look.text
        return data

    def get_feels_like(self) -> int:
        try:
            q_look = self.driver.find_element(By.ID, self.quick_lock_element)
            text = q_look.text
            match = re.search(r'Feels Like:\s*(-?\d+)', text)
            if match:
                return int(match.group(1))
            else:
                raise ValueError("Element not found")
        except Exception as e:
            raise RuntimeError(f"Error extracting 'Feels Like' temperature: {e}")



