#In this file we've implemented all the pase 1 function in an Object oriented way with a class nae W_WANALYTICS
#*****************************************************************************************************
import sqlite3

class W_WANALYTICS:

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)

    def select_all_countries(self):
        try:
            #SQL commands
            query = "SELECT * FROM [countries]"
            cursor = self.connection.cursor()
            results = cursor.execute(query)
            for row in results:
                print(f"Country Id: {row[0]} -- Country Name: {row[1]} -- Country Timezone: {row[2]}")
        #Exception handling
        except sqlite3.OperationalError as ex:
            print(ex)

    def select_all_cities(self):
        try:
            #SQL commands
            query = "SELECT * FROM [cities]"
            cursor = self.connection.cursor()
            results = cursor.execute(query)
            for row in results:
                print(f"City Id: {row[0]} -- City Name: {row[1]} -- Longitude: {row[2]} -- Latitude: {row[3]} -- Country Id of the City: {row[4]}")
        except sqlite3.OperationalError as ex:
            print(ex)

    def average_annual_temperature(self, city_id, year):
        try:
            #SQL commands
            query = """
            SELECT AVG(mean_temp)
            FROM daily_weather_entries
            WHERE city_id = ? AND strftime('%Y', date) = ?
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (city_id, year))
            average_temperature = cursor.fetchone()[0]
            average_temperature =round(average_temperature, 2)
            print(f"Average annual temperature for City {city_id} in {year}: {average_temperature} °C")
        except sqlite3.OperationalError as ex:
            print(ex)

    def average_seven_day_precipitation(self, city_id, start_date):
        try:
            cursor = self.connection.cursor()

            query = """
            SELECT AVG(precipitation)
            FROM daily_weather_entries
            WHERE city_id = ? AND date BETWEEN ? AND date(?, '+6 days')
            """

            cursor.execute(query, (city_id, start_date, start_date))
            #Fetching data
            average_precipitation = cursor.fetchone()[0]
            average_precipitation =round(average_precipitation, 2)
            print(f"Average seven-day precipitation for City {city_id} starting from {start_date}: {average_precipitation} mm")
        except sqlite3.OperationalError as ex:
            print(ex)

    def average_mean_temp_by_city(self, date_from, date_to):
        try:
            cursor = self.connection.cursor()

            query = """
            SELECT city_id, AVG(mean_temp) AS avg_mean_temp
            FROM daily_weather_entries
            WHERE date BETWEEN ? AND ?
            GROUP BY city_id
            """
            cursor.execute(query, (date_from, date_to))
            results = cursor.fetchall()
            for row in results:
                city_id, avg_mean_temp = row
                avg_mean_temp=round(avg_mean_temp, 2)
                print(f"City {city_id}: Average mean temperature between {date_from} and {date_to}: {avg_mean_temp} °C")

        except sqlite3.OperationalError as ex:
            print(ex)

    def average_annual_precipitation_by_country(self, year):
        try:
            cursor = self.connection.cursor()

            query = '''
                SELECT countries.name, AVG(daily_weather_entries.precipitation)
                FROM countries
                JOIN cities ON countries.id = cities.id
                JOIN daily_weather_entries ON cities.id = daily_weather_entries.city_id
                WHERE strftime('%Y', daily_weather_entries.date) = ?
                GROUP BY countries.name
            '''

            cursor.execute(query, (str(year),))
            results = cursor.fetchall()
            for country, avg_precipitation in results:
                avg_precipitation=round(avg_precipitation, 2)
                print(f"Average annual precipitation for {country} in {year}: {avg_precipitation} mm")
        except sqlite3.OperationalError as ex:
            print(ex)
    #This is a class method which close th sqlite database connection
    def close_connection(self):
        self.connection.close()
