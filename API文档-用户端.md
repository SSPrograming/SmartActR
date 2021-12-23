# 用户端接口


- [x] **用户相关** 

@bp_user**.**route('/user-api/v1/user/login', methods=['POST'])

> 登录接口

params：

```
{
	"code": "<code>"
}
```

ret：

```
{
	"jwt": "jwt",
	"errCode": "errcode", #0表示成功，1表示出错
	"errMsg": "errMsg"
}
```



@bp_user.route('/user-api/v1/user/bind', methods=['POST'])

@login_required

> 绑定接口

params：

```
{
	"token": "ticket", #后端利用token获取学生信息
}
```

ret:

```
{
	"errCode": "errcode", #0表示成功，1表示出错
	"errMsg": "errMsg"
}
```



@bp_user.route('/user-api/v1/user/getBindStatus', methods=['GET'])

@login_required

ret:

```
{
	"errCode": "errcode", #0表示成功，1表示出错, 2表示jwt过期
	"errMsg": "errMsg",
	"isBind": BOOL
}
```



@bp_user('/user-api/v1/user/getIdentity', methods=['GET'])

@login_required

ret:

```
{
	"errCode": "errcode", #0表示成功，1表示出错, 2表示jwt过期
	"errMsg": "errMsg",
	"identity": "xxx"
}
```



@bp_user('/user-api/v1/user/getStudentInfo', methods=['GET'])

@login_required

ret:

```
{
	"errCode": "errcode", #0表示成功，1表示出错, 2表示jwt过期
	"errMsg": "errMsg",
	"stuID": "2018****010",
	"department": "xxx"
}
```



@bp_instruction('/user-api/v1/instruction/getInstructionList', method=['GET'])

@login_required

ret:

```
{
	"instructionList":
	[
		{
			"instructionID": number,
			"instructionName": "",
			"instructionTags": 
			[
				"",""
			],
			"instructionCoverURL": ""
		}
	]
}
```



@bp_instruction('/user-api/v1/instruction/getSingleInstruction', method=['POST'])

@login_required

params:

```
{
	"instructionID": number
}
```

ret:

```
{
	"instructionContent": "",
}
```



@bp_instruction.route('/user-api/v1/instruction/getFreezeStatus', method=['GET'])

@login_required

ret:

```
{
	"freezeStatus": bool,
	"freezeDate": ""
}
```

****

- [x] **预约相关**

@bp_reserve.route('/user-api/v1/reserve/getAllEquipmentStatus', methods=['POST'])

@login_required

> 获取全部设备信息

params

```
{
	"year": number,
	"month": number,
	"day": number
}
```

ret:

```
{
	"errCode": number,
	"errMsg": "",
	"status":
	[
		{
			"equipmentType": number,
			"equipmentName": "name",
			"equipmentID": number,
			"equipmentStatus": number, #0空闲，1拥挤，2已满
			"equipmentImageURL": ""
		}
	]
}
```



@bp_reserve.route('/user-api/v1/reserve/getEquipmentStatus', methods=['POST'])

@login_required

> 获取某一台设备信息

params

```
{
	"year": number,
	"month": number,
	"day": number，
	"equipmentType": number,
	"equipmentID": number
}
```

ret:

```
{
	"errCode": number,
	"errMsg": "",
	"equipmentName": "name",
	"equipmentDescription": "",
	"equipmentImageURL": "",
	"equipmentSpareTime": 
	[
		{
			"startTime": "", #时间格式: hh:mm
			"endTime": ""
		}	# 保证返回正确的时间
	]
}
```



@bp_reserve.route('/user-api/v1/reserve/reserveEquipment', methods=['POST'])

@login_required

> 预约设备

params:

```
{
	"startTime": "", 
	"endTime": "",
	"year": number,
	"month": number,
	"date": number,
	"equipmentType": number,
	"equipmentID": number
}
```



ret:

```
{
	"errCode": number,
	"errMsg": ""
}
```



@bp_reserve.route('/user-api/v1/reserve/getCurrentReserveInfo', methods=['GET'])

@login_required

> 获取当前预约信息，今天及以后

ret:

```
{	"errCode": number,
	"info":
	[
		"reserveID": number,
		"equipmentName": "",
		"equipmentID": number,
		"startTime": "",
		"endTime": "",
		"year": number,
		"month": number,
		"date": number,
		"status": ""
	]
}
```



@bp_reserve.route('/user-api/v1/reserve/getHistoryReserveInfo', methods=['GET'])

@login_required

> 获取历史预约信息

ret:

```
{	"errCode": number,
	"info":
	[	
		{
			"reserveID": number,
			"equipmentName": "",
			"equipmentID": number,
			"startTime": "",
			"endTime": "",
			"year": number,
			"month": number,
			"date": number,
			"status": ""
		}
	]
}
```



@bp_reserve.route('/user-api/v1/checkIn', methods=['POST'])

@login_required

params:

```
{
	"hashCode": "",	#已加密
}
```

ret:

```
{
	"errCode": number,
	"checkInStatus": number, 	#0为签到成功，1为码无效，2为无相关记录
	"errMsg": ""
}
```



@bp_reserve.route('/user-api/v1/reserve/cancelReserve', methods=['POST'])

@login_required

> 取消某次预约

params:

```
{
	"reserveID": number
}
```

ret:

```
{
	"errCode": number
}
```

****

- [x] **公告相关**

@bp_notice.route('/user-api/v1/reserve/getNotice', methods=['GET'])

@login_required

ret:

```
{
	"errCode": number,
	"errMsg": "",
	"noticeContent": "",
    "noticeDate": "", #格式的样例："2021-11-09"
    "expireDate": "", #格式的样例："2021-11-12"
}
```
