// config.js
/**
 * 将wx.request包装成Promise
 */
import config from './config';

export const request = (params) => {
  return new Promise((resolve, reject) => {
    wx.request({
      ...params,
      header: {
        Authorization: wx.getStorageSync('jwt') || ''
      },
      url: config.baseUrl + params.url,
      success: (res) => {
        resolve(res);
      },
      fail: (err) => {
        reject(err);
      },
    });
  });
};
