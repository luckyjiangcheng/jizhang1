// pages/analysis/analysis.js
const app = getApp()

// 虚拟数据
const MOCK_DATA = {
  summary: {
    totalExpense: 3580.50,
    totalIncome: 12000.00,
    transactionCount: 42,
    averageAmount: 285.72
  },
  categoryStats: [
    { category: '餐饮美食', icon: '🍜', amount: 1280.00, count: 15, percentage: 35.8, color: '#f97316' },
    { category: '交通出行', icon: '🚗', amount: 560.00, count: 8, percentage: 15.6, color: '#3b82f6' },
    { category: '购物消费', icon: '🛒', amount: 890.50, count: 10, percentage: 24.9, color: '#ec4899' },
    { category: '居家生活', icon: '🏠', amount: 450.00, count: 5, percentage: 12.6, color: '#8b5cf6' },
    { category: '休闲娱乐', icon: '🎮', amount: 400.00, count: 4, percentage: 11.2, color: '#10b981' }
  ],
  trendData: {
    dates: ['1日', '5日', '10日', '15日', '20日', '25日'],
    expenses: [320, 450, 280, 560, 380, 420],
    incomes: [0, 0, 0, 5000, 0, 0]
  },
  recentTransactions: [
    { id: 1, item: '午餐', category: '餐饮美食', icon: '🍜', amount: 45.00, date: '2024-03-28', type: 'expense' },
    { id: 2, item: '打车', category: '交通出行', icon: '🚗', amount: 28.00, date: '2024-03-28', type: 'expense' },
    { id: 3, item: '超市购物', category: '居家生活', icon: '🏠', amount: 128.50, date: '2024-03-27', type: 'expense' },
    { id: 4, item: '工资', category: '工资收入', icon: '💰', amount: 8000.00, date: '2024-03-25', type: 'income' },
    { id: 5, item: '电影票', category: '休闲娱乐', icon: '🎮', amount: 98.00, date: '2024-03-26', type: 'expense' }
  ]
}

Page({
  data: {
    isLoggedIn: false,
    currentPeriod: 'month',
    periodText: '2024年3月',
    summary: {},
    categoryStats: [],
    trendChart: null,
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
    this.loadData()
  },

  onShow() {
    this.checkLoginStatus()
  },

  // 检查登录状态
  checkLoginStatus() {
    this.setData({
      isLoggedIn: app.globalData.isLoggedIn
    })
  },

  // 切换时间周期
  switchPeriod(e) {
    const period = e.currentTarget.dataset.period
    this.setData({ currentPeriod: period })
    this.loadData()
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
    const now = new Date()
    const periodText = this.getPeriodText(now)
    
    this.setData({
      summary: MOCK_DATA.summary,
      categoryStats: MOCK_DATA.categoryStats,
      periodText: periodText,
      recentTransactions: MOCK_DATA.recentTransactions
    })
    
    this.initTrendChart(MOCK_DATA.trendData)
  },

  // 加载真实数据
  loadRealData() {
    wx.showLoading({ title: '加载中...' })
    
    wx.request({
      url: `${app.globalData.apiBaseUrl}/stats/summary`,
      method: 'GET',
      header: app.getHeaders(),
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({
            summary: {
              totalExpense: res.data.total_expense,
              totalIncome: res.data.total_income || 0,
              transactionCount: res.data.transaction_count,
              averageAmount: res.data.average_amount
            }
          })
        }
      },
      complete: () => {
        wx.hideLoading()
      }
    })
    
    this.loadCategoryStats()
    this.loadTrendData()
  },

  // 加载分类统计
  loadCategoryStats() {
    wx.request({
      url: `${app.globalData.apiBaseUrl}/stats/category`,
      method: 'GET',
      header: app.getHeaders(),
      success: (res) => {
        if (res.statusCode === 200) {
          const categoryStats = res.data.map(item => ({
            category: item.category,
            icon: this.getCategoryIcon(item.category),
            amount: item.amount,
            count: item.count,
            percentage: item.percentage || 0,
            color: this.getCategoryColor(item.category)
          }))
          this.setData({ categoryStats })
        }
      }
    })
  },

  // 加载趋势数据
  loadTrendData() {
    wx.request({
      url: `${app.globalData.apiBaseUrl}/stats/trend`,
      method: 'GET',
      header: app.getHeaders(),
      success: (res) => {
        if (res.statusCode === 200) {
          this.initTrendChart(res.data)
        }
      }
    })
  },

  // 初始化趋势图
  initTrendChart(data) {
    this.setData({
      trendChart: {
        onInit: (canvas, width, height) => {
          const chart = echarts.init(canvas, null, {
            width: width,
            height: height
          })
          canvas.setChart(chart)
          
          const option = {
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data: ['支出', '收入']
            },
            grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
            },
            xAxis: {
              type: 'category',
              data: data.dates
            },
            yAxis: {
              type: 'value'
            },
            series: [
              {
                name: '支出',
                type: 'line',
                data: data.expenses,
                smooth: true,
                itemStyle: { color: '#ef4444' }
              },
              {
                name: '收入',
                type: 'line',
                data: data.incomes,
                smooth: true,
                itemStyle: { color: '#10b981' }
              }
            ]
          }
          
          chart.setOption(option)
          return chart
        }
      }
    })
  },

  // 获取分类图标
  getCategoryIcon(category) {
    const icons = {
      '餐饮美食': '🍜',
      '交通出行': '🚗',
      '购物消费': '🛒',
      '居家生活': '🏠',
      '休闲娱乐': '🎮',
      '人情往来': '🎁',
      '医疗健康': '💊',
      '教育培训': '📚',
      '金融贷款': '💳',
      '孝敬父母': '❤️',
      '工作商务': '💼',
      '其他支出': '📝'
    }
    return icons[category] || '📊'
  },

  // 获取分类颜色
  getCategoryColor(category) {
    const colors = {
      '餐饮美食': '#f97316',
      '交通出行': '#3b82f6',
      '购物消费': '#ec4899',
      '居家生活': '#8b5cf6',
      '休闲娱乐': '#10b981',
      '人情往来': '#f59e0b',
      '医疗健康': '#ef4444',
      '教育培训': '#06b6d4',
      '金融贷款': '#6366f1',
      '孝敬父母': '#f43f5e',
      '工作商务': '#84cc16',
      '其他支出': '#64748b'
    }
    return colors[category] || '#6366f1'
  },

  // 获取周期文本
  getPeriodText(date) {
    const period = this.data.currentPeriod
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    
    if (period === 'month') {
      return `${year}年${month}月`
    } else if (period === 'quarter') {
      const quarter = Math.ceil(month / 3)
      return `${year}年第${quarter}季度`
    } else {
      return `${year}年`
    }
  },

  // 跳转登录
  goToLogin() {
    wx.navigateTo({
      url: '/pages/login/login'
    })
  },

  // 查看全部交易
  viewAllTransactions() {
    wx.showToast({
      title: '查看全部交易功能开发中',
      icon: 'none'
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
