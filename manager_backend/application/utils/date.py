import datetime

def strToDate(strDate):
    m_datetime =  datetime.datetime.strptime(strDate, "%Y-%m-%d")
    return datetime.date(m_datetime.year, m_datetime.month, m_datetime.day)

def strToTime(strTime):
    m_datetime = datetime.datetime.strptime(strTime, "%H:%M")
    return datetime.time(m_datetime.hour, m_datetime.minute)