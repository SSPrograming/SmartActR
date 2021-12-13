/**
 * 提示消息的统一入口
 */

/**
 * 提示消息
 * @param that 调用该函数的组件指针
 * @param message 需要提示的消息
 * @param type 'success', 'warning', 'info', 'error'
 */
const alertMessage = (that, message, type) => {
  switch (type) {
    case 'success':
      that.$message({
        message: message,
        type: 'success',
        duration: 3000
      })
      break
    case 'warning':
      that.$message({
        message: message,
        type: 'warning',
        duration: 3000
      })
      break
    case 'info':
      that.$message({
        message: message,
        type: 'info',
        duration: 3000
      })
      break
    case 'error':
      that.$message({
        message: message,
        type: 'error',
        duration: 3000
      })
      break
    default:
      console.warn('Unknown alert type: ' + type)
  }
}

export default alertMessage
