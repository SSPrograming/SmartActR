/**
 * 二维码接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'qrcode'

const qrcode = {
  getQRCode(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/getQRCode`, params)
  },
  refreshQRCode(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/refreshQRCode`, params)
  }
}

export default qrcode
