/**
 * 规则接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'rules'

const rule = {
  getRules() {
    return axios.get(`${config.baseUrl}/${subUrl}/getRules`)
  },
  addRule(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/addRule`, params)
  }
}

export default rule
