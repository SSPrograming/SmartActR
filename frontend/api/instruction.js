//api.insturction.js
/**
 * 使用说明相关api
 */

import {
  reqiest
} from './common.js';

const reserve = {
  getInstructionList() {
    return request({
      url: '/instruction/getInstructionList',
      method: 'GET',
    })
  },
};

export default {
  ...reserve,
}