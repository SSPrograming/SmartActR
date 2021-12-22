// pages/open_instruction.js

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    instructionID: "",
    instructionContent: "",
  },

  getSingleInstruction() {
    let params = {
      "instructionID": this.data.instructionID,
    }
    app.$api.instruction.getSingleInstruction(params)
      .then((res) => {
        if (res.data.errCode === 0) {
          console.log(res);
          this.setData({
            instructionContent: res.data.instructionContent,
          });
          let WxParse = require('../../wxParse/wxParse.js');
          let content = this.data.instructionContent;
          let that = this;
          WxParse.wxParse('content', 'html', content, that, 30)
        } else {
          app.dealError(res.data, 'SERVER');
        }
      })
      .catch((err) => {
        app.dealError(err, 'API');
      })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      instructionID: options.instructionID,
    });
    app.dealThing(this.getSingleInstruction);
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