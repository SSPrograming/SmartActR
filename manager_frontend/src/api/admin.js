/**
 * 管理员接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'amdin'

const admin = {
  getAdminName() {
    return axios.get(`${config.baseUrl}/${subUrl}/getAdminName`)
  }
}

export default admin