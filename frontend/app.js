// app.js
import api from 'api/api.js';
import util from 'utils/util.js';

App({
  $api: api,
  $util: util,
  globalData: {

  },
  onLaunch() {
    // 调用API
    this.$util.hello();
    this.$util.login();
    this.$util.promptBind();
  },
  onShow(options) {
    // 如果是从其他小程序返回
    if (options.scene === 1038) {
      if (options.referrerInfo.extraData) {
        console.log(options.referrerInfo.extraData);
      }
    }
  }
});
