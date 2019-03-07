import time
import requests
import json
from pprint import pprint
import pandas as pd
import sqlalchemy
import pymysql
from sqlalchemy import create_engine
import mysql.connector
import os
import os.path
import traceback
import logging
import sys


# Details for access to DublinBikes and OpenWeather APIs
B_contract="Dublin"
BIKES_URL="https://api.jcdecaux.com/vls/v1/stations"
B_APIKEY ="1b5a70bba36e98ed68efe695e839bcb44f4e6e27"

W_id = "7778677"  # name of contract
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?units=metric"
W_APIKEY = "f189dc2a9a2453baec98286f49d36183"

def bikesData():

    try:
        api_request_response = requests.get(BIKES_URL, params = {"apiKey": B_APIKEY, "contract": B_contract})
        print(json.loads(api_request_response.text))
        bike_data = json.loads(api_request_response.text)
        df = pd.DataFrame(bike_data)
        df['last_update'] = pd.to_datetime((df['last_update'] + 3600000) * 10e5)
        # removes columns not required
        clean_df = df[['number', 'last_update', 'available_bike_stands', 'available_bikes', 'status', 'banking']]
        print(clean_df)

        engine = create_engine("mysql+pymysql://root:whiterabbit@dbbikes.cydtuzfevnm7.us-east-1.rds.amazonaws.com:3306/dbbikes", echo=True)
        clean_df.to_sql(name='temp_table', con=engine, if_exists='replace', index=False)
        connection = engine.connect()
        connection.execute("INSERT INTO availability SELECT * FROM temp_table ON DUPLICATE KEY UPDATE availability.status=temp_table.status")

        PATH='/home/ubuntu/availability_csv.csv'
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
            with open('availability_csv.csv', 'a') as f:
                (clean_df).to_csv(f)
        else:
            clean_df.to_csv('availability_csv.csv')

    except:
        # saves error messages to a file named test.txt rather than simply printing them to the console
        logging.basicConfig(filename='test.txt')

        # formatting the error message - choosing which info to display
        # (error type/error message/line number in code error occurred on
        logging.error('{}. {}, line: {}'.format(sys.exc_info()[0],
                                            sys.exc_info()[1],
                                            sys.exc_info()[2].tb_lineno))
        print(traceback.format_exc())               # if there is any problem, print the traceback
    return                                          # says code is unreachable?

def weatherData():

    try:
        mydb = mysql.connector.connect(
            host="dbbikes.cydtuzfevnm7.us-east-1.rds.amazonaws.com",
            user="root",
            passwd="whiterabbit",
            database='dbbikes',
            charset='utf8mb4',
        )
        mycursor = mydb.cursor(dictionary=False)

        weather_request_response = requests.get(WEATHER_URL, params={"apiKey": W_APIKEY, "id": W_id})
        weather_data = weather_request_response.json()
        print(weather_data)

        main = weather_data
        for key, value in main.items():
            if key == 'dt':
                #print(key, value)
                dt = value

        main = weather_data["weather"][0]
        for key, value in main.items():
            if key == 'main':
                #print(key, value)
                description = value

        main = weather_data["wind"]
        for key, value in main.items():
            if key == 'speed':
                # print(key, value)
                wind_speed = value

        main = weather_data["main"]
        for key, value in main.items():
            if key == 'humidity':
                # print(key, value)
                humidity = value

        main = weather_data["main"]
        for key, value in main.items():
            if key == 'temp':
                # print(key, value)
                temperature = value

        main = weather_data["main"]
        for key, value in main.items():
            if key == 'pressure':
                # print(key, value)
                pressure = value

        print(dt, description, wind_speed, humidity, temperature, pressure)

        print("API data request successful!")

        sql = "INSERT INTO currentweather (dt, description, wind_speed, humidity, temperature, pressure) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (dt, description, wind_speed, humidity, temperature, pressure)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Data successfully sent ", mycursor.rowcount," to database!")
        print(mycursor.rowcount, "record inserted.")
        mycursor.close()

    except:
        print("error, weatherdata function")
        print(traceback.format_exc())               # if there is any problem, print the traceback
    return

i=0
while True:

    try:
        print("I am outside function")
        bikesData()
        print("Sleeping...")
        time.sleep(5 * 60)                          # now sleep for 5 minutes
        i += 1
        print(i)
        while i > 11:
            weatherData()
            i=0
    except:
        print("Error with program, not functions")