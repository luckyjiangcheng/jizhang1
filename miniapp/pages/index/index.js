// pages/index/index.js
const app = getApp()

// 虚拟数据
const MOCK_DATA = {
  monthlyExpense: 3580.50,
  transactionCount: 42,
  hasBudget: true,
  budgetPercent: 68,
  budgetRemaining: 1200,
  recentTransactions: [
    { id: 1, item: '午餐', category: '餐饮美食', icon: '🍜', amount: 45.00, date: '2024-03-28' },
    { id: 2, item: '打车', category: '交通出行', icon: '🚗', amount: 28.00, date: '2024-03-28' },
    { id: 3, item: '超市购物', category: '居家生活', icon: '🏠', amount: 128.50, date: '2024-03-27' },
    { id: 4, item: '电影票', category: '休闲娱乐', icon: '🎮', amount: 98.00, date: '2024-03-26' },
    { id: 5, item: '加油', category: '交通出行', icon: '🚗', amount: 300.00, date: '2024-03-25' }
  ]
}

Page({
  data: {
    isLoggedIn: false,
    userInfo: null,
    currentMonth: '',
    monthlyExpense: 0,
    transactionCount: 0,
    hasBudget: false,
    budgetPercent: 0,
    budgetRemaining: 0,
    recentTransactions: [],
    isRecording: false,
    recognitionResult: '',
    transaction: {
      amount: '',
      category: '',
      note: ''
    },
    categories: ['餐饮美食', '交通出行', '购物消费', '居家生活', '休闲娱乐', '人情往来', '医疗健康', '教育培训', '金融贷款', '孝敬父母', '工作商务', '其他支出'],
    selectedCategoryIndex: 0,
    recording: null
  },

  onLoad() {
    this.checkLoginStatus()
    this.setCurrentMonth()
    this.loadData()
  },

  onShow() {
    this.checkLoginStatus()
  },

  // 检查登录状态
  checkLoginStatus() {
    this.setData({
      isLoggedIn: app.globalData.isLoggedIn,
      userInfo: app.globalData.userInfo
    })
  },

  // 设置当前月份
  setCurrentMonth() {
    const now = new Date()
    const year = now.getFullYear()
    const month = now.getMonth() + 1
    this.setData({
      currentMonth: `${year}年${month}月`
    })
  },

  // 加载数据
  loadData() {
    if (app.globalData.isLoggedIn) {
      this.loadRealData()
    } else {
      this.loadMockData()
    }
  },

  // 加载虚拟数据
  loadMockData() {
    this.setData({
      monthlyExpense: MOCK_DATA.monthlyExpense,
      transactionCount: MOCK_DATA.transactionCount,
      hasBudget: MOCK_DATA.hasBudget,
      budgetPercent: MOCK_DATA.budgetPercent,
      budgetRemaining: MOCK_DATA.budgetRemaining,
      recentTransactions: MOCK_DATA.recentTransactions
    })
  },

  // 加载真实数据
  loadRealData() {
    wx.showLoading({ title: '加载中...' })
    
    // 模拟真实数据请求
    setTimeout(() => {
      wx.hideLoading()
      // 这里应该调用真实的API获取数据
      this.setData({
        monthlyExpense: 3280.50,
        transactionCount: 38,
        hasBudget: true,
        budgetPercent: 62,
        budgetRemaining: 1500,
        recentTransactions: [
          { id: 1, item: '午餐', category: '餐饮美食', icon: '🍜', amount: 45.00, date: '2024-03-28' },
          { id: 2, item: '打车', category: '交通出行', icon: '🚗', amount: 28.00, date: '2024-03-28' },
          { id: 3, item: '超市购物', category: '居家生活', icon: '🏠', amount: 128.50, date: '2024-03-27' }
        ]
      })
    }, 1000)
  },

  // 跳转到分析页
  goToAnalysis() {
    wx.navigateTo({
      url: '/pages/analysis/analysis'
    })
  },

  // 跳转到产品页
  goToProduct() {
    wx.navigateTo({
      url: '/pages/product/product'
    })
  },

  // 跳转到指南页
  goToGuide() {
    wx.navigateTo({
      url: '/pages/guide/guide'
    })
  },

  // 跳转到登录页
  goToLogin() {
    wx.navigateTo({
      url: '/pages/login/login'
    })
  },

  // 处理用户点击
  handleUserTap() {
    if (!this.data.isLoggedIn) {
      this.goToLogin()
    }
  },

  // 联系客服
  contactCustomerService() {
    wx.navigateTo({
      url: '/pages/contact/contact'
    })
  },

  // 开始录音
  startRecording() {
    const that = this
    
    // 申请麦克风权限
    wx.authorize({
      scope: 'scope.record',
      success() {
        // 开始录音
        wx.startRecord({
          success: function(res) {
            const tempFilePath = res.tempFilePath
            that.setData({ isRecording: true })
            that.data.recording = tempFilePath
          },
          fail: function(err) {
            console.error('录音失败:', err)
            wx.showToast({
              title: '录音失败，请重试',
              icon: 'none'
            })
          }
        })
      },
      fail() {
        // 未授权，引导用户开启权限
        wx.showModal({
          title: '需要麦克风权限',
          content: '语音记账需要使用麦克风权限，请在设置中开启',
          success: function(res) {
            if (res.confirm) {
              wx.openSetting({})
            }
          }
        })
      }
    })
  },

  // 停止录音
  stopRecording() {
    const that = this
    
    if (this.data.isRecording) {
      wx.stopRecord({
        success: function(res) {
          const tempFilePath = res.tempFilePath
          that.setData({ isRecording: false })
          that.recognizeVoice(tempFilePath)
        },
        fail: function(err) {
          console.error('停止录音失败:', err)
          that.setData({ isRecording: false })
          wx.showToast({
            title: '停止录音失败，请重试',
            icon: 'none'
          })
        }
      })
    }
  },

  // 语音识别
  recognizeVoice(tempFilePath) {
    const that = this
    
    wx.showLoading({
      title: '识别中...',
      mask: true
    })
    
    // 模拟语音识别，实际项目中应使用微信小程序的语音识别API或第三方服务
    setTimeout(() => {
      wx.hideLoading()
      
      // 模拟不同场景的识别结果
      const mockResults = [
        '今天中午吃饭花了45元',
        '打车去公司花了28元',
        '超市购物花了128.5元',
        '看电影花了98元',
        '加油花了300元'
      ]
      
      const randomIndex = Math.floor(Math.random() * mockResults.length)
      const mockResult = mockResults[randomIndex]
      
      that.setData({ recognitionResult: mockResult })
      that.parseRecognitionResult(mockResult)
      
      // 显示记账信息编辑弹窗
      that.showTransactionModal()
    }, 1500)
  },

  // 解析识别结果
  parseRecognitionResult(result) {
    // 提取金额
    const amountRegex = /(\d+(\.\d+)?)元/g
    const amountMatch = result.match(amountRegex)
    let amount = ''
    if (amountMatch) {
      amount = amountMatch[0].replace('元', '')
    }

    // 提取分类
    const categories = this.data.categories
    let category = categories[0]
    let categoryIndex = 0
    
    for (let i = 0; i < categories.length; i++) {
      if (result.includes(categories[i])) {
        category = categories[i]
        categoryIndex = i
        break
      }
    }

    // 提取备注
    let note = result
    if (amountMatch) {
      note = note.replace(amountMatch[0], '')
    }
    note = note.replace(category, '').trim()

    // 更新数据
    this.setData({
      transaction: {
        amount: amount,
        category: category,
        note: note
      },
      selectedCategoryIndex: categoryIndex
    })
  },

  // 显示记账信息编辑弹窗
  showTransactionModal() {
    wx.showModal({
      title: '记账信息',
      content: `金额: ¥${this.data.transaction.amount}\n分类: ${this.data.transaction.category}\n备注: ${this.data.transaction.note}`,
      confirmText: '确认记账',
      cancelText: '重新录音',
      success: (res) => {
        if (res.confirm) {
          this.confirmTransaction()
        } else if (res.cancel) {
          this.cancelTransaction()
        }
      }
    })
  },

  // 确认记账
  confirmTransaction() {
    const transaction = this.data.transaction
    
    if (!transaction.amount) {
      wx.showToast({
        title: '请输入金额',
        icon: 'none'
      })
      return
    }

    // 模拟记账成功
    wx.showLoading({
      title: '记账中...',
      mask: true
    })

    setTimeout(() => {
      wx.hideLoading()
      wx.showToast({
        title: '记账成功',
        icon: 'success'
      })
      
      // 重置数据
      this.setData({
        recognitionResult: '',
        transaction: {
          amount: '',
          category: '',
          note: ''
        },
        selectedCategoryIndex: 0
      })
      
      // 重新加载数据
      this.loadData()
    }, 1000)
  },

  // 重新录音
  cancelTransaction() {
    this.setData({
      recognitionResult: '',
      transaction: {
        amount: '',
        category: '',
        note: ''
      },
      selectedCategoryIndex: 0
    })
  }
})
