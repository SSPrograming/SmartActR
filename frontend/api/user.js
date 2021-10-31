// api/user.js
/**
 * 用户相关的api
 */

import config from './config.js';

const user = {
    login() {
        // 登录
        wx.login().then(res => {
            // 发送 res.code 到后台换取 openId, sessionKey, unionId
            console.log(res);
            wx.request({
                url: config.url,
                data: {
                    code: res.code
                },
                method: 'POST',
                success(res) {
                    console.log(res);
                    wx.setStorageSync('jwt', res.jwt);
                },
                fail(err) {
                    console.log(err);
                }
            });
        }).catch(err => {
            console.error(err);
        });
    }
};

export default user;