// pages/user/user.js

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    identity: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 获取学生信息
    const needToDo = () => {
      app.$api.user.getIdentity()
        .then((res) => {
          if (res.data.errCode === 0) {
            // 如果后端返回正确信息
            this.setData({
              identity: res.data.identity,
            });
          } else {
            // 如果后端返回错误信息
            console.error(res.data.errMsg);
          }
        })
        .catch((err) => {
          // 如果后端 api 调用失败
          console.error(err);
        });
    };
    // 判断登录状态
    if (app.globalData.login) {
      // 如果已登录，则直接调用
      needToDo();
    } else {
      // 如果未登录，则置入登录回调队列
      app.loginCallBack.push(needToDo);
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
        selected: 2,
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
