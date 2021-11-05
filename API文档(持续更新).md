/api/v1/user/login

POST

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



@bp.route('/api/v1/user/bind', methods=['POST'])

@login_required

> 绑定接口

params：

```
{
	"ticket": "ticket", #后端利用token获取学生信息
}, header中存放jwt
```

ret:

```
{
	"errCode": "errcode", #0表示成功，1表示出错
	"errMsg": "errMsg"
}
```



@bp.route('/api/v1/user/getBindStatus', methods=['GET'])

@login_required

ret:

```
{
	"errCode": "errcode", #0表示成功，1表示出错, 2表示jwt过期
	"errMsg": "errMsg",
	"isBind": BOOL
}
```



@bp.route('/api/v1/user/getIdentity', methods=['GET'])

@login_required

ret:

```
{
	"errCode": "errcode", #0表示成功，1表示出错, 2表示jwt过期
	"errMsg": "errMsg",
	"identity": "xxx"
}
```



@bp.route('/api/v1/user/getStudentInfo', methods=['GET'])

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

