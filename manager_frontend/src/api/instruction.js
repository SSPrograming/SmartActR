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
  getSingleInstructionImageList(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/getSingleInstructionImageList`, params)
  },
  addImage(params, onUploadProgress, rawFile) {
    return axios({
      url: `${config.baseUrl}/${subUrl}/addImage`,
      method: 'post',
      data: params,
      onUploadProgress: (ev) => {
        ev.percent = ev.loaded * 100 / ev.total || 0
        onUploadProgress(ev, rawFile)
      }
    })
  },
  deleteImage(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/deleteImage`, params)
  },
  updateContent(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/updateContent`, params)
  }
}

export default instruction
