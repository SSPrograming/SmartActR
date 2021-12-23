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
    });
  },
  getTagList() {
    return request({
      url: '/instruction/getTagList',
      method: 'GET',
    });
  },
  getSingleInstruction(params) {
    return request({
      url: '/instruction/getSingleInstruction',
      method: 'POST',
      data: params,
    });
  },
  getREADME() {
    return request({
      url: '/instruction/getREADME',
      method: 'GET',
    });
  },
};

export default instruction;
