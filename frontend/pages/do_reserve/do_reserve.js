// pages/reserve/reserve.js

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    equipmentInfo: {
      year: 0,
      month: 0,
      date: 0,
      equipmentType: 0,
      equipmentID: 0,
      equipmentStatus: 0,
      equipmentName: '',
      equipmentImageURL: '',
      equipmentDescription: '',
    },
    equipmentSpareTime: [],
    startTime: [0, 0],
    endTime: [0, 0],
    hours: [],
    startMinutes: [],
    endMinutes: [],
    loading: false,
    picking: false,
  },

  getEquipmentStatus() {
    const params = {
      ...this.data.equipmentInfo
    };
    delete params.equipmentName;
    delete params.equipmentStatus;
    app.$api.reserve.getEquipmentStatus(params)
      .then((res) => {
        if (res.data.errCode === 0) {
          this.setData({
            equipmentInfo: {
              ...this.data.equipmentInfo,
              equipmentDescription: res.data.equipmentDescription,
            },
            equipmentSpareTime: res.data.equipmentSpareTime,
          });
          if (Array.isArray(this.data.equipmentSpareTime) && this.data.equipmentSpareTime.length > 0) {
            let st = this.data.equipmentSpareTime[0]['startTime'].split(":");
            let sh = parseInt(st[0]) - 8;
            let sm = parseInt(st[1]) / 15;
            let et = this.data.equipmentSpareTime[this.data.equipmentSpareTime.length - 1]['endTime'].split(":");
            let eh = parseInt(et[0]) - 8;
            let em = parseInt(et[1]) / 15;
            if (eh - sh > 4) {
              eh = sh + 4;
              em = sm;
            }
            this.setData({
              startTime: [sh, sm],
              endTime: [eh, em],
            });
          }
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

  // 时间滑动选择相关相关
  pickQueue: [],

  pickStart() {
    this.setData({
      picking: true,
    });
  },

  pickEnd() {
    this.setData({
      picking: false,
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
      endMinutes: minutes,
    });
    this.pickQueue.forEach((cbk) => {
      cbk();
    });
    this.pickQueue = [];
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

  doReserve() {
    const needToDo = () => {
      //判断冻结

      //判断是否bind
      app.$api.user.getBindStatus()
        .then((res) => {
          if (res.data.errCode === 0) {
            if (res.data.isBind) {
              const needToDo = () => {
                const timeInterval = {
                  // 格式：'hh:mm'
                  startTime: this.data.hours[this.data.startTime[0]] + ':' + this.data.startMinutes[this.data.startTime[1]],
                  endTime: this.data.hours[this.data.endTime[0]] + ':' + this.data.endMinutes[this.data.endTime[1]],
                };
                if (app.$util.time.isValid(timeInterval, this.data.equipmentSpareTime)) {
                  const params = {
                    ...timeInterval,
                    ...this.data.equipmentInfo,
                  };
                  delete params.equipmentDescription;
                  delete params.equipmentName;
                  delete params.equipmentStatus;
                  app.$api.reserve.reserveEquipment(params)
                    .then((res) => {
                      if (res.data.errCode === 0) {
                        wx.showModal({
                          title: '预约成功',
                          content: '请在用户界面查看预约记录！',
                          showCancel: false,
                          confirmText: '确定',
                          confirmColor: '#cf3c7f',
                          success(res) {
                            if (res.confirm) {
                              wx.switchTab({
                                url: '/pages/reserve/reserve',
                              });
                            }
                          }
                        });
                        this.setData({
                          loading: true,
                        });
                        app.dealThing(this.getEquipmentStatus);
                      } else {
                        app.dealError(res.data, 'SERVER');
                      }
                    })
                    .catch((err) => {
                      app.dealError(err, 'API');
                    });
                } else {
                  wx.showModal({
                    title: '预约失败',
                    content: '请选择正确的时间段！',
                    showCancel: false,
                    confirmText: '确定',
                    confirmColor: '#cf3c7f',
                  });
                }
              };
              if (this.data.picking) {
                this.pickQueue.push(needToDo);
              } else {
                needToDo();
              }
            } else {
              app.$util.promptBind();
            }
          } else {
            app.dealError(res.data, 'SERVER');
          }
        })
        .catch((err) => {
          app.dealError(err, 'API');
        });
    };
    app.dealThing(needToDo);
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    const hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];
    const minutes = ['00', '15', '30', '45'];
    this.setData({
      equipmentInfo: {
        year: parseInt(options.year),
        month: parseInt(options.month),
        date: parseInt(options.date),
        equipmentType: parseInt(options.equipmentType),
        equipmentID: parseInt(options.equipmentID),
        equipmentName: options.equipmentName,
        equipmentImageURL: options.equipmentImageURL,
        equipmentStatus: parseInt(options.equipmentStatus),
      },
      hours: hours.map((num) => {
        return app.$util.time.fix(num + 8, 2);
      }),
      startMinutes: minutes,
      endMinutes: minutes,
      loading: true,
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
  onShow() { },

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
    app.dealThing(this.getEquipmentStatus);
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
