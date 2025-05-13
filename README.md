This assignment is written in Python using the pytest framework. The UI part is implemented using Selenium following the Page Object Model (POM) design pattern, and the REST API part uses the requests library.
To run the project, first install the dependencies using pip install -r requirements.txt, then run the tests by executing the pytest command from the pango_home_assignment/tests directory.
The main (and only) test is test_temp. This test calls all the supporting functions, collects weather data from both the UI and an API and generat the report( tests/weather_report.html).
To ensure that the cities used in the test exist and are available in the UI, the test dynamically fetches a list of popular cities from the UI before selecting a random subset for testing.
