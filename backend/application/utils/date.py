import datetime
import math
def strToDate(strDate):
    m_datetime =  datetime.datetime.strptime(strDate, "%Y-%m-%d")
    return datetime.date(m_datetime.year, m_datetime.month, m_datetime.day)

def strToTime(strTime):
    m_datetime = datetime.datetime.strptime(strTime, "%H:%M")
    return datetime.time(m_datetime.hour, m_datetime.minute)

def now():
    now = datetime.datetime.now() + datetime.timedelta(hours=8)
    return now

def calculate_total_time(occupationList):
    """
    列表中的时间段不能有重叠
    """
    total_time = datetime.timedelta()
    now_datetime = now()
    now_date = datetime.date(year=now_datetime.year, month=now_datetime.month, day=now_datetime.day)
    for item in occupationList:
        total_time += datetime.datetime.combine(now_date,item["endTime"]) - datetime.datetime.combine(now_date,item["startTime"])
    return total_time

def reduce_to_nowTime(occupationList, date):
    """
    将有序的时间段列表的起始时间转化为当前时间，且round到十五分整,date为日期信息
    """
    occupationList_copy = occupationList
    rem_end = 0
    now_datetime = now()
    now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
    if now_date<date:
        return occupationList_copy
    elif now_date>date:
        return []

    minute_round = math.ceil(now_datetime.minute / 15) * 15
    hour = now_datetime.hour
    if minute_round == 60:
        hour += 1
        minute_round = 0
    now_time = datetime.time(hour=hour, minute=minute_round)
    for item in occupationList_copy:
        if item["endTime"]<=now_time:
            rem_end += 1
        elif item["startTime"]<=now_time:
            item["startTime"] = now_time
        else:
            break
    del occupationList_copy[:rem_end]
    return occupationList_copy

def calculate_spare_time(date):
    now_datetime = now()
    now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)

    if now_date<date:
        return datetime.timedelta(hours=14)
    elif now_date>date:
        return datetime.timedelta(0)
    else:
        minute_round = math.ceil(now_datetime.minute / 15) * 15
        hour = now_datetime.hour
        if minute_round == 60:
            hour += 1
            minute_round = 0
        now_time = datetime.time(hour=hour, minute=minute_round)
        end_time = datetime.time(hour=22, minute=0)
        if now_time>=end_time:
            return datetime.timedelta(0)
        else:
            return datetime.datetime.combine(now_date,end_time)- max(datetime.datetime.combine(now_date,now_time),datetime.datetime(
                now_date.year, now_date.month, now_date.day, 8,0
            ))