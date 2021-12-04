// pages/reserve_history/reserve_history.js

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    selected: 0, //0当前预约，1历史预约
    reservation_list: {},
    loading: false,
    reservationStatus2imagePath: [],

  },

  switch_current() {
    this.setData({
      selected: 0,
    })
    app.dealThing(this.getCurrentReserveInfo);
  },

  switch_history() {
    this.setData({
      selected: 1,
    })
    app.dealThing(this.getHistoryReserveInfo);
  },

  getHistoryReserveInfo() {
    app.$api.reserve.getHistoryReserveInfo()
      .then((res) => {
        if (res.data.errCode === 0) {
          this.setData({
            reservation_list: res.data.info,
          });
          console.log(this.data.reservation_list);
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

  getCurrentReserveInfo() {
    app.$api.reserve.getCurrentReserveInfo()
      .then((res) => {
        if (res.data.errCode === 0) {
          this.setData({
            reservation_list: res.data.info,
          });
          console.log(this.data.reservation_list);
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

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    app.dealThing(this.getCurrentReserveInfo);
    this.setData({
      reservationStatus2imagePath: {
        '成功': '/resources/images/reserve_success.png',
        '完成': '/resources/images/reserve_finish.png',
        '违约': '/resources/images/reserve_fail.png',
        '取消': '/resources/images/reserve_cancel.png',
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})