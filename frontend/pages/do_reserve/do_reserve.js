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
    minitues: [],
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
            // equipmentSpareTime: res.data.equipmentSpareTime,
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
            ]
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

  timeChange(e) {
    if (e.currentTarget.dataset.type === 'startTime') {
      const val = e.detail.value;
      this.setData({ startTime: val });
    } else if (e.currentTarget.dataset.type === 'endTime') {
      const val = e.detail.value;
      this.setData({ endTime: val });
    }
  },

  changeTime(e) {
    let time = e.currentTarget.dataset.type === 'startTime' ? this.data.startTime : this.data.endTime;
    const subType = e.currentTarget.dataset.subType === 'hour' ? 0 : 1;
    const length = e.currentTarget.dataset.subType === 'hour' ? this.data.hours.length : this.data.minutes.length;
    time[subType] = (time[subType] + 1) % length;
    e.currentTarget.dataset.type === 'startTime' ? this.setData({
      startTime: time,
    }) : this.setData({
      endTime: time,
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
      minutes,
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
