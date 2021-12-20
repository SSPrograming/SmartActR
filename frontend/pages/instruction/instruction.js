// pages/instruction/instruction.js

const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    loading: false,
    isFocus: false,
    tag_list: [{
        "tagName": "开心",
      }, {
        "tagName": "蛤",
      }, {
        "tagName": "官方",
      }



    ],
    instructionList: [],
    screenedList: [],
    selected: -1,
    loading: false,

  },

  selectTag(e) {
    if (e.currentTarget.dataset.index != this.data.selected) {
      this.setData({
        selected: e.currentTarget.dataset.index,
        loading: true,
      })
    };
    app.dealThing(this.getInstructionInfo);
  },

  getInstructionList() {
    app.$api.reserve.getInstructionList()
      .then((res) => {
        this.setData({
          instructionList: res.data.instructionList,
          screenedList: res.data.instructionList,
        });
        console.log(this.data.instructionList);
      });
    this.setData({
      loading: false,
    });
  },

  screenInstruction(e) {
    if (e.currentTarget.dataset.index != this.data.selected) {
      let tag = e.currentTarget.dataset.name;
      let newTagList = [];
      //console.log(tag);
      //console.log(this.data.instructionList);
      for (var i = 0; i < this.data.instructionList.length; i++) {
        //console.log(this.data.instructionList[i]);
        for (var j = 0; j < this.data.instructionList[i].instructionTags.length; j++) {
          if (tag === this.data.instructionList[i].instructionTags[j]) {
            newTagList.push(this.data.instructionList[i]);
          }
        }
      }
      this.setData({
        screenedList: newTagList,
        selected: e.currentTarget.dataset.index,
      })
    } else {
      let List = this.data.instructionList;
      this.setData({
        selected: -1,
        screenedList: List,
      })
    }

  },

  openInstruction(e) {
    console.log(e.currentTarget.dataset);
  },

  test1(e) {
    console.log(e.currentTarget.dataset);
    console.log("wonderful");
  },


  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    //app.dealThing(this.getAllEquipmentStatus);
    app.dealThing(this.getInstructionList);
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {},

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