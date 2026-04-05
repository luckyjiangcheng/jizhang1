// pages/voice/voice.js
const app = getApp()

Page({
  data: {
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
    // 初始化页面
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

  // 绑定金额输入
  bindAmountInput(e) {
    this.setData({
      'transaction.amount': e.detail.value
    })
  },

  // 绑定分类选择
  bindCategoryChange(e) {
    const index = e.detail.value
    this.setData({
      selectedCategoryIndex: index,
      'transaction.category': this.data.categories[index]
    })
  },

  // 绑定备注输入
  bindNoteInput(e) {
    this.setData({
      'transaction.note': e.detail.value
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
      
      // 重置页面
      setTimeout(() => {
        this.setData({
          recognitionResult: '',
          transaction: {
            amount: '',
            category: '',
            note: ''
          },
          selectedCategoryIndex: 0
        })
      }, 1500)
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