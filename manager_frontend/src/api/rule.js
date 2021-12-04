/**
 * 规则接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'rule'

const rule = {
  addRule(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/addRule`, params)
  }
}

export default rule
