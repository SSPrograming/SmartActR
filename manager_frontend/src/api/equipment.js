/**
 * 设备管理接口
 */
import config from './config'
import axios from './axios'

const subUrl = 'equipment'

const equipment = {
  status2string: {
    'fine': '正常',
    'broken': '损坏'
  },
  getAllEquipmentType() {
    return axios.get(`${config.baseUrl}/${subUrl}/getAllEquipmentType`)
  },
  addEquipmentType(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/addEquipmentType`, params)
  },
  editEquipmentType(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/editEquipmentType`, params)
  },
  deleteEquipmentType(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/deleteEquipmentType`, params)
  },
  getAllEquipment(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/getAllEquipment`, params)
  },
  swapEquipmentOrder(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/swapEquipmentOrder`, params)
  },
  addEquipment(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/addEquipment`, params)
  },
  editEquipment(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/editEquipment`, params)
  },
  deleteEquipment(params) {
    return axios.post(`${config.baseUrl}/${subUrl}/deleteEquipment`, params)
  }
}

export default equipment
