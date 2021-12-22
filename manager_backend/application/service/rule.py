from requests.sessions import merge_setting
from application.database import db
from application.models import Reserve_Record, ruleTable
from application.utils import strToTime, strToDate, now, next_weekday, WechatService
import datetime
from application.service import UserService, EquipmentService
from config import query_yaml


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
            if day<1 or day>7 or expireDate < now_date or expireDate < next_weekday(day):
                return "无意义的规则", False

            existedRules = ruleTable.query.filter(ruleTable.expireDate>=now_date).all()
            for rule_ in existedRules:
                if rule_.repeat==1 and rule_.day==day:
                    if rule_.expireDate < next_weekday(day):
                        continue
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "添加规则失败：已有其他规则占用同一时间段", False
                elif rule_.repeat==0 and rule_.date.isoweekday()==day:
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "添加规则失败：已有其他规则占用同一时间段", False

            new_rule = ruleTable()
            new_rule.repeat = 1
            new_rule.day = day
            new_rule.startTime = startTime
            new_rule.endTime = endTime
            new_rule.expireDate = expireDate
            new_rule.ruleDescription = ruleContent['ruleDescription']
            


            # 将冲突的预约记录标记为取消
            conflict_record_list = []
            record_list = Reserve_Record.query.filter(Reserve_Record.status=="成功",
                                                      Reserve_Record.reserveDate>=now_date,
                                                      Reserve_Record.reserveDate<=expireDate).all()
            for record in record_list:
                if record.reserveDate.isoweekday()==day:
                    if not (record.startTime>=endTime or record.endTime <= startTime):
                        conflict_record_list.append(record)
            
            token, getStatus = WechatService.getAccessToken()
            for record in conflict_record_list:
                try:
                    record.status='取消'
                    db.session.commit()
                    if getStatus:
                        messageContent = ruleService.compute_cancel_message(record)
                        WechatService.sendMessage(content=messageContent, token=token)
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    return "更新数据库失败", False

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
            existedRules = ruleTable.query.filter(ruleTable.expireDate>=now_date).all()
            for rule_ in existedRules:
                if rule_.repeat==1 and rule_.day==date.isoweekday():
                    if rule_.expireDate < next_weekday(rule_.day):
                        continue
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "添加规则失败：已有其他规则占用同一时间段", False
                elif rule_.repeat==0 and rule_.date==date:
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "添加规则失败：已有其他规则占用同一时间段", False
            new_rule = ruleTable()
            new_rule.repeat = 0
            new_rule.startTime = startTime
            new_rule.endTime = endTime
            new_rule.date = date
            new_rule.expireDate = expireDate
            new_rule.ruleDescription = ruleContent['ruleDescription']
            
            token, getStatus = WechatService.getAccessToken()
            # 将冲突的预约记录标记为取消
            conflict_record_list = []
            record_list = Reserve_Record.query.filter(Reserve_Record.status=="成功",
                                                      Reserve_Record.reserveDate==date).all()
            for record in record_list:
                if not (record.startTime>=endTime or record.endTime <= startTime):
                    conflict_record_list.append(record)
            for record in conflict_record_list:
                try:
                    record.status='取消'
                    db.session.commit()
                    if getStatus:
                        messageContent = ruleService.compute_cancel_message(record)
                        WechatService.sendMessage(content=messageContent, token=token)
                except:
                    db.session.rollback()
                    return "更新数据库失败", False

            try:
                db.session.add(new_rule)
                db.session.commit()
                return "ok", True
            except Exception as e:
                print(e)
                db.session.rollback()
                return "插入数据库时失败", False
        else:
            return "bad arguments", False
    
    def get_rule_list():
        now_datetime = now()
        now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
        rule_list = ruleTable.query.filter(ruleTable.expireDate>=now_date).all()
        return rule_list
    
    def updateRule(ruleID, ruleType, ruleContent):
        now_datetime = now()
        now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
        target_rule = ruleTable.query.filter(ruleTable.ruleID==ruleID).first()
        if target_rule is None:
            return "规则不存在", False
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
            if day<1 or day>7 or expireDate < now_date or expireDate < next_weekday(day):
                return "无意义的规则", False

            existedRules = ruleTable.query.filter(ruleTable.expireDate>=now_date).all()
            for rule_ in existedRules:
                if rule_.ruleID==ruleID:
                    continue
                if rule_.repeat==1 and rule_.day==day:
                    if rule_.expireDate < next_weekday(day):
                        continue
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "更新规则失败：已有其他规则占用同一时间段", False
                elif rule_.repeat==0 and rule_.date.isoweekday()==day:
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "更新规则失败：已有其他规则占用同一时间段", False

            target_rule.repeat = 1
            target_rule.day = day
            target_rule.startTime = startTime
            target_rule.endTime = endTime
            target_rule.expireDate = expireDate
            target_rule.ruleDescription = ruleContent['ruleDescription']

            token, getStatus = WechatService.getAccessToken()
            # 将冲突的预约记录标记为取消
            conflict_record_list = []
            record_list = Reserve_Record.query.filter(Reserve_Record.status=="成功",
                                                      Reserve_Record.reserveDate>=now_date,
                                                      Reserve_Record.reserveDate<=expireDate).all()
            for record in record_list:
                if record.reserveDate.isoweekday()==day:
                    if not (record.startTime>=endTime or record.endTime <= startTime):
                        conflict_record_list.append(record)
            for record in conflict_record_list:
                try:
                    record.status='取消'
                    db.session.commit()
                    if getStatus:
                        messageContent = ruleService.compute_cancel_message(record)
                        WechatService.sendMessage(content=messageContent, token=token)
                except:
                    db.session.rollback()
                    return "更新数据库失败", False

            try:
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
            existedRules = ruleTable.query.filter(ruleTable.expireDate>=now_date).all()
            for rule_ in existedRules:
                if rule_.ruleID==ruleID:
                    continue
                if rule_.repeat==1 and rule_.day==date.isoweekday():
                    if rule_.expireDate < next_weekday(rule_.day):
                        continue
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "更新规则失败：已有其他规则占用同一时间段", False
                elif rule_.repeat==0 and rule_.date==date:
                    if not (rule_.startTime>=endTime or rule_.endTime<=startTime):
                        return "更新规则失败：已有其他规则占用同一时间段", False
            target_rule.repeat = 0
            target_rule.startTime = startTime
            target_rule.endTime = endTime
            target_rule.date = date
            target_rule.expireDate = expireDate
            target_rule.ruleDescription = ruleContent['ruleDescription']

            token, getStatus = WechatService.getAccessToken()
            # 将冲突的预约记录标记为取消
            conflict_record_list = []
            record_list = Reserve_Record.query.filter(Reserve_Record.status=="成功",
                                                      Reserve_Record.reserveDate==date).all()
            for record in record_list:
                if not (record.startTime>=endTime or record.endTime <= startTime):
                    conflict_record_list.append(record)
            for record in conflict_record_list:
                try:
                    record.status='取消'
                    db.session.commit()
                    if getStatus:
                        messageContent = ruleService.compute_cancel_message(record)
                        WechatService.sendMessage(content=messageContent, token=token)
                except:
                    db.session.rollback()
                    return "更新数据库失败", False

            try:
                db.session.commit()
                return "ok", True
            except Exception as e:
                print(e)
                db.session.rollback()
                return "插入数据库时失败", False
        else:
            return "bad arguments", False

    def deleteRule(ruleID):
        target_rule = ruleTable.query.filter(ruleTable.ruleID==ruleID).first()
        if target_rule is None:
            return "规则不存在", False
        try:
            db.session.delete(target_rule)
            db.session.commit()
            return "ok", True
        except:
            db.session.rollback()
            return "更新数据库失败", False

    
    def compute_cancel_message(record):
        messageContent = {}
        messageContent_data = {}
        messageContent["touser"] = record.userID
        messageContent["template_id"] = query_yaml('app.TEMPLATEID')
        messageContent_data["name1"] = {"value":UserService.get_name_by_id(record.userID)}
        messageContent_data["time22"] = {"value":str(record.reserveDate) + ' ' + record.startTime.strftime("%H:%M")}
        messageContent_data["time23"] = {"value":str(record.reserveDate) + ' ' + record.endTime.strftime("%H:%M")}
        messageContent_data["thing8"] = {"value":"预约取消提醒: " + EquipmentService.get_name_by_type(record.equipmentType)[0] + str(record.equipmentID) + '号'}
        messageContent_data["thing7"] = {"value":"活动室被占用"}
        messageContent["data"] = messageContent_data
        return messageContent
