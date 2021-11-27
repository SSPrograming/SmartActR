/**
 * 管理员接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'notice'

const notice = {
  getNoticeList(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/getNoticeList`, params)
  },
  createNotice(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/createNotice`, params)
  },
  updateNotice(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/updateNotice`, params)
  },
  deleteNotice(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/deleteNotice`, params)
  }
}

export default notice
