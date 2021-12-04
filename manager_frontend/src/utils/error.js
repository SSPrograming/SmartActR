/**
 * 错误的统一处理借口
 */

import alertMessage from './alertMessage'

const error = {
  // 服务器错误
  ServerError(that, err) {
    console.log(err)
    alertMessage(that, '网络超时', 'warning')
  },
  /**
   * API调用返回错误
   * @param that 调用该函数的组件指针
   * @param err 错误信息{ errCode: number, errMsg: String }
   * @constructor
   */
  APIError(that, err) {
    console.log(err)
    alertMessage(that, err.errMsg, 'error')
  }
}

export default error
