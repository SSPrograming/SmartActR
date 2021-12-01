/**
 * 设备管理接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'equipment'

const equipment = {
  status2string: [
    '正常',
    '损坏'
  ],
  getAllEquipmentType() {
    return axios.get(`${config.baseUrl}/${subUrl}/getAllEquipmentType`)
  },
  testPicUpload(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/testPicUpload`, params)
  }
}

export default equipment
