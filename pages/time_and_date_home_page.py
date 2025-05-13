import re
import random

import pytest
from selenium.webdriver.common.by import By

import config
from pages.base_page import BasePage
from tests.conftest import driver


@pytest.mark.usefixtures("browser")
class TimeAndDateHomePage(BasePage):
    url = config.TIME_AND_DATE_HOME_PAGE
    table = "//div[@class='tb-scroll']//table//tbody"
    search_field = "picker-city__input"
    search_btn = "picker-city__button"

    def get_home_page(self):
        self.open_url(url=self.url)

    def get_all_most_popular_cities(self):
        cities = self.driver.find_elements(By.XPATH, self.table)
        cleaned = []
        cities = cities[0].text.split("°C")

        for city in cities:
            city = re.sub(r'[^A-Za-z0-9:\- ]+', '', city)
            city = re.sub(r'\b(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)\b', '', city)
            colon_index = city.find(':')
            to_remove = city[colon_index - 2: colon_index + 3]
            city = city.replace(to_remove, '')
            city = city.strip()
            cleaned.append(city)
        temperature_by_city = []
        for city in cleaned:
            web_dict = {}
            for i, char in enumerate(city):
                if char.isdigit() or char == '-':
                    break

            city_ = city[:i].strip()
            temp = (city[i:].strip())
            web_dict['city'] = city_
            web_dict['temperature_web'] = temp
            temperature_by_city.append(web_dict)

        return temperature_by_city

    def get_random_n_cities(self, cities: list, n: int) -> dict:
        return random.sample(cities, n)

    def click_on_city(self, city: str):
        self.driver.find_element(By.XPATH, f"//*[contains(text(), '{city}')]").click()
