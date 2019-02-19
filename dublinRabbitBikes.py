# dublinRabbitBikes

"""
Program to scrape DublinBikes data.

Rough first attempt
"""
NAME="Dublin"                                           # name of contract
STATIONS="https://api.jcdecaux.com/vls/v1/stations"     # and the JCDecaux endpoint
APIKEY = "secret"
def main():
                                                        # run forever...
        while True:
                try:
                    r = requests.get(STATIONS,
                         params={"apiKey": APIKEY, "contract": NAME})
                    store(json.loads(r.text))                                # now sleep for 5 minutes
                        time.sleep(5*60)
                except:
                                                        # if there is any problem, print the traceback
                        print traceback.format_exc()
        return
                



                      




