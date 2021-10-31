# 前端

&emsp;&emsp;该文件夹为“智慧活动室”小程序的前端部分，其目录结构为

```bash
├─api/
│  ├─api.js             # api接口的统一出口
|  └─...                # 其他的api文件
├─pages/
│  ├─common/            # 所有页面共同的部分
│  ├─components/        # 所有页面共用的组件
│  ├─{{ page }}/        # 页面
|  |  ├─components/     # 该页面使用的组件
|  |  ├─{{ page }}.js   # 页面的js文件
|  |  ├─{{ page }}.json # 页面的json文件
|  |  ├─{{ page }}.wxml # 页面的结构文件
|  |  └─{{ page }}.wxss # 页面的样式文件
├─resources/            # 资源文件
│  ├─icons/             # 图标
│  │  └─toolbar/        # 工具栏图标
│  └─images/            # 图片
├─utils/                # 工具函数集
|  └─util.js            # 工具函数js文件
├─app.js                # 小程序的js文件（启动入口）
├─app.json              # 小程序的配置文件
├─app.wxss              # 小程序的样式文件
├─project.config.json   # 项目的配置文件
└─sitemap.jspn          # 配置搜索规则
```

## API使用规则

&emsp;&emsp;不同类型的API分别写在不同的JS文件（如`api/user.js`）中，并在`api/api.js`中加入。`api/api.js`已挂在全局实例APP中，在页面JS文件中可以通过以下方式调用：

```js
const app = getApp();
// 调用user.js中的一个API
app.$api.user.login(code);
```

&emsp;&emsp;`utils/util.js`使用方法类似。

```js
const app = getApp();
app.$util.hello();
```

## 页面文件

&emsp;&emsp;页面文件放在`pages`文件夹下，每个页面一个文件夹，可以使用组件。一个页面文件夹下至少包括`.js`、`.json`、`.wxml`与`.wxss`四个文件，分别对应逻辑、配置、结构与样式。

## 资源文件

&emsp;&emsp;资源文件放在`resources`文件夹下。

