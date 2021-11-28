/**
 * 预约管理接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'reserve'

const reserve = {
  getTodayRecord() {
    return axios.get(`${config.baseUrl}/${subUrl}/getNoticeList`)
  },
  getHistoryRecord(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/getNoticeList`, params)
  }
}

export default reserve
