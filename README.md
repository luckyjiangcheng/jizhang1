# ZenLedger (禅记账)

**ZenLedger** 是一款基于 iOS 生态的“无感”AI 财务助理。它利用 iOS 快捷指令 (Shortcuts) 和 **SiliconFlow (硅基流动)** 的多模态 AI 能力，为您提供极简的记账体验。

## ✨ 核心功能

*   **📷 一键捕捉 (One-click Capture)**
    *   长按或轻点手机背面触发截图。
    *   AI 自动识别消费金额、商家、分类和项目。
    *   识别完成后自动删除截图，保持相册整洁。
*   **🎙️ 随口记录 (Voice Recording)**
    *   通过 Siri 说“记账”。
    *   自然语言描述消费（例如：“刚才在全家买了面包和牛奶花了25块”）。
    *   AI 自动解析并入账。
*   **📊 智能分析 (Analysis & Insights)**
    *   本地 Web View 仪表盘。
    *   消费分类饼图 (ECharts)。
    *   月度预算曲线与进度监控。
    *   超支预警（当月消费 > 80% 时背景变橙）。

## 🛠️ 准备工作

1.  **iOS 设备**：iPhone 需要安装“快捷指令” (Shortcuts) 应用。
2.  **iCloud Drive**：确保已开启 iCloud Drive，用于存储账单数据 (`ZenLedger.csv`)。
3.  **SiliconFlow API Key**：需要从 [SiliconFlow 官网](https://cloud.siliconflow.cn/) 获取 API Key。

## 🚀 安装与配置

详细的安装步骤请参考 [iOS 快捷指令配置指南](docs/shortcut_guide.md)。

### 简易步骤：
1.  **获取 API Key**。
2.  **配置快捷指令**：按照指南创建三个快捷指令（捕捉、语音、分析）。
3.  **初始化数据**：快捷指令会自动在 iCloud Drive 的 `/Shortcuts/` 目录下创建或追加 `ZenLedger.csv`。

## 📂 项目结构

```
ZenLedger/
├── src/
│   ├── dashboard_template.html  # 仪表盘 HTML 模板 (供快捷指令使用)
│   ├── dashboard_test.html      # 仪表盘测试文件 (含样本数据)
│   ├── prompt.txt               # AI 系统提示词
│   ├── sample_data.csv          # 样本 CSV 数据
│   ├── config.json              # 配置文件 (需手动创建，参考 config.json.example)
│   └── test_siliconflow.py      # Python 测试脚本 (用于验证 API)
├── docs/
│   └── shortcut_guide.md        # 详细安装指南
└── README.md                    # 项目说明
```

## 🔒 隐私说明

*   所有账单数据存储在您个人的 **iCloud Drive** 中。
*   图片和语音数据仅在处理时发送给 SiliconFlow API，不会存储在任何第三方服务器。
*   无需注册账号，完全掌握自己的数据。

---
*Created with Trae IDE*
