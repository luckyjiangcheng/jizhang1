# Plan：修复 confirm 页提交后弹出中间页与写入格式错误

## Summary
- 目标：修复“点击确认记账后出现图1中间页、完成后写入图2异常格式”的问题，并实现“点击确认后直接完成，不再出现中间页”。
- 成功标准：
  - 点击“确认记账”后快捷指令直接继续，不再出现 CSV 文本中间页；
  - 写入 `ZenLedger.csv` 的每条记录严格为一行 CSV：`Date,Time,Amount,Category,Item,Merchant`；
  - 点击“取消”后不写入任何数据，也不出现无意义中间页。

## Current State Analysis
- `src/confirm.txt` 与 `public/confirm.txt` 当前存在明显漂移：
  - `src` 已包含占位符防误替换与回退关闭逻辑（`placeholderToken`、`window.close()`），见 [confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/src/confirm.txt#L169-L191)。
  - `public` 仍是旧逻辑：`endWith` 在无 `completion` 时仅 `document.body.innerText = value`，会呈现图1样式，见 [confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/public/confirm.txt#L181-L187)。
  - `public` 仍使用旧判断 `if (rawData === "JSON_DATA_PLACEHOLDER")`，见 [confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/public/confirm.txt#L209-L215)。
- 图2“整页文本被写入 CSV”与以下场景一致：
  - WebView 返回了页面文本（标题/标签/按钮文案），而不是 `completion` 的 CSV；
  - 或快捷指令在“显示网页视图”后拿错变量（拿了“网页文本/更新后文本”而非回传值）。
- 文档已强调 `FinalCSVRaw -> FinalCSVText -> 追加`，但缺少“确认页版本/缓存”与“中间页出现即回退异常”的明确判定提示，见 [developer_distribution_guide.md](file:///Users/zyb/Documents/trae/jizhang1/docs/developer_distribution_guide.md#L109-L125)。

## Proposed Changes

### 1) 统一 confirm 模板逻辑并消除中间页
- **文件**：`src/confirm.txt`、`public/confirm.txt`
- **What**：
  - 以 `src/confirm.txt` 为唯一真源；
  - 确保 `endWith` 统一为：
    - 优先 `window.completion(value)`；
    - fallback 不展示可见 CSV 中间页，直接关闭（或最小化不可见回退）；
  - 保持占位符判断使用非字面量比较，避免替换误伤。
- **Why**：
  - 图1本质是 fallback 把 CSV 写进页面正文导致；
  - 若继续使用旧 `public` 文件，线上仍会复现问题。
- **How**：
  - 修正 `src` 后立即构建生成 `public`，并核对关键片段一致性。

### 2) 固化快捷指令返回链路，防止写入整页文本
- **文件**：`docs/developer_distribution_guide.md`
- **What**：
  - 在确认页步骤增加“异常判定”：
    - 若出现图1（页面显示 CSV 文本）说明未走 completion，应先更新模板再测；
  - 明确“追加到文件”只能接 `FinalCSVText`，禁止接“网页页面文本/更新后文本/请求输入”。
- **Why**：
  - 图2属于“变量接线错误或返回类型错误”造成的典型症状。
- **How**：
  - 文档补充“错误现象 -> 对应修复动作”检查表。

### 3) 强化发布一致性与设备侧更新流程
- **文件**：`scripts/build.py`（使用方式）、`public/confirm.txt`（产物）
- **What**：
  - 执行构建并核验 `src/public` 关键函数一致；
  - 补充“必须重新运行 Installer 拉取最新 confirm.txt”的操作说明。
- **Why**：
  - 用户设备常驻旧模板是该问题高频根因。
- **How**：
  - 通过关键字符串检查（`window.completion`、`placeholderToken`、`endWith` fallback）确认产物正确。

## Assumptions & Decisions
- 决策 1：保留确认页（允许用户修改），但提交后不再展示中间 CSV 页面。
- 决策 2：CSV 写入唯一来源为确认页提交返回值，不允许任何“页面全文文本”进入写入步骤。
- 决策 3：优先修复模板一致性，再校正文档与设备更新流程，避免“本地修复、线上无效”。

## Verification Steps
1. **模板一致性验证**：`src/public` 的 `endWith` 与占位符判断一致。
2. **确认提交验证**：点击“确认记账”后直接返回主流程，不出现图1。
3. **取消验证**：点击取消后不写入 CSV，且不出现中间页。
4. **写入格式验证**：CSV 新增记录严格单行六列，无“标题/标签/按钮文案”污染。
5. **端到端验证**：语音与截图两分支均通过 `FinalCSVRaw -> FinalCSVText -> 追加` 完成写入。
