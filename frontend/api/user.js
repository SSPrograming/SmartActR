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
    }
};

export default user;
