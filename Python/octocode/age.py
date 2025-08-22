import datetime
# datetime.datetime: Represents both date and time.
# datetime.date: Represents a date (year, month, day).
# datetime.time: Represents a time (hour, minute, second).
# datetime.timedelta: Represents a duration (difference between two dates/times).
# ===============================================

year_now= datetime.datetime.now().year
month_now= datetime.datetime.now().month
day_now= datetime.datetime.now().day
print(f"Year Now is {year_now}")
# print(month_now)
# print (day_now)
# =============================================

now = datetime.datetime.now()
formatted = now.strftime("%Y-%m-%d \n%H:%M:%S")
# formatted = now.strftime("%H:%M:%S")
# print (now)
print (formatted)
# age= int(input("How Old Are You? : "))

# print (f"You Were Born In The Year  {year_now - age}")