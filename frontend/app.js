// app.js
import $api from 'api/api';
import $util from 'utils/util';

App({
  $api: $api,
  $util: $util,
  globalData: {
    login: false,
    freeze: false,
  },
  login_timer: null,
  loginCallBack: [],
  // 处理事务
  dealThing(func) {
    if (this.globalData.login) {
      func();
    } else {
      this.loginCallBack.push(func);
    }
  },
  // 处理错误
  dealError(err, type) {
    console.error(err);
    if (type === 'API') {
      wx.showToast({
        title: '网络超时',
        icon: 'error',
        duration: 1000,
      });
    } else if (type === 'SERVER') {
      wx.showToast({
        title: '服务器错误',
        icon: 'error',
        duration: 1000,
      });
    } else if (type === 'LOGIN') {
      wx.showToast({
        title: '登录失败',
        icon: 'error',
        duration: 1000,
      });
    }
  },
  login() {
    const needToDo = () => {
      if (!this.globalData.login) {
        this.$util.login()
          .then(() => {
            // 设置登录标志
            this.globalData.login = true;
            // 完成回调函数
            this.loginCallBack.forEach((cbk) => {
              cbk();
            });
            this.loginCallBack = [];
          })
          .catch((err) => {
            // 如果登录失败
            this.dealError(err, 'LOGIN');
          });
      }
    };
    needToDo();
    // 打开定时器以处理登录失败的问题
    this.login_timer = setInterval(needToDo, 10000);
  },

  /**
   * 生命周期函数--监听小程序启动
   */
  onLaunch() {
    // 调用API
    this.$util.hello();
    // 把绑定加入登录回调函数列表
    this.loginCallBack.push(() => {
      // 获取绑定状态
      this.$api.user.getBindStatus()
        .then((res) => {
          if (res.data.errCode === 0) {
            // 如果后端返回正确信息
            if (!res.data.isBind) {
              // 如果没有绑定身份，则打开绑定提示
              this.$util.promptBind();
            }
          } else {
            // 如果后端返回错误信息
            this.dealError(res.data, 'SERVER');
          }
        })
        .catch((err) => {
          // 如果后端 api 调用失败
          this.dealError(err, 'API');
        });
    });
    // 把获取冻结状态加入登录回调列表
    this.loginCallBack.push(() => {
      this.$api.user.getFreezeStatus()
        .then((res) => {
          if (res.data.errCode === 0) {
            // 如果后端返回正确信息
            this.globalData.freezeStatus = res.data.freezeStatus;
            if (res.data.freezeStatus) {
              const date = new Date(res.data.freezeDate);
              date.setDate(date.getDate() + 7);
              this.globalData.freezeDate = date;
              const date_str = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
              wx.showModal({
                title: '冻结提示',
                content: `抱歉，您因为多次违约或恶劣行为被冻结，冻结时间持续到${date_str}，期间您无法进行预约操作`,
                showCancel: false,
                confirmText: '确定',
                confirmColor: '#cf3c7f',
              });
            }
          } else {
            // 如果后端返回错误信息
            this.dealError(res.data, 'SERVER');
          }
        })
        .catch((err) => {
          // 如果后端 api 调用失败
          this.dealError(err, 'API');
        })
    });
    // 登录
    this.login();
  },

  /**
   * 生命周期函数--监听小程序显示
   */
  onShow(options) {
    // 如果是从其他小程序返回（绑定过程）
    if (options.scene === 1038) {
      if (
        options.referrerInfo.extraData &&
        options.referrerInfo.extraData.token
      ) {
        const params = {
          token: options.referrerInfo.extraData.token,
        };
        this.$api.user.bind(params)
          .then((res) => {
            if (res.data.errCode === 0) {
              // 如果绑定成功，则提示
              wx.showToast({
                title: '绑定成功',
                icon: 'success',
                duration: 1000,
              });
            } else {
              // 如果后端返回错误信息
              this.dealError(res.data, 'SERVER');
            }
          })
          .catch((err) => {
            // 如果后端 api 调用失败
            this.dealError(err, 'API');
          });
      }
    }
  }
});
