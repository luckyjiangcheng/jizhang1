// pages/login/login.js
const app = getApp()

Page({
  data: {
    username: '',
    password: ''
  },

  // 用户名输入
  onUsernameInput(e) {
    this.setData({ username: e.detail.value })
  },

  // 密码输入
  onPasswordInput(e) {
    this.setData({ password: e.detail.value })
  },

  // 登录
  handleLogin() {
    const { username, password } = this.data
    
    if (!username) {
      wx.showToast({ title: '请输入用户名', icon: 'none' })
      return
    }
    
    if (!password) {
      wx.showToast({ title: '请输入密码', icon: 'none' })
      return
    }

    wx.showLoading({ title: '登录中...' })
    
    // 调用后端登录接口
    wx.request({
      url: `${app.globalData.apiBaseUrl}/auth/login`,
      method: 'POST',
      data: {
        phone: username, // 后端接口使用phone字段接收登录凭证
        password: password
      },
      success: (res) => {
        wx.hideLoading()
        
        if (res.statusCode === 200) {
          const { access_token, token_type } = res.data
          
          // 获取用户信息
          wx.request({
            url: `${app.globalData.apiBaseUrl}/auth/me`,
            method: 'GET',
            header: {
              'Authorization': `${token_type} ${access_token}`
            },
            success: (userRes) => {
              if (userRes.statusCode === 200) {
                const userInfo = userRes.data
                
                // 登录成功，存储用户信息和token
                app.globalData.isLoggedIn = true
                app.globalData.userInfo = userInfo
                app.globalData.token = access_token
                
                wx.setStorageSync('token', access_token)
                wx.setStorageSync('userInfo', userInfo)
                
                wx.showToast({
                  title: '登录成功',
                  icon: 'success'
                })
                
                // 跳转到首页
                setTimeout(() => {
                  wx.switchTab({
                    url: '/pages/index/index'
                  })
                }, 1000)
              } else {
                wx.showToast({
                  title: '获取用户信息失败',
                  icon: 'none',
                  duration: 2000
                })
              }
            },
            fail: (err) => {
              wx.hideLoading()
              wx.showToast({
                title: '获取用户信息失败',
                icon: 'none',
                duration: 2000
              })
            }
          })
        } else {
          // 登录失败
          wx.showToast({
            title: res.data.detail || '登录失败',
            icon: 'none',
            duration: 2000
          })
        }
      },
      fail: (err) => {
        wx.hideLoading()
        wx.showToast({
          title: '网络错误，请稍后重试',
          icon: 'none',
          duration: 2000
        })
      }
    })
  },

  // 跳转产品介绍
  goToProduct() {
    wx.navigateTo({
      url: '/pages/product/product'
    })
  }
})
