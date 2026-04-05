// pages/contact/contact.js
Page({
  data: {},

  onLoad() {},

  // 打开获客链接
  openCustomerLink() {
    console.log('openCustomerLink called');
    const customerLink = 'https://work.weixin.qq.com/ca/cawcde4716ce3659af';
    
    // 直接显示模态框，提示用户复制链接到浏览器打开
    // 因为小程序的web-view组件不支持打开微信内部链接
    wx.showModal({
      title: '添加企业微信',
      content: '请复制以下链接到浏览器中打开，添加企业微信客服：\n\n' + customerLink,
      showCancel: true,
      cancelText: '取消',
      confirmText: '复制链接',
      success: (res) => {
        console.log('Modal success:', res);
        if (res.confirm) {
          wx.setClipboardData({
            data: customerLink,
            success: () => {
              console.log('Link copied');
              wx.showToast({
                title: '链接已复制，请在浏览器中打开',
                icon: 'success',
                duration: 2000
              });
            },
            fail: (err) => {
              console.error('Copy failed:', err);
              wx.showToast({
                title: '复制失败，请手动复制链接',
                icon: 'none'
              });
            }
          });
        }
      },
      fail: (err) => {
        console.error('Modal failed:', err);
        wx.showToast({
          title: '操作失败，请稍后重试',
          icon: 'none'
        });
      }
    });
  },

  // 复制邮箱
  copyEmail() {
    wx.setClipboardData({
      data: 'support@jizhang.com',
      success: () => {
        wx.showToast({
          title: '已复制',
          icon: 'success'
        });
      }
    });
  }
});