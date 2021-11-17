// pages/reserve/reserve.js

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    equipmentType2imagePath: app.$api.reserve.equipmentType2imagePath,
    equipmentInfo: {
      year: 0,
      month: 0,
      date: 0,
      equipmentType: 0,
      equipmentID: 0,
      equipmentStatus: 0,
      equipmentName: '',
      equipmentDescription: '',
    },
    equipmentSpareTime: [],
    startTime: [0, 0],
    endTime: [0, 0],
    hours: [],
    startMinutes: [],
    endMinutes: [],
    loading: false,
  },

  getEquipmentStatus() {
    const params = this.data.equipmentInfo;
    app.$api.reserve.getEquipmentStatus(params)
      .then((res) => {
        if (res.data.errCode === 0) {
          this.setData({
            equipmentInfo: {
              ...params,
              equipmentDescription: res.data.equipmentDescription,
            },
            equipmentSpareTime: [
              {
                startTime: '08:00',
                endTime: '12:00',
              },
              {
                startTime: '13:00',
                endTime: '15:00',
              },
              {
                startTime: '08:00',
                endTime: '22:00',
              },
            ],
            // equipmentSpareTime: res.data.equipmentSpareTime,
          });
        } else {
          app.dealError(res.data, 'SERVER');
        }
        wx.stopPullDownRefresh();
        this.setData({
          loading: false,
        });
      })
      .catch((err) => {
        app.dealError(err, 'API');
        wx.stopPullDownRefresh();
        this.setData({
          loading: false,
        });
      });
  },

  // 当时间滑动改变时
  timeChange(e) {
    let val = e.detail.value;
    let minutes = ['00', '15', '30', '45'];
    if (val[0] === this.data.hours.length - 1) {
      val[1] = 0;
      minutes = ['00'];
    }
    e.currentTarget.dataset.type === 'startTime' ? this.setData({
      startTime: val,
      startMinutes: minutes,
    }) : this.setData({
      endTime: val,
      endMinutes: minutes
    });
  },

  // 当点击按钮调整时间时
  changeTime(e) {
    let time = e.currentTarget.dataset.type === 'startTime' ? this.data.startTime : this.data.endTime;
    const subType = e.currentTarget.dataset.subType === 'hour' ? 0 : 1;
    const length = e.currentTarget.dataset.subType === 'hour' ? this.data.hours.length :
      e.currentTarget.dataset.type === 'startTime' ? this.data.startMinutes.length : this.data.endMinutes.length;
    time[subType] = e.currentTarget.dataset.direction === 'prev' ? (time[subType] - 1 + length) % length : (time[subType] + 1) % length;
    let minutes = ['00', '15', '30', '45'];
    if (time[0] === this.data.hours.length - 1) {
      time[1] = 0;
      minutes = ['00'];
    }
    e.currentTarget.dataset.type === 'startTime' ? this.setData({
      startTime: time,
      startMinutes: minutes,
    }) : this.setData({
      endTime: time,
      endMinutes: minutes,
    });
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.setData({
      equipmentInfo: {
        year: parseInt(options.year),
        month: parseInt(options.month),
        date: parseInt(options.date),
        equipmentType: parseInt(options.equipmentType),
        equipmentID: parseInt(options.equipmentID),
        equipmentName: options.equipmentName,
        equipmentStatus: parseInt(options.equipmentStatus),
      },
      loading: true,
    });
    const hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];
    const minutes = ['00', '15', '30', '45'];
    this.setData({
      hours: hours.map((num) => {
        return app.$util.time.fix(num + 8, 2);
      }),
      startMinutes: minutes,
      endMinutes: minutes,
    });
    app.dealThing(this.getEquipmentStatus);
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },
});
