/**
 * 用户接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'user'

const user = {
  queryUserInfo(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/queryUserInfo`, params)
  }
}

export default user
