// pages/instruction/instruction.js

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    loading: false,
    tag_list: [{
      name: "tag1"
    }, {
      name: "tag2"
    }, {
      name: "tag3"
    }],
    equipmentList: [],

  },

  getAllEquipmentStatus() {
    const params = {
      year: 2021,
      month: 12,
      date: 9,
      day: "周四"
    };
    app.$api.reserve.getAllEquipmentStatus(params)
      .then((res) => {
        if (res.data.errCode === 0) {
          this.setData({
            equipmentList: res.data.status,
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

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    app.dealThing(this.getAllEquipmentStatus);
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
    // 更新TabBar
    if (
      typeof this.getTabBar === 'function' &&
      this.getTabBar()
    ) {
      this.getTabBar().setData({
        selected: 0,
      });
    }
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