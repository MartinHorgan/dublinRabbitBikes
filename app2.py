from flask import Flask, flash, redirect, url_for, render_template, request, session, abort, jsonify
import mysql.connector
import json
import datetime
import pickle
import pandas as pd
import numpy as np
#from sklearn.linear_model import LinearRegression 
from datetime import date, timedelta
#import holidays

app = Flask(__name__)

@app.route("/graphs", methods=['POST'])
def graphs():
    # DATABASE CONNECTION
    mydb = mysql.connector.connect(
        host="dbbikes.cydtuzfevnm7.us-east-1.rds.amazonaws.com",
        user="root",
        passwd="whiterabbit",
        database="dbbikes"
    )

    # GET FORMS FROM HTML
    radio = request.form.get('radio')
    stn = request.form.get('id')


    # GENERATE STATION LIST
    # prebuilt function in mysql to interact with a database
    mycursor = mydb.cursor(dictionary=True)
    # Next, we setup our SQL query
    mycursor.execute("SELECT * from stations a, temp_table b where a.number= b.number order by a.address")
    # Then we get some stuff back... By appending a variable to the response of the query
    myresult = mycursor.fetchall()
    # We make an empty list
    station_list = []

    # for every result we get back, we add that to the list in a new index
    for x in myresult:
        station_list.append(dict((x)))

    # Print station list for error checking
    print(station_list)

    # this json dumps function is essential in returning data back to the front end correctly
    station_list = json.dumps(station_list)

    # CHARTS: DECLARE X AS CURRENT DATE/TIME
    x = datetime.datetime.now()
    station_number = stn
    dayx = x.strftime("%A")
    hourx = int(x.strftime("%H"))
    print(dayx)
    print(hourx)
    print("this is radio:", radio)
    print("this is stn:", stn)

    # CHARTS: AVG BIKES BY SELECTED STATION, NOW & +HOURS, for Radio button "Available Bikes"
    if radio == "available_bikes":
        mycursor = mydb.cursor(dictionary=False)
        mycursor.execute(
            "SELECT avg(available_bikes) from availability where number = %s and (DAYNAME(last_update) = %s) AND (HOUR(last_update) = %s)",
            (station_number, dayx, hourx + 1,))
        myresult = mycursor.fetchall()
        # print(myresult)
        now1 = []
        for i in myresult:
            print("now1:",i)
            now1.append(i)
        try:
            now1x = int((now1[0][0]))
            print("1hr:", now1x)
        except:
            now1x = 0

        mycursor = mydb.cursor(dictionary=False)
        mycursor.execute(
            "SELECT avg(available_bikes) from availability where number = %s and (DAYNAME(last_update) = %s) AND (HOUR(last_update) = %s)",
            (station_number, dayx, (hourx + 2),))
        myresult = mycursor.fetchall()
        # print(myresult)
        now2 = []
        for i in myresult:
            print("now2:",i)
            now2.append(i)
        try:
            now2x = int((now2[0][0]))
            print("2hr:", now2x)
        except:
            now2x = 0

        mycursor = mydb.cursor(dictionary=False)
        mycursor.execute(
            "SELECT avg(available_bikes) from availability where number = %s and (DAYNAME(last_update) = %s) AND (HOUR(last_update) = %s)",
            (station_number, dayx, hourx + 3,))
        myresult = mycursor.fetchall()
        # print(myresult)
        now3 = []
        for i in myresult:
            print("now3:",i)
            now3.append(i)
        try:
            now3x = int((now3[0][0]))
            print("3hr:", now3x)
        except:
            now3x = 0

        mycursor = mydb.cursor(dictionary=False)
        mycursor.execute(
            "SELECT avg(available_bikes) from availability where number = %s and (DAYNAME(last_update) = %s) AND (HOUR(last_update) = %s)",
            (station_number, dayx, hourx + 4,))
        myresult = mycursor.fetchall()
        # print(myresult)
        now4 = []
        for i in myresult:
            print("now4:",i)
            now4.append(i)
        try:
            now4x = int((now4[0][0]))
            print("4hr:", now4x)
        except:
            now4x = 0

        times = ["1hr", "2hr", "3hr", "4hr"]
        qty = [now1x, now2x, now3x, now4x]

        # CHARTS: AVG STATION OCCUPANCY BY DAY-OF-WEEK, for Radio button "Available Bikes"
        mycursor = mydb.cursor(dictionary=False)
        mycursor.execute(
            "SELECT avg(available_bikes) from availability where (DAYOFWEEK(last_update) = 1)  AND number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        mon = []
        for i in myresult:
            # print(i)
            mon.append(i)
        monday = int((mon[0][0]))
        print("Monday:", monday)

        mycursor.execute(
            "SELECT avg(available_bikes) from availability where (DAYOFWEEK(last_update) = 2)  AND number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        tue = []
        for i in myresult:
            # print(i)
            tue.append(i)
        tuesday = int((tue[0][0]))
        print("Tuesday:", tuesday)

        mycursor.execute(
            "SELECT avg(available_bikes) from availability where (DAYOFWEEK(last_update) = 3) and number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        wed = []
        for i in myresult:
            # print(i)
            wed.append(i)
        wednesday = int((wed[0][0]))
        print("Wednesday:", wednesday)

        mycursor.execute(
            "SELECT avg(available_bikes) from availability where (DAYOFWEEK(last_update) = 4) and number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        thur = []
        for i in myresult:
            # print(i)
            thur.append(i)
        thursday = int((thur[0][0]))
        print("Thursday:", thursday)

        mycursor.execute(
            "SELECT avg(available_bikes) from availability where (DAYOFWEEK(last_update) = 5) and number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        fri = []
        for i in myresult:
            # print(i)
            fri.append(i)
        friday = int((fri[0][0]))
        print("Friday:", friday)

        mycursor.execute(
            "SELECT avg(available_bikes) from availability where (DAYOFWEEK(last_update) = 6) and number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        sat = []
        for i in myresult:
            # print(i)
            sat.append(i)
        saturday = int((sat[0][0]))
        print("Saturday:", saturday)

        mycursor.execute(
            "SELECT avg(available_bikes) from availability where (DAYOFWEEK(last_update) = 7) and number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        sun = []
        for i in myresult:
            # print(i)
            sun.append(i)
        sunday = int((sun[0][0]))
        print("Sunday:", sunday)

        labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_values = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
    else:

        # CHARTS: AVG BIKES BY SELECTED STATION, NOW & +HOURS, for Radio button "Available Stands"
        mycursor = mydb.cursor(dictionary=False)
        mycursor.execute(
            "SELECT avg(available_bike_stands) from availability where number = %s and (DAYNAME(last_update) = %s) AND (HOUR(last_update) = %s)",
            (station_number, dayx, hourx + 1,))
        myresult = mycursor.fetchall()
        # print(myresult)
        now1 = []
        for i in myresult:
            print(i)
            now1.append(i)
        try:
            now1x = int((now1[0][0]))
            print("1hr:", now1x)
        except:
            now1x = 0

        mycursor = mydb.cursor(dictionary=False)
        mycursor.execute(
            "SELECT avg(available_bike_stands) from availability where number = %s and (DAYNAME(last_update) = %s) AND (HOUR(last_update) = %s)",
            (station_number, dayx, (hourx + 2),))
        myresult = mycursor.fetchall()
        # print(myresult)
        now2 = []
        for i in myresult:
            print(i)
            now2.append(i)
        try:
            now2x = int((now2[0][0]))
            print("2hr:", now2x)
        except:
            now2x = 0

        mycursor = mydb.cursor(dictionary=False)
        mycursor.execute(
            "SELECT avg(available_bike_stands) from availability where number = %s and (DAYNAME(last_update) = %s) AND (HOUR(last_update) = %s)",
            (station_number, dayx, hourx + 3,))
        myresult = mycursor.fetchall()
        # print(myresult)
        now3 = []
        for i in myresult:
            print(i)
            now3.append(i)
        try:
            now3x = int((now3[0][0]))
            print("3hr:", now3x)
        except:
            now3x = 0

        mycursor = mydb.cursor(dictionary=False)
        mycursor.execute(
            "SELECT avg(available_bike_stands) from availability where number = %s and (DAYNAME(last_update) = %s) AND (HOUR(last_update) = %s)",
            (station_number, dayx, hourx + 4,))
        myresult = mycursor.fetchall()
        # print(myresult)
        now4 = []
        for i in myresult:
            print(i)
            now4.append(i)
        try:
            now4x = int((now4[0][0]))
            print("4hr:", now4x)
        except:
            now4x = 0

        times = ["1hr", "2hr", "3hr", "4hr"]
        qty = [now1x, now2x, now3x, now4x]

        # CHARTS: AVG BIKES BY SELECTED STATION, NOW & +HOURS, for Radio button "Available Stands"
        mycursor = mydb.cursor(dictionary=False)
        mycursor.execute(
            "SELECT avg(available_bike_stands) from availability where (DAYOFWEEK(last_update) = 1)  AND number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        mon = []
        for i in myresult:
            # print(i)
            mon.append(i)
        monday = int((mon[0][0]))
        print("Monday:", monday)

        mycursor.execute(
            "SELECT avg(available_bike_stands) from availability where (DAYOFWEEK(last_update) = 2)  AND number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        tue = []
        for i in myresult:
            # print(i)
            tue.append(i)
        tuesday = int((tue[0][0]))
        print("Tuesday:", tuesday)

        mycursor.execute(
            "SELECT avg(available_bike_stands) from availability where (DAYOFWEEK(last_update) = 3) and number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        wed = []
        for i in myresult:
            # print(i)
            wed.append(i)
        wednesday = int((wed[0][0]))
        print("Wednesday:", wednesday)

        mycursor.execute(
            "SELECT avg(available_bike_stands) from availability where (DAYOFWEEK(last_update) = 4) and number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        thur = []
        for i in myresult:
            # print(i)
            thur.append(i)
        thursday = int((thur[0][0]))
        print("Thursday:", thursday)

        mycursor.execute(
            "SELECT avg(available_bike_stands) from availability where (DAYOFWEEK(last_update) = 5) and number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        fri = []
        for i in myresult:
            # print(i)
            fri.append(i)
        friday = int((fri[0][0]))
        print("Friday:", friday)

        mycursor.execute(
            "SELECT avg(available_bike_stands) from availability where (DAYOFWEEK(last_update) = 6) and number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        sat = []
        for i in myresult:
            # print(i)
            sat.append(i)
        saturday = int((sat[0][0]))
        print("Saturday:", saturday)

        mycursor.execute(
            "SELECT avg(available_bike_stands) from availability where (DAYOFWEEK(last_update) = 7) and number = %s",
            (station_number,))
        myresult = mycursor.fetchall()
        # print(myresult)
        sun = []
        for i in myresult:
            # print(i)
            sun.append(i)
        sunday = int((sun[0][0]))
        print("Sunday:", sunday)

        labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_values = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

    #getting the holidays for ireland
    ie_holidays = holidays.IE()
    print("holidays", date(2017,12,25) in ie_holidays)

    now = datetime.datetime.now()
    datetomorrow = datetime.datetime.now() + timedelta(days = 1)
    dateintwodays = datetime.datetime.now() + timedelta(days=2)
    dateinthreedays = datetime.datetime.now() + timedelta(days=3)
    dateinfourdays = datetime.datetime.now() + timedelta(days=4)
    dateinfivedays = datetime.datetime.now() + timedelta(days=5)
    dateinsixdays = datetime.datetime.now() + timedelta(days=6)

    print("current date is: ", now.strftime("%Y-%m-%d"))
    print("in six days: ", dateinsixdays.strftime("%d %B %Y"))
    print ("is this easter?", date(2019,4,22) in ie_holidays )

    holidaylist = []

    if (now.strftime("%Y, %m, %d")) in ie_holidays:
        holidaylist.append(ie_holidays.get(now.strftime("%Y-%m-%d")) + " is today! This may affect bike availability.")
    elif (datetomorrow.strftime("%Y, %m, %d")) in ie_holidays:
        holidaylist.append(ie_holidays.get(datetomorrow.strftime("%Y-%m-%d")) + " is tomorrow! This may affect bike availability.")
    elif (dateintwodays.strftime("%Y, %m, %d")) in ie_holidays:
        holidaylist.append(ie_holidays.get(dateintwodays.strftime("%Y-%m-%d")) + " is in 2 days! This may affect bike availability.")
    elif (dateinthreedays.strftime("%Y, %m, %d")) in ie_holidays:
        holidaylist.append(ie_holidays.get(dateinthreedays.strftime("%Y-%m-%d")) + " is in 3 days! This may affect bike availability.")
    elif (dateinfourdays.strftime("%Y, %m, %d")) in ie_holidays:
        holidaylist.append(ie_holidays.get(dateinfourdays.strftime("%Y-%m-%d")) + " is in 4 days! This may affect bike availability.")
    elif (dateinfivedays.strftime("%Y, %m, %d")) in ie_holidays:
        holidaylist.append(ie_holidays.get(dateinfivedays.strftime("%Y-%m-%d")) + " is in 5 days! This may affect bike availability.")
    elif (dateinsixdays.strftime("%Y, %m, %d")) in ie_holidays:
        holidaylist.append(ie_holidays.get(dateinsixdays.strftime("%Y-%m-%d")) + " is in 6 days! This may affect bike availability.")
    else:
        holidaylist.append("There are no upcoming holidays. Enjoy your day!")

    # RETURN TO FRONT END
    return render_template ("/index.html", station_list=station_list, labels=labels,day_values=day_values, times=times, qty=qty, holidaylist=holidaylist)

@app.route("/", methods=['GET','POST'])
def index():
    radio = request.form.get('radio')
    #stn = request.form.get('id')


# DATABASE CONNECTION
    mydb = mysql.connector.connect(
        host="dbbikes.cydtuzfevnm7.us-east-1.rds.amazonaws.com",
        user="root",
        passwd="whiterabbit",
        database="dbbikes"
    )
# GENERATE STATION LIST
    # prebuilt function in mysql to interact with a database
    mycursor = mydb.cursor(dictionary=True)
    # Next, we setup our SQL query
    mycursor.execute("SELECT * from stations a, temp_table b where a.number= b.number order by a.address")
    # Then we get some stuff back... By appending a variable to the response of the query
    myresult = mycursor.fetchall()
    # We make an empty list
    station_list=[]
    # for every result we get back, we add that to the list in a new index

    for x in myresult:
        station_list.append(dict((x)))
    # This 'welcomemessage' is an example of passing a variable back into the front end using jinjas2
    welcomemessage = "Hello, welcome to Dublin Bikes!"
    # Then we ALWAYS PRINT STUFF TO MAKE SURE IT'S ACTUALLY RIGHT'
    print(station_list)

    # this json dumps function is essential in returning data back to the front end correctly
    station_list = json.dumps(station_list)

    #getting the holidays for ireland
    # ie_holidays = holidays.IE()
    # print("holidays", date(2017,12,25) in ie_holidays)

    # now = datetime.datetime.now()
    # datetomorrow = datetime.datetime.now() + timedelta(days = 1)
    # dateintwodays = datetime.datetime.now() + timedelta(days=2)
    # dateinthreedays = datetime.datetime.now() + timedelta(days=3)
    # dateinfourdays = datetime.datetime.now() + timedelta(days=4)
    # dateinfivedays = datetime.datetime.now() + timedelta(days=5)
    # dateinsixdays = datetime.datetime.now() + timedelta(days=6)

    # print("current date is: ", now.strftime("%Y-%m-%d"))
    # print("in six days: ", dateinsixdays.strftime("%d %B %Y"))
    # print ("is this easter?", date(2019,4,22) in ie_holidays )

    # holidaylist = []

    # if (now.strftime("%Y, %m, %d")) in ie_holidays:
    #     holidaylist.append(ie_holidays.get(now.strftime("%Y-%m-%d")) + " is today! This may affect bike availability.")
    # if (datetomorrow.strftime("%Y, %m, %d")) in ie_holidays:
    #     holidaylist.append(ie_holidays.get(datetomorrow.strftime("%Y-%m-%d")) + " is tomorrow! This may affect bike availability.")
    # if (dateintwodays.strftime("%Y, %m, %d")) in ie_holidays:
    #     holidaylist.append(ie_holidays.get(dateintwodays.strftime("%Y-%m-%d")) + " is in 2 days! This may affect bike availability.")
    # if (dateinthreedays.strftime("%Y, %m, %d")) in ie_holidays:
    #     holidaylist.append(ie_holidays.get(dateinthreedays.strftime("%Y-%m-%d")) + " is in 3 days! This may affect bike availability.")
    # if (dateinfourdays.strftime("%Y, %m, %d")) in ie_holidays:
    #     holidaylist.append(ie_holidays.get(dateinfourdays.strftime("%Y-%m-%d")) + " is in 4 days! This may affect bike availability.")
    # if (dateinfivedays.strftime("%Y, %m, %d")) in ie_holidays:
    #     holidaylist.append(ie_holidays.get(dateinfivedays.strftime("%Y-%m-%d")) + " is in 5 days! This may affect bike availability.")
    # if (dateinsixdays.strftime("%Y, %m, %d")) in ie_holidays:
    #     holidaylist.append(ie_holidays.get(dateinsixdays.strftime("%Y-%m-%d")) + " is in 6 days! This may affect bike availability.")

    # RETURN TO FRONT END
    # return render_template("/index.html", station_list=station_list, holidaylist=holidaylist)
    return render_template("/index.html", station_list=station_list)
                           

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)