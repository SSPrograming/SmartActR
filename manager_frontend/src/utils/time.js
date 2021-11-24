/**
 * 时间函数
 */

const time = {
  day2str(day) {
    const map = ['日', '一', '二', '三', '四', '五', '六']
    return map[day]
  },
  fix(num, length) {
    // 以固定位数显示整数
    return ('' + num).length < length ? ((new Array(length + 1)).join('0') + num).slice(-length) : '' + num
  }
}

export default time