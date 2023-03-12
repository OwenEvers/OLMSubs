from datetime import datetime


def getStarDate():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    secs = now.second

    year = str(year)
    year = year[2:]
    if month < 10:
        month = "0" + str(month)

    if day < 10:
        day = "0" + str(day)

    if hour < 10:
        hour = "0" + str(hour)

    if minute < 10:
        minute = "0" + str(minute)



    st = str(year) + str(month) + str(day) + "." + str(hour) + str(minute) + str(secs)
    return st


st = getStarDate()
