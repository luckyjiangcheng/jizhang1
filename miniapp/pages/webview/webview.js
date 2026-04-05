// pages/webview/webview.js
Page({
  data: {
    url: ''
  },

  onLoad(options) {
    if (options.url) {
      this.setData({
        url: decodeURIComponent(options.url)
      });
    }
    console.log('Webview loaded');
  },

  onError(e) {
    console.error('Webview error:', e);
    wx.showToast({
      title: '加载失败，请重试',
      icon: 'none'
    });
  }
});