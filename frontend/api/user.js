// api/user.js
/**
 * 用户相关的api
 */
import { request } from './common.js';

const user = {
    login(params) {
        return request({
            url: '/user/login',
            method: 'POST',
            data: params
        });
    },
    bind(params) {
        return request({
            url: '/user/bind',
            method: 'POST',
            data: params
        });
    },
    getBindStatus() {
        return request({
            url: '/user/getBindStatus',
            method: 'POST'
        });
    },
    getIdentity() {
        return request({
            url: '/user/getIdentity',
            method: 'POST'
        });
    },
    getStudentInfo() {
        return request({
            url: '/user/getStudentInfo',
            method: 'POST'
        });
    }
};

export default user;
