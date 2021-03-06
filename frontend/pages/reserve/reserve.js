// pages/reserve/reserve.js

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    equipmentStatus2String: app.$api.reserve.equipmentStatus2String,
    equipmentList: [],
    dates: [],
    selected: 0,
    notice: '各位同学，为避免不必要的麻烦，请仔细阅读公告，如有问题，请及时反馈！',
    noticeDate: '',
    noticeContents: [],
    isShowNotice: false,
    loading: false,
  },

  // 后端数据获取
  getAllEquipmentStatus() {
    const params = this.data.dates[this.data.selected];
    //console.log(params);
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

  // 后端获取公告
  getNotice() {
    app.$api.reserve.getNotice()
      .then((res) => {
        if (res.data.errCode === 0) {
          let show = false;
          const date = new Date(res.data.expireDate);
          date.setDate(date.getDate() + 1);
          if (new Date() <= date) {
            show = true;
          }
          this.setData({
            noticeDate: res.data.noticeDate,
            noticeContents: res.data.noticeContent.trim().split('\n'),
            isShowNotice: show
          });
        } else {
          app.dealError(res.data, 'SERVER');
        }
      })
      .catch((err) => {
        app.dealError(err, 'API');
      })
  },

  showNotice(e) {
    this.setData({
      isShowNotice: true
    });
  },

  hideNotice(e) {
    this.setData({
      isShowNotice: false
    });
  },

  onEnter(e) { },

  switchDate(e) {
    if (e.currentTarget.dataset.index != this.data.selected) {
      this.setData({
        selected: e.currentTarget.dataset.index,
        loading: true,
      });
      app.dealThing(this.getAllEquipmentStatus);
    }
  },

  doReserve(e) {
    const target_equipment = this.data.equipmentList[e.currentTarget.dataset.index];
    wx.navigateTo({
      url: `/pages/do_reserve/do_reserve?equipmentType=${target_equipment.equipmentType}&equipmentID=${target_equipment.equipmentID}&equipmentName=${target_equipment.equipmentName}&equipmentStatus=${target_equipment.equipmentStatus}&equipmentImageURL=${target_equipment.equipmentImageURL}&year=${this.data.dates[this.data.selected].year}&month=${this.data.dates[this.data.selected].month}&date=${this.data.dates[this.data.selected].date}`,
    });
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 获取当前及7天内日期信息
    const numbers = [0, 1, 2, 3, 4, 5, 6];
    const day2string = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    this.setData({
      dates: numbers.map((num) => {
        const date = new Date();
        date.setDate(date.getDate() + num);
        return {
          year: date.getFullYear(),
          month: date.getMonth() + 1,
          date: date.getDate(),
          day: day2string[date.getDay()],
        };
      }),
      loading: true,
    });
    app.dealThing(this.getNotice);
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
        selected: 1,
      });
    }
    app.dealThing(this.getAllEquipmentStatus);
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
    this.setData({
      loading: true,
    });
    app.dealThing(this.getAllEquipmentStatus);
    app.dealThing(this.getNotice);
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
