// utils/util.js

const time = {
  fix(num, length) {
    // 以固定位数显示整数
    return ('' + num).length < length ? ((new Array(length + 1)).join('0') + num).slice(-length) : '' + num;
  },
  // 将hh:mm形式的时间转化为分钟计算
  timeStr2minutes(timeStr) {
    const hour = parseInt(timeStr.substr(0, 2));
    const minute = parseInt(timeStr.substr(3, 2));
    return hour * 60 + minute;
  },
  // 判断所给定时间区间是否与给定区间集相交
  isIntersect(timeInterval0, timeIntervals) {
    let intersect = false;
    timeIntervals.forEach((timeInterval) => {
      if (timeInterval0.startTime < timeInterval.endTime && timeInterval0.endTime > timeInterval.endTime
        || timeInterval0.startTime < timeInterval.startTime && timeInterval0.endTime > timeInterval.startTime) {
        intersect = true;
      }
    });
    return intersect;
  },
  isAvailable(timeInterval0, timeIntervals) {
    let available = false;
    timeIntervals.forEach((timeInterval) => {
      if (timeInterval0.startTime >= timeInterval.startTime && timeInterval0.endTime <= timeInterval.endTime) {
        available = true;
      }
    });
    return available;
  },
  // 判断所给定时间区间在给定区间集时是否有效
  isValid(timeIntervalStr, timeIntervalStrs) {
    const timeInterval0 = {
      startTime: this.timeStr2minutes(timeIntervalStr.startTime),
      endTime: this.timeStr2minutes(timeIntervalStr.endTime),
    };
    if (timeInterval0.endTime - timeInterval0.startTime <= 0) {
      return false;
    }
    if (timeIntervalStrs.length === 0) {
      return false;
    }
    const timeIntervals = timeIntervalStrs.map((timeIntervalStr) => {
      return {
        startTime: this.timeStr2minutes(timeIntervalStr.startTime),
        endTime: this.timeStr2minutes(timeIntervalStr.endTime),
      };
    });
    return this.isAvailable(timeInterval0, timeIntervals);
  }
};

export default time;
