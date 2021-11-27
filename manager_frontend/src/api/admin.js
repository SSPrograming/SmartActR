/**
 * 管理员接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'admin'

const admin = {
  login(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/login`, params)
  }
}

export default admin
