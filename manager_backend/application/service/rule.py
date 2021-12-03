from application.database import db
from application.models import Reserve_Record, OccupationInfo
from application.utils import strToTime, strToDate, now, next_weekday
import datetime

class ruleService():
    def addRule(ruleType, ruleContent):
        now_datetime = now()
        now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
        if ruleType==1:
            day = ruleContent['day']
            startTime = ruleContent['startTime']
            endTime = ruleContent['endTime']
            expireDate = ruleContent['expireDate']
            try:
                startTime = strToTime(startTime)
                endTime = strToTime(endTime)
                expireDate = strToDate(expireDate)
                day = int(day)
            except:
                return "bad arguments", False
            print(expireDate,now_date, next_weekday(day), day)
            if day<1 or day>7 or expireDate < now_date or expireDate < next_weekday(day):
                return "无意义的规则", False

            existedRules = OccupationInfo.query.filter(OccupationInfo.expireDate>=now_date).all()
            for rule_ in existedRules:
                if rule_.repeat==1 and rule_.day==day:
                    if rule_.expireDate < next_weekday(day):
                        continue
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "添加规则失败：已有其他规则占用同一时间段", False
                elif rule_.repeat==0 and rule_.date.isoweekday()==day:
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "添加规则失败：已有其他规则占用同一时间段", False

            new_rule = OccupationInfo()
            new_rule.repeat = 1
            new_rule.day = day
            new_rule.startTime = startTime
            new_rule.endTime = endTime
            new_rule.expireDate = expireDate
            try:
                db.session.add(new_rule)
                db.session.commit()
                return "ok", True
            except:
                db.session.rollback()
                return "插入数据库时失败", False
        elif ruleType == 0:
            date = ruleContent['date']
            startTime = ruleContent['startTime']
            endTime = ruleContent['endTime']
            expireDate = ruleContent['expireDate']
            try:
                startTime = strToTime(startTime)
                endTime = strToTime(endTime)
                date = strToDate(date)
                expireDate = strToDate(expireDate)
            except:
                return "bad arguments", False
            if expireDate<now_date or expireDate < date or date < now_date:
                return "无意义的规则", False
            existedRules = OccupationInfo.query.filter(OccupationInfo.expireDate>=now_date).all()
            for rule_ in existedRules:
                if rule_.repeat==1 and rule_.day==date.isoweekday():
                    if rule_.expireDate < next_weekday(rule_.day):
                        continue
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "添加规则失败：已有其他规则占用同一时间段", False
                elif rule_.repeat==0 and rule_.date==date:
                    print(rule_.date)
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "添加规则失败：已有其他规则占用同一时间段", False
            new_rule = OccupationInfo()
            new_rule.repeat = 0
            new_rule.startTime = startTime
            new_rule.endTime = endTime
            new_rule.date = date
            new_rule.expireDate = expireDate
            try:
                db.session.add(new_rule)
                db.session.commit()
                return "ok", True
            except:
                db.session.rollback()
                return "插入数据库时失败", False
        else:
            return "bad arguments", False