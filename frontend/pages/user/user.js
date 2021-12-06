// pages/user/user.js
import $util from '../../utils/util';
import $api from '../../api/api';

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    identity: '',
    loading: false,
    isShowNotice: false,
    reservationList: [],
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
            app.dealError(res.data, 'SERVER');
          }
        })
        .catch((err) => {
          // 如果后端 api 调用失败
          app.dealError(err, 'API');
        });
    };
    app.dealThing(needToDo);
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  //跳转历史记录
  seeRecord(e) {
    wx.navigateTo({
      url: `/pages/reserve_history/reserve_history`,
    })
  },

  //活动室使用须知
  showNotice(e) {
    wx.showModal({
      title: "使用须知",
      content: "1. 活动室内禁止吃东西\r\n2. 活动室里禁止卖萌\r\n3. 活动室里禁止使用2进制",
      showCancel: false,
    })
  },

  //扫码签到
  scanCode(e) {
    wx.scanCode({
      onlyFromCamera: true,
      success(res) {
        console.log(res)
      },
      fail(err) {

      }
    })
  },



  //身份绑定
  identityCheck() {
    app.$api.user.getBindStatus()
      .then((res) => {
        if (res.data.errCode === 0) {
          // 如果后端返回正确信息
          if (!res.data.isBind) {
            // 如果没有绑定身份，则打开绑定提示
            app.$util.openBind();
          } else if (res.data.isBind) {
            wx.showModal({
              content: "您已经绑定身份",
              confirmText: "解绑身份",
              success(res) {
                if (res.confirm) {
                  //解绑身份
                  app.$api.user.unbind()
                    .then((res) => {
                      console.log(res);
                    })
                    .catch((err) => {
                      this.dealError(err, 'API');
                    });
                }
              },


            })
          }
        } else {
          // 如果后端返回错误信息
          app.dealError(res.data, 'SERVER');
        }
      })
      .catch((err) => {
        // 如果后端 api 调用失败
        app.dealError(err, 'API');
      });
  },

  //意见反馈
  feedBack() {
    wx.showModal({
      title: "意见反馈",
      content: "请输入您的反馈意见~",
      editable: true,
      placeholderText: "点击此处输入",
      confirmText: "提交",
      success(res) {
        if (res.confirm) {
          console.log(res.content);
        } else if (res.cancel) {
          console.log("取消");
        }
      },
    })
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