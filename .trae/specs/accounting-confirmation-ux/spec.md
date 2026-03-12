# 记账确认体验优化规格说明书 (Accounting Confirmation UX Spec)

## 为什么 (Why)
目前的记账确认机制仅使用了 iOS 快捷指令原生的“要求输入”功能，界面简陋，且修改字段（如金额、类目）不直观。用户希望获得一个类似 App 原生体验的精美对话框，能够清晰展示账单详情，支持便捷修改，并在成功后给予丝滑的反馈。

## 变更内容 (What Changes)
- **快捷指令逻辑重构**: 不再直接使用“要求输入”文本框，而是改为调用一个专门设计的 Web 视图（HTML）来进行确认。
- **新增确认页模板**: `src/confirm.txt` (HTML)。
- **Prompt 输出格式变更**: 为了方便 Web 视图解析，AI 的输出格式从 CSV 改为 JSON。
- **文档更新**: 更新 `docs/developer_distribution_guide.md` 以反映新的 JSON + Web View 确认流程。
- **移除不必要的弹框**: 确保确认页仅作为输入/确认界面，不包含额外的弹框提示。

## 影响范围 (Impact)
- **Affected specs**: `product-launch-iteration` (部分逻辑被优化替代).
- **Affected code**: `src/prompt.txt` (输出格式变更为 JSON), `src/confirm.txt` (新增), `docs/developer_distribution_guide.md`.

## 新增需求 (ADDED Requirements)

### 需求：Web View 确认对话框
系统应通过快捷指令的“显示网页视图”动作，展示一个美观的 HTML 页面。
- **界面元素**:
  - 标题: "✨ 记账确认"
  - 表单区域:
    - 日期 (Date): 支持日期选择器。
    - 时间 (Time): 支持时间选择器。
    - 金额 (Amount): 大字体显示，支持数字键盘输入。
    - 类目 (Category): 下拉或标签选择（预设中文类目）。
    - 事项 (Item): 文本输入。
    - 商户 (Merchant): 文本输入。
  - 按钮:
    - "确认记账" (主按钮，蓝色/高亮)。
    - "取消" (次要按钮，灰色)。
- **交互**:
  - 页面加载时自动填充 AI 识别的数据。
  - 点击“确认记账”后，通过 JavaScript 将修改后的数据返回给快捷指令（通过剪贴板或 URL Scheme 机制，或者直接在 HTML 中生成最终 CSV 字符串供用户复制，考虑到快捷指令 Web View 交互限制，最稳妥方式是：**HTML 生成最终 CSV 字符串 -> 用户点击确认 -> JS 复制到剪贴板 -> 快捷指令读取剪贴板**）。
  - *优化方案*: iOS 快捷指令的“显示网页视图”可以直接获取网页的输出（如果网页结束时调用 `completion()`）。我们将采用此方案。
  - **重要**: 确保没有额外的弹框（如 `alert` 或不必要的确认框），流程应顺畅。

### 需求：记账成功 Toast
快捷指令在成功追加文件后，应显示一个精美的通知（Toast 风格），内容包含："✨ 记账成功！已存入账本"。

## 修改需求 (MODIFIED Requirements)

### 需求：Prompt 输出格式
**修改**: 为了更精准地填充 Web 表单，`src/prompt.txt` 的输出格式由 CSV 改为 **JSON**。
**JSON 结构**:
```json
{
  "date": "YYYY-MM-DD",
  "time": "HH:mm",
  "amount": 12.50,
  "category": "餐饮美食",
  "item": "西瓜",
  "merchant": "水果店"
}
```

### 需求：开发者指南流程
**修改**: 开发者指南中的快捷指令构建步骤需要大幅调整，增加“获取 `confirm.txt` -> 替换 JSON 占位符 -> 显示网页视图 -> 获取网页输出 -> 解析并写入 CSV”的流程。

## 移除需求 (REMOVED Requirements)
### 需求：额外弹框
**Reason**: 用户明确表示不需要额外的弹框提示，流程应尽可能简洁。
