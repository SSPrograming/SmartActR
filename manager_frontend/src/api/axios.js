/**
 * axios配置
 */
import axios from 'axios'
import store from '../store'

/**
 * 请求拦截器
 * 每次请求前，如果存在jwt则在请求头中携带jwt
 */
axios.interceptors.request.use(
    config => {
      const jwt = store.state.jwt
      jwt && (config.headers.Authorization = jwt)
      return config
    },
    error => {
      Promise.error(error)
    }
)

/**
 * 响应拦截器
 */
axios.interceptors.response.use(
    res => res.status === 200 ? Promise.resolve(res) : Promise.reject(res)
)

export default axios
