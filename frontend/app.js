// app.js
import $api from 'api/api';
import $util from 'utils/util';

App({
  $api: $api,
  $util: $util,
  globalData: {
    login: false,
  },
  login_timer: null,
  loginCallBack: [],
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
            wx.showToast({
              title: '登录失败',
              icon: 'error',
              duration: 1000,
            });
            console.error(err);
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
    // 解绑（仅用于测试）
    /*
    this.loginCallBack.push(() => {
      this.$api.user.unbind()
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.error(err);
        });
    });
    */
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
            } else {
              // 如果绑定身份，测试返回信息
              this.$api.user.getIdentity()
                .then((res) => {
                  console.log(res.data.identity);
                })
                .catch((err) => {
                  console.error(err);
                });
              this.$api.user.getStudentInfo()
                .then((res) => {
                  console.log(res.data);
                })
                .catch((err) => {
                  console.error(err);
                });
            }
          } else {
            // 如果后端返回错误信息
            console.error(res.data.errMsg);
          }
        })
        .catch((err) => {
          // 如果后端 api 调用失败
          console.error(err);
        });
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
              console.error(res.data.errMsg);
            }
          })
          .catch((err) => {
            // 如果后端 api 调用失败
            console.error(err);
          });
      }
    }
  }
});