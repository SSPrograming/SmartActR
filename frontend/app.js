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
    this.$api.user.login();
  }
});
