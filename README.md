# ZenLedger (禅记账)

**ZenLedger** 是一款基于 iOS 生态的“无感”AI 财务助理。它利用 iOS 快捷指令 (Shortcuts) 和 **SiliconFlow (硅基流动)** 的多模态 AI 能力，为您提供极简的记账体验。

## ✨ 核心功能

*   **🎙️ 语音记账**: 对着 Siri 说“记账”，自然语言描述，AI 自动解析。
*   **📷 截图记账**: 支付完成后随手截图，AI 自动识别金额、商户和分类。
*   **📊 智能分析**: 本地可视化仪表盘，展示月度预算、消费分类饼图和进度曲线。

## 🚀 用户使用指南

如果您是最终用户，请直接阅读 **[用户安装手册](docs/user_manual.md)**。
您只需要点击两个 iCloud 链接，即可在 30 秒内完成安装，无需编写代码。

---

## 💻 开发者指南

如果您想部署自己的 ZenLedger 分发服务，或者贡献代码，请阅读以下内容。

### 📂 项目结构

```
ZenLedger/
├── public/              # [自动生成] 静态资源发布目录 (推送到 GitHub Pages)
├── src/                 # 源代码
│   ├── config.json      # 您的私有配置 (含 API Key)
│   ├── dashboard.html   # 仪表盘模板
│   └── prompt.txt       # AI 系统提示词
├── scripts/             # 工具脚本
│   ├── build.py         # 构建 public 目录
│   └── test_api.py      # 本地测试 API 连通性
├── docs/                # 文档
│   ├── developer_distribution_guide.md # 开发者分发指南 (制作母版指令)
│   └── user_manual.md                  # 用户手册
└── README.md            # 项目说明书
```

### 🛠️ 开发流程

1.  **配置环境**:
    复制 `src/config.json.example` 为 `src/config.json`，并填入您的 SiliconFlow API Key。

2.  **本地测试**:
    使用测试脚本验证 API 是否通畅：
    ```bash
    python3 scripts/test_api.py -t "我买西瓜花了20元"
    ```

3.  **构建发布**:
    运行构建脚本，生成 `public` 目录：
    ```bash
    python3 scripts/build.py
    ```
    该脚本会执行以下操作：
    - 读取 `src/config.json` 中的配置（包括 API Key）。
    - 读取 `src/prompt.txt` 中的系统提示词。
    - 读取 `src/dashboard.txt` 模板。
    - 将以上内容打包生成到 `public/` 目录中。
    
    > **注意**：生成的 `public/config.json` 将包含您的 API Key。如果您将 `public` 目录托管到公开网络（如 GitHub Pages），请确保您了解相关风险。推荐使用限制额度的 API Key。
    然后将 `public` 目录推送到您的静态资源服务器（如 GitHub Pages）。

4.  **制作快捷指令**:
    参考 **[开发者分发指南](docs/developer_distribution_guide.md)**，在您的 iPhone 上制作 `Installer` 和 `ZenLedger` 快捷指令，并生成分享链接。

## 🔒 隐私说明

*   所有账单数据存储在用户个人的 **iCloud Drive** 中。
*   图片和语音数据仅在处理时发送给 AI 服务商，不存储在任何第三方服务器。
*   无需注册账号，完全掌握自己的数据。

---
*Created with Trae IDE*
