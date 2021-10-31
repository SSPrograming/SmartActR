// app.js
import api from "api/api.js";
import util from "utils/util.js";

App({
  $api: api,
  $util: util,
  globalData: {

  },
  onLaunch() {
    // 调用API
    this.$util.hello();
    // 登录
    wx.login().then((res) => {
      // 发送 res.code 到后台换取 openId, sessionKey, unionId
      console.log(res);
      this.$api.user.login(res.code);
    }).catch((err) => {
      console.error(err);
    });
  }
});
