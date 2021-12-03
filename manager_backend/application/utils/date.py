import datetime

def strToDate(strDate):
    m_datetime =  datetime.datetime.strptime(strDate, "%Y-%m-%d")
    return datetime.date(m_datetime.year, m_datetime.month, m_datetime.day)

def strToTime(strTime):
    m_datetime = datetime.datetime.strptime(strTime, "%H:%M")
    return datetime.time(m_datetime.hour, m_datetime.minute)

def now():
    now = datetime.datetime.now() + datetime.timedelta(hours=8)
    return now

def next_weekday(day):
    if day<1 or day > 7:
        return None
    now_datetime = now()
    now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
    for i in range(0,7):
        if (now_date + datetime.timedelta(days=i)).isoweekday() == day:
            return now_date + datetime.timedelta(days=i)