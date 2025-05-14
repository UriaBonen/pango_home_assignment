import re
import statistics

import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import config
from automation_framework.utilities.api_helpers import ApiHelper
from automation_framework.utilities.db_helpers import DatabaseHelper
from pages.time_and_date_home_page import TimeAndDateHomePage
from pages.whether_page import WeatherPage
from tests.conftest import driver
from tests.report import ReportGenerator


@pytest.mark.usefixtures("driver")
class TestTemperature:

    def get_value_by_city(slef, data, city_name, key):
        for item in data:
            if item.get('city') == city_name:
                return item.get(key)
        return None

    def get_cities(self, driver, n=20):
        driver.get(config.TIME_AND_DATE_HOME_PAGE)
        home_page = TimeAndDateHomePage(driver)
        all_popular_cities = home_page.get_all_most_popular_cities()
        n_cities = home_page.get_random_n_cities(cities=all_popular_cities, n=n)
        return n_cities

    def get_web_temperature_and_feels_like(self, driver, cities):
        whether_page = WeatherPage(driver)
        home_page = TimeAndDateHomePage(driver)
        driver.get(config.TIME_AND_DATE_HOME_PAGE)
        web_data = cities
        for key in web_data:
            try:
                home_page.click_on_city(city=key["city"])
                feels_like = whether_page.get_feels_like()
                key['feels_like_web'] = feels_like
                driver.get(config.TIME_AND_DATE_HOME_PAGE)
            except:
                web_data.remove(key)
        return web_data

    def get_api_temperature_and_feels_like(self, driver, cities):
        api_helper = ApiHelper()
        cities = cities
        api_data = []
        for city in cities:
            api_elmnt = {}

            response = api_helper.get_current_weather(city=f'{city}').json()
            api_elmnt['city'] = city
            api_elmnt['temperature_api'] = response['main']['temp'] - 273.15
            api_elmnt['feels_like_api'] = response['main']['feels_like'] - 273.15
            api_data.append(api_elmnt)
        return api_data

    def generate_api_and_web_data(self, driver):
        web_cities = self.get_cities(driver)

        web_data = self.get_web_temperature_and_feels_like(driver, cities=web_cities)
        api_cities_list = [item["city"] for item in web_data]
        api_data = self.get_api_temperature_and_feels_like(driver, cities=api_cities_list)
        db = DatabaseHelper()
        for city in api_cities_list:
            temperature_web_ = float(self.get_value_by_city(data=web_data, city_name=city, key='temperature_web'))
            temperature_api_ = self.get_value_by_city(data=api_data, city_name=city, key='temperature_api')
            avg_temperature_ = (temperature_api_ + temperature_web_) / 2
            feels_like_web_ = self.get_value_by_city(data=web_data, city_name=city,
                                                     key='feels_like_web')
            feels_like_api_ = self.get_value_by_city(data=api_data, city_name=city,
                                                     key='feels_like_api')

            db.insert_weather_data(city=city, temperature_web=temperature_web_,
                                   feels_like_web=feels_like_web_,
                                   temperature_api=temperature_api_,
                                   feels_like_api=feels_like_api_,
                                   avg_temperature=avg_temperature_
                                   )
        cities_whether = db.select_all()
        return cities_whether

    def test_temp(self,driver):
        data = self.generate_api_and_web_data(driver=driver)
        try:
            report = ReportGenerator(data)
            report.generate_html()
        except:
            print("Report creation failed.")


