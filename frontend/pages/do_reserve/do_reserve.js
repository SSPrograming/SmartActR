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
          console.error(res.data.errMsg);
        }
        wx.stopPullDownRefresh();
        this.setData({
          loading: false,
        });
      })
      .catch((err) => {
        console.error(err);
        wx.stopPullDownRefresh();
        this.setData({
          loading: false,
        });
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
    if (app.globalData.login) {
      this.getEquipmentStatus();
    } else {
      app.loginCallBack.push(this.getEquipmentStatus);
    }
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
