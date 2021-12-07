/**
 * 使用说明管理接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'instruction'

const instruction = {
  getInstructionList() {
    return axios.get(`${config.baseUrl}/${subUrl}/getInstructionList`)
  },
  addInstruction(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/addInstruction`, params)
  },
  updateInstruction(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/updateInstruction`, params)
  },
  deleteInstruction(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/deleteInstruction`, params)
  },
  getSingleInstruction(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/getSingleInstruction`, params)
  },
  addImage(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/addImage`, params)
  },
  updateContent(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/updateContent`, params)
  }
}

export default instruction
