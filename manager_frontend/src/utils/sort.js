/**
 * 排序的统一入口
 */

/**
 * 排序对象数组
 * @param array 数组
 * @param sortType 排序方式 {prop: String, order: String}
 * @param primaryKey 主键
 */
const sort = (array, sortType, primaryKey) => {
  array.sort((a, b) => {
    const var1 = a[sortType.prop]
    const var2 = b[sortType.prop]
    const asc = sortType.order === 'ascending'
    if (var1 < var2) {
      return asc ? -1 : 1
    } else if (var1 > var2) {
      return asc ? 1 : -1
    } else {
      if (primaryKey) {
        if (a[primaryKey] < b[primaryKey]) {
          return asc ? -1 : 1
        } else if (a[primaryKey] > b[primaryKey]) {
          return asc ? 1 : -1
        } else {
          return 0
        }
      } else {
        return 0
      }
    }
  })
}

export default sort
