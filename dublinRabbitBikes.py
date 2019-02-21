# dublinRabbitBikes
import requests
import json
from pprint import pprint
import time

"""
Program to scrape DublinBikes data.

Rough first attempt
"""
NAME="Dublin"                                             # name of contract
STATIONS_URI="https://api.jcdecaux.com/vls/v1/stations"       # and the JCDecaux endpoint
APIKEY ="1b5a70bba36e98ed68efe695e839bcb44f4e6e27"

# r = requests.get("{}/{}".format(STATIONS_URI, 41),
#                  params={"apiKey": APIKEY, "contract": NAME})
# pprint(json.loads(r.text))


def main():                                             # run forever...
                                                         
    while True:
        try:
            r = requests.get(STATIONS_URI, params = {"apiKey": APIKEY, "contract": NAME})
            print(json.loads(r.text))                 
            time.sleep(5*60)                                # now sleep for 5 minutes
        except:
                print("error")
#             print(traceback.format_exc())               # if there is any problem, print the traceback
    return
                

main()