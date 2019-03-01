import time
import requests
import json
from pprint import pprint
import pandas as pd
import sqlalchemy
import pymysql
from sqlalchemy import create_engine

id="7778677"  # name of contract
WEATHER_URI = "https://api.openweathermap.org/data/2.5/forecast?"   # and the open weather endpoint
W_APIKEY = "f189dc2a9a2453baec98286f49d36183"

def weather():                                                      # run forever...

    while True:
        try:
            weather_request_response = requests.get(WEATHER_URI, params={"apiKey": W_APIKEY, "id": id})
            print(json.loads(weather_request_response.text))
            weather_data = json.loads(weather_request_response.text)
            df = pd.DataFrame(weather_data)
            df['dt'] = pd.to_datetime((df['dt'] + 3600000) * 10e5)
            # removes columns not required
            clean_Weather_df = df[['main.temp', 'wind', 'clouds', 'rain.1h', 'snow.1h', 'dt', 'id']]
            print(clean_Weather_df)

            engine = create_engine(
                "mysql+pymysql://root:whiterabbit@dbbikes.cydtuzfevnm7.us-east-1.rds.amazonaws.com:3306/dbbikes",
                echo=True)
            clean_Weather_df.to_sql(name='temp_Weather_table', con=engine, if_exists='replace', index=False)
            connection = engine.connect()
            connection.execute(
                "INSERT INTO currentweather SELECT * FROM temp_Weather_table ON DUPLICATE KEY UPDATE currentweather.status=temp_Weather_table.status")

            print("Sleeping..")  # now sleep for 15 minutes
            time.sleep(15 * 60)
      except:
            print("error")
            time.sleep(15*60)                                       # now sleep for 15 minutes

#           print(traceback.format_exc())                           # if there is any problem, print the traceback
    return

weather()
