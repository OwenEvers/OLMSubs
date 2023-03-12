import datetime
import calendar


def find_month(m: int):
    if m == 1:
        return 'January'
    if m == 2:
        return 'February'
    if m == 3:
        return 'March'
    if m == 4:
        return 'April'
    if m == 5:
        return 'May'
    if m == 6:
        return 'June'
    if m == 7:
        return 'July'
    if m == 8:
        return 'August'
    if m == 9:
        return 'September'
    if m == 10:
        return 'October'
    if m == 11:
        return 'November'
    if m == 12:
        return 'December'
    return 'N/A'


def find_Month_Num(m: str):

    monthText = m
    monthNum = 0
    now = datetime.datetime.today()
    yearNow = now.year
    monthNow = now.month
    #monthNow = 4
    dayNow = now.day
    #dayNow = 1
    lastDays = 0
    if monthText == 'February':
        monthNum = 2

    if monthText == 'April':
        monthNum = 4

    if monthText == 'June':
        monthNum = 6

    if monthText == 'August':
        monthNum = 8

    if monthText == 'October':
        monthNum = 10

    if monthText == 'December':
        monthNum = 12

    if (monthNow % 2) != 0:
        #print("odd")        # odd month so published last issue monthNow minus 1
        liMonth = monthNow - 1
        if monthNow == 1:
            liMonth = 12
        lastDays = find_days_in_month(liMonth) # get tot days from last month

    else:
        liMonth = monthNow - 2
        #print("even")       # even month so published last issue monthNow
        liDays = find_days_in_month(liMonth)


    #print(f"day is {dayNow} in month {monthNow} last issue month is {liMonth}")
    nowdays = find_days_in_month(monthNow)
    y = float(nowdays + lastDays)            # total days till next issue
    x = float(lastDays + dayNow)          # days passed from last issue
    per = 100
    retNum = x * per / y
    #print(f"Year is {yearNow} so month {monthNow} has {nowdays} days")
    return retNum


def find_days_in_month(m: int):
    global days
    now = datetime.datetime.today()
    yearNow = now.year
    monthNow = m
    if monthNow in (1, 3, 5, 7, 8, 10, 12):
        days = 31
    elif monthNow in (4, 6, 9, 11):
        days = 30
    elif monthNow == 2:
        if (yearNow % 4 == 0) and (not (yearNow % 100 == 0) or (yearNow % 400 == 0)):
            days = 29
        else:
            days = 28
    return days
    #print(f"Year is {yearNow} so month {monthNow} has {days} days")


#find_Month_Num("April")
