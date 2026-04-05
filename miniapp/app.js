// app.js - 记账小助手小程序入口
App({
  globalData: {
    isLoggedIn: false,
    userInfo: null,
    token: null,
    apiBaseUrl: 'http://39.107.253.44:8000/api', // 实际API地址
    phone: null,
    deviceInfo: null,
    platform: null,
    isHarmonyOS: false
  },

  onLaunch() {
    // 检查登录状态
    this.checkLoginStatus();
    
    // 获取设备信息，判断平台类型
    this.getDeviceInfo();
  },

  // 获取设备信息
  getDeviceInfo() {
    wx.getDeviceInfo({
      success: (res) => {
        this.globalData.deviceInfo = res;
        this.globalData.platform = res.platform;
        this.globalData.isHarmonyOS = res.platform === 'harmony';
        console.log('设备信息:', res);
        console.log('平台类型:', res.platform);
      },
      fail: (err) => {
        console.error('获取设备信息失败:', err);
      }
    });
  },

  // 检查登录状态
  checkLoginStatus() {
    const token = wx.getStorageSync('token');
    const userInfo = wx.getStorageSync('userInfo');
    
    if (token && userInfo) {
      this.globalData.isLoggedIn = true;
      this.globalData.token = token;
      this.globalData.userInfo = userInfo;
    }
  },

  // 登录方法
  login(username, password) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${this.globalData.apiBaseUrl}/auth/login`,
        method: 'POST',
        data: { phone: username, password },
        success: (res) => {
          if (res.statusCode === 200) {
            const { access_token, token_type } = res.data;
            
            // 获取用户信息
            wx.request({
              url: `${this.globalData.apiBaseUrl}/auth/me`,
              method: 'GET',
              header: {
                'Authorization': `${token_type} ${access_token}`
              },
              success: (userRes) => {
                if (userRes.statusCode === 200) {
                  const user = userRes.data;
                  this.globalData.isLoggedIn = true;
                  this.globalData.token = access_token;
                  this.globalData.userInfo = user;
                  this.globalData.phone = username;
                  
                  wx.setStorageSync('token', access_token);
                  wx.setStorageSync('userInfo', user);
                  wx.setStorageSync('phone', username);
                  
                  resolve({ token: access_token, user });
                } else {
                  reject({ message: '获取用户信息失败' });
                }
              },
              fail: (err) => {
                reject(err);
              }
            });
          } else {
            reject(res.data);
          }
        },
        fail: (err) => {
          reject(err);
        }
      });
    });
  },

  // 退出登录
  logout() {
    this.globalData.isLoggedIn = false;
    this.globalData.token = null;
    this.globalData.userInfo = null;
    this.globalData.phone = null;
    
    wx.removeStorageSync('token');
    wx.removeStorageSync('userInfo');
    wx.removeStorageSync('phone');
  },

  // 获取请求头
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json'
    };
    if (this.globalData.token) {
      headers['Authorization'] = `Bearer ${this.globalData.token}`;
    }
    return headers;
  }
});
