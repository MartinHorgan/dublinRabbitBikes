# dublinRabbitBikes
import time
import requests
import json
from pprint import pprint
import pandas as pd
import sqlalchemy
import pymysql
from sqlalchemy import create_engine
import mysql.connector

id = "7778677"  # name of contract
WEATHER_URI = "https://api.openweathermap.org/data/2.5/weather?units=metric"
APIKEY = "f189dc2a9a2453baec98286f49d36183"

def weatherData():

    while True:

        try:
            mydb = mysql.connector.connect(
                host="dbbikes.cydtuzfevnm7.us-east-1.rds.amazonaws.com",
                user="root",
                passwd="whiterabbit",
                database='dbbikes',
                charset='utf8mb4',
            )
            mycursor = mydb.cursor(dictionary=False)

            weather_request_response = requests.get(WEATHER_URI, params={"apiKey": APIKEY, "id": id})
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

            print("Sleeping..")  # now sleep for 5 minutes
            time.sleep(60 * 60)
        except:
            print("error")
            time.sleep(60 * 60)  # now sleep for 5 minutes

    #             print(traceback.format_exc())               # if there is any problem, print the traceback
    return


weatherData()