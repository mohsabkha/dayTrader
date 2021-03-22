from datetime import datetime, timedelta

####################################################################
#PURPOSE: to return the date in a format recognized by the dataframe
#ARGS: n/a
#RETURNS: string
#NOTE: Currently, this should only run when market is closed
#TO-DO: Add functionality that will get hour by hour data
####################################################################
def get_date(date='today'):
    #if no specific date is entered
    if(date == 'today'):
         #check if today is sunday
        if(datetime.date(datetime.today()).weekday() == 6):
            print('Its Sunday')
            date = datetime.today() - timedelta(days=2)
            date = str(date).split()[0]
            closing_time = f'{date} 16:00:00-05:00'
            return closing_time, date
        #check if today is saturday
        elif(datetime.date(datetime.today()).weekday() == 5):
            print('Its Saturday')
            date = datetime.today() - timedelta(days=1)
            date = str(date).split()[0]
            closing_time = f'{date} 16:00:00-05:00'
            del date
            return closing_time, date
        #if not saturday or sunday, but passed market closing, only pull data at closing time
        if(datetime.today().hour >= 15):
            print('Its after market close')
            date = datetime.today()
            date = str(date).split()[0]
            closing_time = f'{date} 16:00:00-05:00'
            return closing_time, date
        #its before market open and its a monday
        elif(datetime.today().hour <= 3 and datetime.date(datetime.today()).weekday() == 0):
            print('Its before market opens and its Monday: Getting data from Friday')
            date = datetime.today() - timedelta(days=3)
            date = str(date).split()[0]
            closing_time = f'{date} 4:00:00-05:00'
            print(date)
            return closing_time, date
        #its before market open and its not monday
        elif(datetime.today().hour <= 3):
            print('Its before market opens')
            date = datetime.today() - timedelta(days=1)
            date = str(date).split()[0]
            closing_time = f'{date} 4:00:00-05:00'
            print(date)
            return closing_time, date
        #if not passed market time, get hour and minute to pull proper data
        else:
            hour = datetime.today().hour
            minute = datetime.today().minute
            date = datetime.today()
            date = str(date).split()[0]
            if(minute >= 11):
                minute = minute - 1
                closing_time = f'{date} {hour+1}:{minute}:00-05:00'
            else:
                minute = minute - 1
                closing_time = f'{date} {hour+1}:0{minute}:00-05:00'
            return closing_time, date
    #if specific date is entered, then just pull closing data from that date
    else:
        closing_time = f'{date} 16:00:00-05:00'
    return closing_time, date
