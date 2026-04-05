Component({
  data: {
    currentTab: 0
  },
  methods: {
    switchTab(e) {
      const path = e.currentTarget.dataset.path;
      const index = e.currentTarget.dataset.index;
      
      wx.switchTab({
        url: path,
        success: () => {
          this.setData({
            currentTab: index
          });
        }
      });
    },
    startVoice() {
      wx.authorize({
        scope: 'scope.record',
        success: () => {
          wx.showLoading({
            title: '正在录音...',
            mask: true
          });
          
          wx.startRecord({
            success: (res) => {
              const tempFilePath = res.tempFilePath;
              this.recognizeVoice(tempFilePath);
            },
            fail: (err) => {
              wx.hideLoading();
              wx.showToast({
                title: '录音失败',
                icon: 'none'
              });
              console.error('录音失败:', err);
            }
          });
        },
        fail: () => {
          wx.showModal({
            title: '权限提示',
            content: '需要麦克风权限才能使用语音记账功能',
            success: (res) => {
              if (res.confirm) {
                wx.openSetting({
                  success: (settingRes) => {
                    if (settingRes.authSetting['scope.record']) {
                      this.startVoice();
                    }
                  }
                });
              }
            }
          });
        }
      });
    },
    stopVoice() {
      wx.stopRecord();
    },
    recognizeVoice(tempFilePath) {
      wx.hideLoading();
      
      setTimeout(() => {
        const mockResult = '今天早上买早餐花了15元';
        this.parseRecognitionResult(mockResult);
      }, 1000);
    },
    parseRecognitionResult(result) {
      const amountRegex = /\d+(\.\d+)?/;
      const amountMatch = result.match(amountRegex);
      const amount = amountMatch ? amountMatch[0] : '0';
      
      let category = '其他';
      if (result.includes('早餐') || result.includes('吃')) {
        category = '餐饮';
      } else if (result.includes('交通') || result.includes('打车')) {
        category = '交通';
      } else if (result.includes('购物') || result.includes('买')) {
        category = '购物';
      }
      
      wx.showModal({
        title: '记账确认',
        content: `金额: ${amount}元\n分类: ${category}`,
        success: (res) => {
          if (res.confirm) {
            wx.showToast({
              title: '记账成功',
              icon: 'success'
            });
          }
        }
      });
    }
  }
});