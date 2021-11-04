// utils/util.js
import $api from '../api/api.js';

const hello = () => {
  console.log('Hello, world!');
};

const login = () => {
  // 登录
  wx.login().then((res) => {
    // 发送 res.code 到后台换取 openId, sessionKey, unionId
    const params = {
      code: res.code
    };
    // 调用后端 api 获取登陆状态
    $api.user.login(params).then((res) => {
      wx.setStorageSync('jwt', res.data.jwt);
    }).catch((err) => {
      console.error(err);
    });
  }).catch((err) => {
    console.error(err);
  });
};

const promptBind = () => {
  // 绑定身份
  wx.showModal({
    title: '温馨提示',
    content: '请绑定您的身份信息',
    showCancel: true,
    cancelText: "取消",
    cancelColor: '#000000',
    confirmText: "确定",
    confirmColor: '#cf3c7f',
    success: (res) => {
      if (res.confirm) {
        // 如果用户选择确定，则跳转至助教的小程序
        wx.navigateToMiniProgram({
          appId: 'wx31f880501d44724a',
          path: 'pages/index/index',
          envVersion: 'trial',
          extraData: {
            origin: 'miniapp',
            type: 'id.tsinghua'
          },
          // 如果用户选择“取消”，则提示失败
          fail: (err) => {
            wx.showToast({
              title: '打开失败',
              icon: 'error',
              duration: 1500
            });
          }
        });
      }
    }
  });
};

export default {
  hello,
  login,
  promptBind
};
