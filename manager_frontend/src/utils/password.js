/**
 * 密码相关工具函数
 */

import crypto from 'crypto'

const salt = process.env.VUE_APP_SALT

const password = {
  getHash(username, password) {
    let obj = crypto.createHash('md5')
    obj.update(username + password + salt)
    return obj.digest('hex')
  }
}

export default password
