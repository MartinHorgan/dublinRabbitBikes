import time
import requests
import json
from pprint import pprint
import pandas as pd
import sqlalchemy
import pymysql
from sqlalchemy import create_engine
import os
import os.path
import traceback
import logging
import sys



contract="Dublin"                                             # name of contract
STATIONS_URI="https://api.jcdecaux.com/vls/v1/stations"       # and the JCDecaux endpoint
APIKEY ="1b5a70bba36e98ed68efe695e839bcb44f4e6e27"

def main():                                             # run forever...
                                                         
    while True:
        try:
            api_request_response = requests.get(STATIONS_URI, params = {"apiKey": APIKEY, "contract": contract})
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

            print("Sleeping..")# now sleep for 5 minutes
            time.sleep(5*60)

        except:
            logging.basicConfig(filename='test.txt')

            logging.error('{}. {}, line: {}'.format(sys.exc_info()[0],
                                             sys.exc_info()[1],
                                             sys.exc_info()[2].tb_lineno))

            time.sleep(5*60)                                # now sleep for 5 minutes

            print(traceback.format_exc())               # if there is any problem, print the traceback
    return


main()