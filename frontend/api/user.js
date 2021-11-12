// api/user.js
/**
 * 用户相关的api
 */
import {
  request
} from './common.js';

const user = {
  login(params) {
    return request({
      url: '/user/login',
      method: 'POST',
      data: params,
    });
  },
  bind(params) {
    return request({
      url: '/user/bind',
      method: 'POST',
      data: params,
    });
  },
  unbind() {
    return request({
      url: '/user/unbind',
      method: 'POST',
    });
  },
  getBindStatus() {
    return request({
      url: '/user/getBindStatus',
      method: 'GET',
    });
  },
  getIdentity() {
    return request({
      url: '/user/getIdentity',
      method: 'GET',
    });
  },
  getStudentInfo() {
    return request({
      url: '/user/getStudentInfo',
      method: 'GET',
    });
  },
};

export default user;
