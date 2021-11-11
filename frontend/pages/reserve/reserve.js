// pages/reserve/reserve.js

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    equipmentType2imagePath: [
      '',
      '/resources/images/3DPrinter.jpg',
      '/resources/images/experimentTable.jpg',
      '/resources/images/laserCutter.jpg',
    ],
    equipmentStatus2String: [
      '空闲',
      '拥挤',
      '已满',
    ],
    equipmentList: [
      /*
      {
        equipmentType: 2,
        equipmentName: '实验台',
        equipmentID: 1,
        equipmentStatus: 0,
      },
      {
        equipmentType: 2,
        equipmentName: '实验台',
        equipmentID: 2,
        equipmentStatus: 1,
      },
      {
        equipmentType: 1,
        equipmentName: '3D打印机',
        equipmentID: 1,
        equipmentStatus: 2,
      },
      */
    ],
    dates: [],
    selected: 0,
    notice: '各位同学，为避免不必要的麻烦，请仔细阅读公告，如有问题，请及时反馈！',
    loading: false,
  },

  // 后端数据获取
  getAllEquipmentStatus() {
    const date = new Date();
    const params = this.data.dates[this.data.selected];
    app.$api.reserve.getAllEquipmentStatus(params)
      .then((res) => {
        if (res.data.errCode === 0) {
          this.setData({
            equipmentList: res.data.status,
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

  switchDate(e) {
    if (e.currentTarget.dataset.index != this.data.selected) {
      this.setData({
        selected: e.currentTarget.dataset.index,
      });
      // 判断登录状态
      this.setData({
        loading: true,
      });
      if (app.globalData.login) {
        this.getAllEquipmentStatus();
      } else {
        app.loginCallBack.push(this.getAllEquipmentStatus);
      }
    }
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
      })
    });
    // 判断登录状态
    this.setData({
      loading: true,
    });
    if (app.globalData.login) {
      this.getAllEquipmentStatus();
    } else {
      app.loginCallBack.push(this.getAllEquipmentStatus);
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
    // 更新TabBar
    if (
      typeof this.getTabBar === 'function'
      && this.getTabBar()
    ) {
      this.getTabBar().setData({
        selected: 1,
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
    // 判断登录状态
    this.setData({
      loading: true,
    });
    if (app.globalData.login) {
      this.getAllEquipmentStatus();
    } else {
      app.loginCallBack.push(this.getAllEquipmentStatus);
    }
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
