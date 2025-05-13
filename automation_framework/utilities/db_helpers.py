import sqlite3

class DatabaseHelper:
    def __init__(self, db_name="data.db"):
        self.conn = sqlite3.connect(db_name)
        with self.conn:
            self.conn.execute('DROP TABLE IF EXISTS weather_data')  # <- TEMP fix

            self.conn.execute('DROP TABLE IF EXISTS weather_data')

        self.create_tables()

    def create_tables(self):
        # Create the table with updated columns
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS weather_data (
                    city TEXT PRIMARY KEY,
                    temperature_web REAL,
                    feels_like_web REAL,
                    temperature_api REAL,
                    feels_like_api REAL,
                    avg_temperature REAL
                )
            ''')

    def insert_weather_data(self, city, temperature_web, feels_like_web, temperature_api, feels_like_api,avg_temperature):
        # Compute average temperature (ignoring None values)
        temps = [t for t in [temperature_web, temperature_api] if t is not None]
        avg_temperature = sum(temps) / len(temps) if temps else None

        with self.conn:
            self.conn.execute('''
                INSERT OR REPLACE INTO weather_data (
                    city, temperature_web, feels_like_web, temperature_api, feels_like_api, avg_temperature
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (city, temperature_web, feels_like_web, temperature_api, feels_like_api, avg_temperature))

    def get_weather_data(self, city):
        # Retrieve all weather data for a city
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT temperature_web, feels_like_web, temperature_api, feels_like_api, avg_temperature
            FROM weather_data WHERE city = ?
        ''', (city,))
        result = cursor.fetchone()
        if result:
            return {
                'city': city,
                'temperature_web': result[0],
                'feels_like_web': result[1],
                'temperature_api': result[2],
                'feels_like_api': result[3],
                'avg_temperature': result[4]
            }
        else:
            return None

    def select_all(self):
        # Retrieve all weather data for all cities
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT city, temperature_web, feels_like_web, temperature_api, feels_like_api, avg_temperature
            FROM weather_data
        ''')
        results = cursor.fetchall()

        # Check if results have been fetched correctly
        print(f"Retrieved rows: {len(results)}")  # Debugging: This should print the number of rows retrieved

        # Format the results into a list of dictionaries
        all_weather_data = []
        for row in results:
            all_weather_data.append({
                'city': row[0],
                'temperature_web': row[1],
                'feels_like_web': row[2],
                'temperature_api': row[3],
                'feels_like_api': row[4],
                'avg_temperature': row[5]
            })

        return all_weather_data
