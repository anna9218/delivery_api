from datetime import datetime, timedelta
from time import asctime, strptime

def get_weekdates():
    weeknum = datetime.now().isocalendar()[1] -1
    startdate = asctime(strptime('2021 %d 0' % weeknum, '%Y %W %w'))
    startdate = datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
    dates = [startdate.strftime('%d-%m-%y')]
    for i in range(1, 7):
        day = startdate + timedelta(days=i)
        dates.append(day.strftime('%Y-%m-%d'))
    return dates

