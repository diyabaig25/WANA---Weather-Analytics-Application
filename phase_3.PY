#This is our Executble file which contain our menu 
#*****************************************************************************************************
from phase_1 import W_WANALYTICS as Wana
from phase_2 import GRAPH_PLOTTING
from datetime import datetime
wana=Wana("CIS4044-N-SDI-OPENMETEO-PARTIAL.db")
plot=GRAPH_PLOTTING("CIS4044-N-SDI-OPENMETEO-PARTIAL.db")

while True:
    #WANA Menu
    print("==============NOTE======================")
    print("Note: It only contains weather entries for the following years:") 
    print("2020 to 2022 so Enter data between this range only")
    print("==============WANA======================\n")

    print("1. Fetch all citiess")
    print("2. Fetch all countries")
    print("3. Average annual temperature Calculation ")
    print("4. Average seven-day precipitation calculation")
    print("5. Average mean temperature by city Calculation ")
    print("6. Average annual precipitation by country Calculation ")
    print("==============CHART PLOTTING=============\n")
    print("7.  Annual precipitation by Country")
    print("8.  City Weather Statistics")
    print("9.  Minimum and Maximum Temperature of a city")
    print("10. Avg_temp_vs_avg_rainfall")
    print("11. Average_mean_temp_and_precipitation_by_city")
    print("12. Average seven day Precipitation Plot")
    print("==============CLOSING WANA=========================\n")
    print("0.  Close application")

    try:
        num = int(input("Select a number from 1-13 or 0 to Exit: "))
        if num == 1:
            wana.select_all_cities()
        elif num == 2:
            wana.select_all_countries()
        elif num == 3:
            cID = int(input("Enter City ID: (from 1-4) "))
            year = input("Enter year:(e.g 2020) ")
            wana.average_annual_temperature(cID, year)
        elif num == 4:
            while True:
                cID = int(input("Enter City ID: (from 1-4) "))
                if 1 <= cID <= 4: #There are 4 cities in the data
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 4.")
            while True:
                sDate_str = input("Enter start date (e.g 2022-01-01): ")
                try:
                    sDate = datetime.strptime(sDate_str, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Invalid date format. Please enter the correct format (e.g 2022-01-01).")
            
            wana.average_seven_day_precipitation(cID, sDate)
        elif num == 5:
        
            while True:
                date_from_str = input("Enter start date (YYYY-MM-DD): ")
                date_to_str = input("Enter end date (YYYY-MM-DD): ")
                try:
                    date_from = datetime.strptime(date_from_str, '%Y-%m-%d') # input Date format
                    date_to = datetime.strptime(date_to_str, '%Y-%m-%d')
                    break
                except ValueError: #Error handling
                    print("Invalid date format. Please enter the correct format (YYYY-MM-DD).")
            wana.average_mean_temp_by_city(date_from, date_to)

        elif num == 6:
            year=input("Enter a year: (e.g 2020) ")
            wana.average_annual_precipitation_by_country(year)
        elif num==7:
            year = input("Enter year: (e.g 2020) ")
            plot.avg_annual_precipitation_by_country(year)
        elif num == 8:
            while True:
                datef = input("Enter Date From: (e.g 2022-01-01) ")
                datet = input("Enter Date To:   (e.g 2022-01-01) ")
                
                try:
                    date_from = datetime.strptime(datef, '%Y-%m-%d')
                    date_to = datetime.strptime(datet, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Invalid date format. Please enter the date in the correct format (e.g. 2022-01-01).")
            
            plot.city_weather_statistics(date_from, date_to)

        elif num == 9:
            while True:
                try:
                    cID = int(input("Enter City ID: (from 1-4) "))
                    if 1 <= cID <= 4:
                        break
                    else:
                        print("Invalid input. Please enter a number between 1 and 4.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            while True:
                try:
                    year = int(input("Enter year: (e.g. 2020) "))
                    if year >= 0:  
                        break
                    else:
                        print("Invalid input. Please enter a valid year.")
                except ValueError:
                    print("Invalid input. Please enter a valid year.")

            while True:
                try:
                    month = int(input("Enter month (1-12): "))
                    if 1 <= month <= 12:
                        break
                    else:
                        print("Invalid input. Please enter a number between 1 and 12.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            plot.daily_temperature(cID, year, month)

        elif num ==10:
            
            plot.plot_avg_temp_vs_avg_rainfall()
        elif num ==11:
            datef = input("Enter Date From: (e.g 2022-01-01) ")
            datet = input("Enter Date To:   (e.g 2022-01-01) ")
            plot.average_mean_temp_and_precipitation_by_city(datef,datet)
        elif num==12:
            cID=int(input('Enter City ID: (from 1-4) '))
            start_date=input('Enter Start Date: (e.g 2022-01-01)')
            plot.average_seven_day_precipitation(cID,start_date)
        elif num==13:
            #OpenMeteo()
            print('good')
        elif num == 0:
            print("Exiting from Wana. Goodbye!")
            break
    except Exception as e:
        print('Error:', e)