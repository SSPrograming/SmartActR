/**
 * 使用说明管理接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'instruction'

const instruction = {
  addInstruction(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/addInstruction`, params)
  }
}

export default instruction
