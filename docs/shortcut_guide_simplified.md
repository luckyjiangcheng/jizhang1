# iOS 快捷指令配置指南 (极简版)

本指南帮助您快速配置 ZenLedger。我们通过“配置分离”的方式，让您只需在手机上进行极少的操作。

## 第一步：一键部署文件

1.  在您的电脑上，找到本项目生成的 `dist/ZenLedger` 文件夹。
2.  将整个 `ZenLedger` 文件夹复制到您的 **iCloud Drive** 的 `Shortcuts` 文件夹下。
    *   最终路径应为：`iCloud Drive > Shortcuts > ZenLedger`
    *   该文件夹内应包含：`config.json`, `dashboard.html`, `ZenLedger.csv`。

> **注意**：`config.json` 中已包含了您的 API Key 和系统提示词，请勿泄露给他人。

---

## 第二步：创建快捷指令

现在，您只需要在 iPhone 上创建非常简单的快捷指令，因为所有复杂的配置（Prompt、Key）都已自动读取。

### 1. 语音记账 (Voice Recording)

1.  **获取文件**: 获取 `/Shortcuts/ZenLedger/config.json`。
2.  **获取字典**: 从上一步的“文件”获取字典。
3.  **听写文本**: 添加“听写文本”动作。
4.  **调用 API**:
    *   添加“获取 URL 内容”动作。
    *   **URL**: 从字典中获取值 `api_base`，并追加 `/chat/completions`。
    *   **方法**: `POST`
    *   **头部**:
        *   `Authorization`: `Bearer` + [从字典获取值 `api_key`]
        *   `Content-Type`: `application/json`
    *   **请求体 (JSON)**:
        *   `model`: [从字典获取值 `text_model`]
        *   `messages` (数组):
            *   Item 1: `role`=`system`, `content`=[从字典获取值 `system_prompt`]
            *   Item 2: `role`=`user`, `content`=[听写文本] + ` (Today is [当前日期])`
        *   `temperature`: `0.1` (数字)
5.  **解析与保存**:
    *   获取字典值 `choices.1.message.content`。
    *   追加到文件 `/Shortcuts/ZenLedger/ZenLedger.csv` (开启追加新行)。
    *   (可选) 朗读文本 "已记账"。

### 2. 一键截图记账 (One-click Capture)

逻辑与语音记账类似，区别在于：
1.  输入源为“截取屏幕”。
2.  需要对图片进行 Base64 编码。
3.  请求体中的 `model` 使用 `vision_model`。
4.  请求体 `messages` 的 `user` 部分需要按照 OpenAI Vision 格式构造（参考旧版指南或自行构建）。

### 3. 查看账单 (Dashboard)

1.  **获取文件**: 获取 `/Shortcuts/ZenLedger/ZenLedger.csv`。
2.  **获取文件**: 获取 `/Shortcuts/ZenLedger/dashboard.html`。
3.  **替换文本**: 将模板中的 `/* CSV_DATA_PLACEHOLDER */` 替换为 CSV 内容。
4.  **显示网页视图**。

---
**优势**:
如果未来需要修改 API Key 或 提示词，您只需在电脑上修改 `config.json`，所有快捷指令会自动生效，无需逐个编辑！
