// pages/instruction/instruction.js

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    loading: false,
    isFocus: false,
    tagList: [],
    instructionList: [],
    screenedList: [],
    selected: 0,
    loading: false,
    chosenInstructionID: -1,
    instructionContent: "",
  },

  getTagList() {
    app.$api.instruction.getTagList()
      .then((res) => {
        if (res.data.errCode === 0) {
          let List = res.data.tagList;
          List.unshift("全部");
          this.setData({
            tagList: List,
          });
        } else {
          app.dealError(res.data, 'SERVER');
        }
      })
      .catch((err) => {
        app.dealError(err, 'API');
      });
  },

  getInstructionList() {
    app.$api.instruction.getInstructionList()
      .then((res) => {
        if (res.data.errCode === 0) {
          this.setData({
            instructionList: res.data.instructionList,
            screenedList: res.data.instructionList,
          });
        } else {
          app.dealError(res.data, 'SERVER');
        }
      })
      .catch((err) => {
        app.dealError(err, 'API');
      });
    this.setData({
      loading: false,
    });
  },

  screenInstruction(e) {
    if (e.currentTarget.dataset.index === 0) {
      let List = this.data.instructionList;
      this.setData({
        selected: 0,
        screenedList: List,
      });
    } else if (e.currentTarget.dataset.index != this.data.selected) {
      let tag = e.currentTarget.dataset.name;
      let newTagList = [];
      for (let i = 0; i < this.data.instructionList.length; i++) {
        for (let j = 0; j < this.data.instructionList[i].instructionTags.length; j++) {
          if (tag === this.data.instructionList[i].instructionTags[j]) {
            newTagList.push(this.data.instructionList[i]);
          }
        }
      }
      this.setData({
        screenedList: newTagList,
        selected: e.currentTarget.dataset.index,
      });
    }
  },

  openInstruction(e) {
    this.setData({
      chosenInstructionID: e.currentTarget.dataset.instructionId,
    });
    wx.navigateTo({
      url: `/pages/open_instruction/open_instruction?instructionID=${this.data.chosenInstructionID}`,
    })
  },

  search_event(e) {
    let list = this.data.instructionList;
    let value = e.detail.value;
    let new_instruction_list = [];
    for (let i = 0; i < list.length; i++) {
      if (list[i].instructionName.indexOf(value) != -1) {
        new_instruction_list.push(list[i]);
      }
    }
    this.setData({
      screenedList: new_instruction_list,
      selected: 0,
    })
  },

  onPullDownRefresh() {
    this.setData({
      loading: true,
    });
    app.dealThing(this.getTagList);
    app.dealThing(this.getInstructionList);
  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    app.dealThing(this.getTagList);
    app.dealThing(this.getInstructionList);
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() { },

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
