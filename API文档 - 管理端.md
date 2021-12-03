
# 管理端接口

- [x] **登录**

@bp_notice.route('/api/v1/admin/login', methods=['POST'])

params

```
{
	"username":"",
	"password":"" "加盐散列"
}
```

ret:

```
{
	"errCode":number,
	"jwt": "",
	"errMsg":""
}
```

****

- [x] **公告相关**

@bp_notice.route('/api/v1/notice/getNoticeList', methods=['POST'])

params:

````
{
	"num": number, #-1表示全部
	"queryType": number,	#时间为1，内容为2，不搜索为0，结合为3
	"queryStartDate": "",
	"queryEndDate": "",
	"queryStr": ""
}
````

ret:

```
{
	noticeList:
	[
		{
			"noticeID": number,
			"postDate": "",
			"expireDate": "",
			"content": ""
		}
	]
}
```



@bp_notice.route('/api/v1/notice/createNotice', methods=['POST'])

params:

```
{
	"noticeContent": "",
	"expireDate": ""
}
```

ret:

```
{
	"errCode": "",
	"errMsg": ""
}
```



@bp_notice.route('/api/v1/notice/updateNotice', methods=['POST'])

params:

```
{
	"noticeContent": "",
	"expireDate": "",	#例如2021-11-25
	"noticeID": number
}
```

ret:

```
{
	"errCode": "",
	"errMsg": ""
}
```



@bp_notice.route('/api/v1/notice/deleteNotice', methods=['POST'])

params:

```
{
	"noticeID": number
}
```

ret:

```
{
	"errCode": "",
	"errMsg": ""
}
```

****

- [x] **预约管理**

@bp_notice.route('/api/v1/reserve/getTodayRecord', methods=['GET'])

@login_required

ret:

```
{
	"recordList":
	[
		{
			"recordID":number,
			"postTime": "",
			"reserveDate": "",
			"startTime": "",
			"endTime": "",
			"userName": "",
			"status": "",
			"equipmentName": ""
		}
	]
}
```



@bp_notice.route('/api/v1/reserve/getHistoryRecord', methods=['POST'])

@login_required

params:

```
{
	"startDate": "",
	"endDate": ""
}
```

ret:

```
{
	"recordList":
	[
		{
			"recordID":number,
			"postTime": "",
			"reserveDate": "",
			"startTime": "",
			"endTime": "",
			"userID": "",
			"status": "",
			"equipmentName": ""
		}
	]
}
```

****

**设备详情**：

展示有哪些种类的设备：

@bp_equipment.route('/api/v1/equipment/getAllEquipmentType', methods=['GET'])

@login_required

ret:

```
{
	"TypeList":
	[
		{
			"equipmentType": number,
			"equipmentName": "",
			"equipmentDescription": "",
			"equipmentCount": number
			"equipmentImage": ""		#图床路径
		}
	]
}
```



获取某设备种类的所有设备信息：

@bp_equipment.route('/api/v1/equipment/getEquipmentList', methods=['POST'])

@login_required

params:

```
{
	"equipmentType": number
}
```

ret:

```
{
	"equipmentList":
	[
		{
			"equipmentID": number,
			"status": "",
			"equipmentName":""
		}
	]
}
```





添加新的设备种类：

@bp_equipment.route('/api/v1/equipment/addEquipmentType', methods=['POST'])

@login_required

params: **form-data**

```
{
	"equipmentName": "",
	"equipmentCount": number,
	"equipmentDescription": "",
	"equipmentImage": ""	
}
```

ret:

```
{
	"errCode":number
}
```





编辑设备种类：

@bp_equipment.route('/api/v1/equipment/editEquipmentType', methods=['POST'])

@login_required

params: **form-data**

```
{
	"equipmentType": number,
	"equipmentName": "",						#optional
	"equipmentDescription": "",					#optional
	"equipmentImage": ""						#optional
}
```

ret:

```
{
	"errCode":
	"errMsg":
}
```



删除设备种类：

@bp_equipment.route('/api/v1/equipment/deleteEquipmentType', methods=['POST'])

@login_required

```
{
	"equipmentType": number
}
```

ret:

```
{
	"errCode":
}
```



交换设备顺序：

@bp_equipment.route('/api/v1/equipment/swapEquipmentOrder', methods=['POST'])

@login_required

```
{
	"equipmentType1": number,
	"equipmentType2": number
}
```

ret:

```
{
	"errCode":
}
```





添加设备：

@bp_equipment.route('/api/v1/equipment/addEquipment', methods=['POST'])

@login_required

params:

```
{
	"equipmentType":number
}
```

ret:

```
{
	"errCode":
	"errMsg":
}
```



编辑设备状态：

@bp_equipment.route('/api/v1/equipment/editEquipment', methods=['POST'])

@login_required

params:

```
{
	"equipmentType":number,
	"equipmentID": number,
	"equipmentStatus": ""
}
```

ret:

```
{
	"errCode":
	"errMsg":	
}
```



获取设备预约记录：

@bp_equipment.route('/api/v1/equipment/getEquipmentRecordList', methods=['POST'])

@login_required

params:

```
{
	"equipmentType": number,
	"equipmentID": number
}
```

ret:

```
{
	"RecordList":
	[
		{
			"recordID":number,
			"postTime": "",
			"reserveDate": "",
			"startTime": "",
			"endTime": "",
			"userName": "",
			"status": "",
		}
	]
}
```





删除设备：

@bp_equipment.route('/api/v1/equipment/deleteEquipment', methods=['POST'])

@login_required

```
{
	
}
```

****

**二维码查看**：

@bp_equipment.route('/api/v1/qrcode/getQRCode', methods=['POST'])

@login_required

params:

```
{
	"equipmentType":
	"equipmentID":
}
```

ret:

```
{
	"qrcodeURL": ""
}
```



@bp_equipment.route('/api/v1/qrcode/refreshQRCode', methods=['POST'])

@login_required

params:

```
{
	"equipmentType":
	"equipmentID":
}
```

ret:

```
{
	"errCode":
	"qrcodeURL":
}
```

****

#### 独占规则

@bp_rule.route('/api/v1/rules/addRule',methods=['POST'])

@login_required

params:

```
{
	"repeat": number, 	#1表示重复，0表示不重复
	"day": number, 		#周几
	"date": ""			# 2021-21-11
	"startTime": ""		# 20:17
	"endTime":   ""		# 20:18
	"expireDate": ""	# 1202-20-21
}
```

ret:

```
{
	"errCode": number,
	"errMsg": ""
}
```



@bp_rule.route('/api/v1/rules/deleteRule',methods=['POST'])

@login_required

params

```
{
	"ruleID": number
}
```

ret:

```
{
	"errCode":
}
```



@bp_rule.route('/api/v1/rules/getRules',methods=['GET'])

@login_required

>  获取尚未失效的规则

ret:

```
{
	rules:
	[
		{
			"repeat": number, 	#1表示重复，0表示不重复
			"day": number, 		#周几
			"date": "",			# 2021-21-11
			"startTime": "",		# 20:17
			"endTime":   "",		# 20:18
			"expireDate": "",	# 1202-20-21
			"ruleID": number
		}
	]
}
```



****

**使用说明**

@bp_instruction.route('/api/v1/instruction/addInstruction',methods=['POST'])

@login_required

params:

```
{
	"instructionName": "",
	"instructionContent": ""
	"instructionTags": 
	[
		"",""
	]
}
```

ret:

```
{
	"errCode":
}
```



@bp_instruction.route('/api/v1/instruction/addImage',methods=['POST'])

@login_required

params: **form-data**

```
{
	key: "file", value: an image
}
```

ret:

```
{
	"ImageURL": ""	
}
```



@bp_instruction.route('/api/v1/instruction/updateInstruction',methods=['POST'])

@login_required

params:

```
{
	"instructionName": "",
	"instructionContent": "",
	"instructionID": number,
	"instructionTags": 
	[
		"",""
	]
}
```

ret:

```
{
	"errCode":
}
```



@bp_instruction.route('/api/v1/instruction/getInstructionList',methods=['POST'])

@login_required

ret:

```
{
	InstructionList:
	[
		{
			"instructionID":
			"instructionName":
			"instructionContent":
			"instructionTags":
			[
				"",""
			]
		}
	]
}
```



@bp_instruction.route('/api/v1/instruction/deleteInstruction',methods=['POST'])

@login_required

params:

```
{
	"instructionID": ""
}
```

ret:

```
{
	"errCode": 
}
```

****

**用户管理**

@bp_instruction.route('/api/v1/user/queryUserInfo',methods=['POST'])

@login_required

params:

```
{
	"stuID": "", 		#optional
	"stuName": "", 		#optional
	"department": ""	#optional
}
```

ret:

```
{
	"stuList":
	[
		{
			"stuID": "", 		
			"stuName": "", 		
			"department": "",	
			"email": "",
			"cellphone": "",
			"status": ""
		}
	]
}
```



@bp_instruction.route('/api/v1/user/updateUserStatus',methods=['POST'])

@login_required

params:

```
{
	"stuID": "",
	"status": ""
}
```

ret：

```
{
	"errCode"
}
```



****

**反馈**

@bp_instruction.route('/api/v1/feedback/getFeedbackList',methods=['POST'])

@login_required

```
{
	"startDate": "",
	"endDate": "",
	"limitNum": number
}
```

ret:

```
{
	"feedbackList":
	[
		{
			"feedbackID": number,
			"postDate": "",
			"feedbackContent": "",
			"stu"
		}
	]
}
```

