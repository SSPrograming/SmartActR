// utils/util.js
import $api from '../api/api';

const hello = () => {
  console.log('Hello, world!');
};

const login = () => {
  return new Promise((resolve, reject) => {
    // 登录
    wx.showLoading({
      title: '登录中',
      mask: true,
      fail: (err) => { },
    });
    wx.login()
      .then((res) => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        const params = {
          code: res.code,
        };
        // 调用后端 api 获取登陆状态
        $api.user.login(params)
          .then((res) => {
            wx.hideLoading({ fail: (err) => { } });
            if (res.data.errCode === 0) {
              // 如果后端返回正确信息
              try {
                wx.setStorageSync('jwt', res.data.jwt);
                // 至此获取登录凭证成功
                resolve();
              } catch (err) {
                reject(err);
              }
            } else {
              // 如果后端返回错误信息
              // TODO: 增加更多的错误处理
              console.error(res.data.errMsg);
            }
          })
          .catch((err) => {
            // 如果后端 api 调用失败
            wx.hideLoading({ fail: (err) => { } });
            console.error(err);
          });
      })
      .catch((err) => {
        // 如果微信登录失败
        wx.hideLoading({ fail: (err) => { } });
        console.error(err);
      });
  });
};

const openBind = () => {
  // 跳转至助教的小程序
  wx.navigateToMiniProgram({
    appId: 'wx31f880501d44724a',
    path: 'pages/index/index',
    envVersion: 'trial',
    extraData: {
      origin: 'miniapp',
      type: 'id.tsinghua',
    },
    // 如果用户选择取消打开小程序，则提示打开失败
    fail: (err) => {
      wx.showToast({
        title: '打开失败',
        icon: 'error',
        duration: 1000,
      });
    },
  });
};

const promptBind = () => {
  // 绑定身份
  wx.showModal({
    title: '温馨提示',
    content: '请绑定您的身份信息',
    showCancel: true,
    cancelText: '取消',
    cancelColor: '#000000',
    confirmText: '确定',
    confirmColor: '#cf3c7f',
    success: (res) => {
      if (res.confirm) {
        // 如果用户选择确定，则开始绑定
        openBind();
      };
    },
  });
};

export default {
  hello,
  login,
  promptBind,
  openBind,
};
