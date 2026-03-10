# iOS 快捷指令配置指南 (SiliconFlow 版)

本指南将帮助你创建三个 iOS 快捷指令，用于通过截图或语音记录账单，并查看分析仪表板。本项目使用 **SiliconFlow (硅基流动)** 的 API 服务。

## 准备工作

1.  **获取 API Key**:
    -   访问 [SiliconFlow 官网](https://cloud.siliconflow.cn/) 注册并获取 API Key (`sk-xxxxxxxx`).
2.  **iCloud Drive 文件路径**:
    -   确保你的 iCloud Drive 中存在 `/Shortcuts/ZenLedger.csv` 文件。
    -   确保你的 iCloud Drive 中存在 `/Shortcuts/dashboard_template.html` 文件。

---

## 1. 一键截图记账 (One-click Capture)

此快捷指令用于处理当前屏幕截图，提取信息并记录。

**步骤:**

1.  **截取屏幕**: 添加“截取屏幕”动作。
2.  **Base64 编码**:
    -   添加“Base64 编码”动作。
    -   输入: 上一步的“屏幕快照”。
    -   **关键**: 确保“换行”选项设置为“无” (None) 或每 64/76 字符（OpenAI 格式通常兼容，但建议无换行）。
3.  **文本**:
    -   添加“文本”动作，粘贴 `src/prompt.txt` 的内容作为系统提示词。
4.  **调用 SiliconFlow API**:
    -   添加“获取 URL 内容”动作。
    -   URL: `https://api.siliconflow.cn/v1/chat/completions`
    -   方法: `POST`
    -   头部 (Headers):
        -   `Authorization`: `Bearer sk-xxxxxxxx` (你的 API Key)
        -   `Content-Type`: `application/json`
    -   请求体 (Request Body): `JSON`
    -   添加字段:
        -   `model`: `Qwen/Qwen2-VL-72B-Instruct` (支持图像的模型)
        -   `messages` (数组):
            -   Item 1 (字典):
                -   `role`: `system`
                -   `content`: [选择步骤 3 的“文本”]
            -   Item 2 (字典):
                -   `role`: `user`
                -   `content` (数组):
                    -   Item 1 (字典):
                        -   `type`: `text`
                        -   `text`: `Extract transaction details.`
                    -   Item 2 (字典):
                        -   `type`: `image_url`
                        -   `image_url` (字典):
                            -   `url`: `data:image/jpeg;base64,[选择步骤 2 的 Base64 编码结果]`
        -   `temperature`: `0.1` (数字)
5.  **解析响应**:
    -   添加“获取字典值”动作，获取 `choices.1.message.content`。
    -   这将是 API 返回的 CSV 行。
6.  **追加到 CSV**:
    -   添加“追加到文件”动作。
    -   输入: [上一步解析出的文本]。
    -   文件: `/Shortcuts/ZenLedger.csv`。
    -   确保开启“追加新行”。
7.  **清理**:
    -   添加“删除照片”动作（可选）。

---

## 2. 语音记账 (Voice Recording)

此快捷指令用于通过语音口述消费信息。

**步骤:**

1.  **听写文本**:
    -   添加“听写文本”动作。
2.  **文本**:
    -   添加“文本”动作，粘贴 `src/prompt.txt` 的内容。
3.  **调用 SiliconFlow API**:
    -   添加“获取 URL 内容”动作。
    -   URL: `https://api.siliconflow.cn/v1/chat/completions`
    -   方法: `POST`
    -   头部: 同上。
    -   请求体: `JSON`
    -   添加字段:
        -   `model`: `deepseek-ai/DeepSeek-V3` (或 `Qwen/Qwen2.5-7B-Instruct` 等文本模型)
        -   `messages` (数组):
            -   Item 1 (字典):
                -   `role`: `system`
                -   `content`: [选择步骤 2 的“文本”]
            - Item 2 (字典):
                - `role`: `user`
                - `content`: [选择步骤 1 的“听写文本”] (建议在此文本后拼接当前日期，例如：`[听写文本] (Today is [Current Date])`)
        -   `temperature`: `0.1`
4.  **解析响应**:
    -   获取 `choices.1.message.content`。
5.  **追加到 CSV**:
    -   同上。

---

## 3. 分析仪表板 (Analysis Dashboard)

此部分逻辑未变，参考原文档或直接使用 HTML 模板。
