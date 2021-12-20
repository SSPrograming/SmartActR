//api.insturction.js
/**
 * 使用说明相关api
 */

import {
  request
} from './common.js';

const instruction = {
  getInstructionList() {
    return request({
      url: '/instruction/getInstructionList',
      method: 'GET',
    })
  },
  getTagList() {
    return request({
      url: '/instruction/getTagList',
      method: 'GET',
    })
  },
};

export default instruction;