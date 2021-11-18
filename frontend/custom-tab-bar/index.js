// custom-tab-bar/index.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据
   */
  data: {
    selected: null,
    color: '#999999',
    selectedColor: '#999999',
    list: [
      {
        pagePath: '/pages/instruction/instruction',
        text: '使用说明',
        iconPath: '/resources/icons/toolbar/instruction.png',
        selectedIconPath: '/resources/icons/toolbar/instruction-selected.png',
      },
      {
        pagePath: '/pages/reserve/reserve',
        text: '预约',
        iconPath: '/resources/icons/toolbar/reserve.png',
        selectedIconPath: '/resources/icons/toolbar/reserve-selected.png',
      },
      {
        pagePath: '/pages/user/user',
        text: '用户',
        iconPath: '/resources/icons/toolbar/user.png',
        selectedIconPath: '/resources/icons/toolbar/user-selected.png',
      },
    ],
  },

  /**
   * 组件的方法列表
   */
  methods: {
    switchTab(e) {
      const data = e.currentTarget.dataset;
      const url = data.path;
      wx.switchTab({ url });
    },
  },
});
