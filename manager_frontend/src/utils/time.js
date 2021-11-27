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
  },
  format(date, fmt) {
    const o = {
      'M+': date.getMonth() + 1,
      'd+': date.getDate(),
      'h+': date.getHours(),
      'm+': date.getMinutes(),
      's+': date.getSeconds(),
      'q+': Math.floor((date.getMonth() + 3) / 3),
      'S': date.getMilliseconds()
    };
    if (/(y+)/.test(fmt)) {
      fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length));
    }
    for (let k in o) {
      if (new RegExp('(' + k + ')').test(fmt)) {
        fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)));
      }
    }
    return fmt;
  }
}

export default time