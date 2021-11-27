/**
 * 管理员接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'notice'

const notice = {
  createNotice(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/createNotice`, params)
  }
}

export default notice
