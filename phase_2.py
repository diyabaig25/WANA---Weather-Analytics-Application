##In this file we've implemented all the plots in an Object oriented way with a class name GRAPH_PLOTTING
#*****************************************************************************************************
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

class GRAPH_PLOTTING:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
    def avg_annual_precipitation_by_country(self, year):
        try:
            cursor = self.connection.cursor()

            query = '''
                SELECT countries.name, AVG(daily_weather_entries.precipitation)
                FROM countries
                JOIN cities ON countries.id = cities.country_id
                JOIN daily_weather_entries ON cities.id = daily_weather_entries.city_id
                WHERE strftime('%Y', daily_weather_entries.date) = ?
                GROUP BY countries.name
            '''

            cursor.execute(query, (str(year),))
            results = cursor.fetchall()

            countries = []
            avg_precipitations = []

            for country, avg_precipitation in results:
                countries.append(country)
                avg_precipitations.append(avg_precipitation)
                print(f"Average annual precipitation for {country} in {year}: {avg_precipitation} mm")

            # Plotting the bar chart
            plt.figure(figsize=(10, 6))
            plt.bar(countries, avg_precipitations, color='green')
            plt.xlabel('Countries')
            plt.ylabel('Average Yearly Precipitation (mm)')
            plt.title(f'Average Yearly Precipitation by Country in {year}')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

        except sqlite3.OperationalError as ex:
            print(ex)    
    def city_weather_statistics(self, date_from, date_to):
        try:
            cursor =self.connection.cursor()

            query = """
            SELECT city_id, 
                AVG(mean_temp) AS avg_mean_temp,
                MIN(mean_temp) AS min_mean_temp,
                MAX(mean_temp) AS max_mean_temp,
                AVG(precipitation) AS avg_precipitation
            FROM daily_weather_entries
            WHERE date BETWEEN ? AND ?
            GROUP BY city_id
            """

            cursor.execute(query, (date_from, date_to))
            results = cursor.fetchall()

            city_ids = []
            avg_mean_temps = []
            min_mean_temps = []
            max_mean_temps = []
            avg_precipitations = []

            for row in results:
                city_id, avg_mean_temp, min_mean_temp, max_mean_temp, avg_precipitation = row
                city_ids.append(city_id)
                avg_mean_temps.append(avg_mean_temp)
                min_mean_temps.append(min_mean_temp)
                max_mean_temps.append(max_mean_temp)
                avg_precipitations.append(avg_precipitation)

                print(f"City {city_id}:")
                print(f"Average Mean Temperature: {avg_mean_temp} °C")
                print(f"Minimum Mean Temperature: {min_mean_temp} °C")
                print(f"Maximum Mean Temperature: {max_mean_temp} °C")
                print(f"Average Precipitation: {avg_precipitation} mm\n")

            # Plotting
            plt.bar(city_ids, avg_mean_temps, label='Average Mean Temperature', alpha=0.7)
            plt.bar(city_ids, min_mean_temps, label='Minimum Mean Temperature', alpha=0.7)
            plt.bar(city_ids, max_mean_temps, label='Maximum Mean Temperature', alpha=0.7)
            plt.bar(city_ids, avg_precipitations, label='Average Precipitation', alpha=0.7)
            
            plt.xlabel('City ID')
            plt.ylabel('Values')
            plt.title(f'Weather Statistics for Cities between {date_from} and {date_to}')
            plt.legend()
            plt.show()

        except sqlite3.OperationalError as ex:
            print(ex)

    def daily_temperature(self, city_id, year, month):
        try:
            
            cursor = self.connection.cursor()

            query = """
            SELECT date, min_temp, max_temp
            FROM daily_weather_entries
            WHERE city_id = ? AND strftime('%Y-%m', date) = ?
            """

            cursor.execute(query, (city_id, f"{year:04d}-{month:02d}"))
            results = cursor.fetchall()

            dates = []
            min_temps = []
            max_temps = []

            for row in results:
                date_str, min_temp, max_temp = row
                date = datetime.strptime(date_str, '%Y-%m-%d')
                dates.append(date)
                min_temps.append(min_temp)
                max_temps.append(max_temp)

            # Plotting
            plt.plot(dates, min_temps, label='Min Temperature',c='blue', marker='o')
            plt.plot(dates, max_temps, label='Max Temperature',c='red', marker='o')
            
            plt.xlabel('Date')
            plt.ylabel('Temperature (°C)')
            plt.title(f'Daily Minimum and Maximum Temperature for City {city_id} in {year}-{month:02d}')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()

        except sqlite3.OperationalError as ex:
            print(ex)

    def plot_avg_temp_vs_avg_rainfall(self):
        try:
            
            cursor = self.connection.cursor()

            query = """
            SELECT city_id, AVG(mean_temp) AS avg_temp, AVG(precipitation) AS avg_rainfall
            FROM daily_weather_entries
            GROUP BY city_id
            """

            cursor.execute(query)
            results = cursor.fetchall()

            city_ids = []
            avg_temps = []
            avg_rainfalls = []

            for row in results:
                city_id, avg_temp, avg_rainfall = row
                city_ids.append(city_id)
                avg_temps.append(avg_temp)
                avg_rainfalls.append(avg_rainfall)

            # Plotting
            plt.scatter(avg_temps, avg_rainfalls, c='blue', alpha=0.7)
            plt.xlabel('Average Temperature (°C)')
            plt.ylabel('Average Rainfall (mm)')
            plt.title('Scatter Plot of Average Temperature vs Average Rainfall')
            plt.show()

        except sqlite3.OperationalError as ex:
            print(ex)
    
    def average_mean_temp_and_precipitation_by_city(self,date_from, date_to):
        try:
            
            cursor = self.connection.cursor()

            query = """
            SELECT city_id, 
                AVG(mean_temp) AS avg_mean_temp,
                AVG(precipitation) AS avg_precipitation
            FROM daily_weather_entries
            WHERE date BETWEEN ? AND ?
            GROUP BY city_id
            """
            cursor.execute(query, (date_from, date_to))
            results = cursor.fetchall()

            cities = []
            avg_temps = []
            avg_precipitations = []

            for row in results:
                city_id, avg_mean_temp, avg_precipitation = row
                cities.append(city_id)
                avg_temps.append(avg_mean_temp)
                avg_precipitations.append(avg_precipitation)
                print(f"City {city_id}:")
                print(f"  - Average Mean Temperature between {date_from} and {date_to}: {avg_mean_temp} °C")
                print(f"  - Average Precipitation between {date_from} and {date_to}: {avg_precipitation} mm\n")

            # Plotting
            plt.figure(figsize=(10, 6))
            plt.bar(cities, avg_temps, color='yellow', label='Average Mean Temperature')
            plt.bar(cities, avg_precipitations, color='green', label='Average Precipitation')
            plt.xlabel('City ID')
            plt.ylabel('Values')
            plt.title('Average Mean Temperature and Precipitation by City')
            plt.legend()
            plt.xticks(cities)
            plt.tight_layout()
            plt.show()

        except sqlite3.OperationalError as ex:
            print(ex)
    def average_seven_day_precipitation(self, city_id, start_date):
        try:
            cursor = self.connection.cursor()

            query = """
            SELECT date, precipitation
            FROM daily_weather_entries
            WHERE city_id = ? AND date BETWEEN ? AND date(?, '+6 days')
            """

            cursor.execute(query, (city_id, start_date, start_date))
            results = cursor.fetchall()

            dates = []
            precipitation_values = []

            for date, precipitation in results:
                dates.append(date)
                precipitation_values.append(precipitation)
                print(f"Precipitation for City {city_id} on {date}: {precipitation} mm")

            # Plotting the bar chart
            plt.figure(figsize=(10, 6))
            plt.bar(dates, precipitation_values, color='lightgreen')
            plt.xlabel('Date')
            plt.ylabel('Precipitation (mm)')
            plt.title(f'7-Day Precipitation for City {city_id} starting from {start_date}')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

        except sqlite3.OperationalError as ex:
            print(ex)