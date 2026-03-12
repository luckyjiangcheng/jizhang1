# Plan：修复“保存数据不是确认页提交结果”问题

## Summary
- 目标：确保写入 `ZenLedger.csv` 的内容**只**来自确认页用户最终提交的数据，而不是 AI 原始 JSON 或其他中间变量。
- 成功标准：
  - 确认页默认填充 AI 识别数据；
  - 用户不修改直接确认可正常入账；
  - 用户修改后入账内容与修改一致；
  - 全流程无二次弹窗干扰（仅保留必要的确认页本身）。

## Current State Analysis
- 当前链路主要在 [developer_distribution_guide.md](file:///Users/zyb/Documents/trae/jizhang1/docs/developer_distribution_guide.md#L79-L149) 定义。
- 已发现两个关键风险：
  - **分支链路不一致**：语音分支直接写 `FinalCSV`，截图分支先做“转文本”再写入，行为不统一，易出现写入来源漂移。
  - **确认页实现不稳定**：`confirm.txt` 样式块存在结构问题（变量定义位置异常），可能触发网页视图异常渲染；同时存在 `alert`，与“不要再次弹窗”的目标冲突。
- 确认页回传逻辑在 [confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/src/confirm.txt#L320-L355)，目前虽调用 `window.completion(csvLine)`，但快捷指令端变量接线仍可能误用旧变量。

## Proposed Changes

### 1) 统一确认页输出契约（`src/confirm.txt`）
- **改什么**：
  - 修复 CSS 结构（恢复合法 `:root` 变量定义与单一容器布局）；
  - 移除 `alert` 交互，改为页面内轻量提示或直接阻止提交；
  - 保留并强化 `window.completion(csvLine)` 作为唯一返回出口；
  - 取消动作仅返回空字符串（或明确 CANCEL 标记）并立即结束。
- **为什么**：
  - 让确认页输出稳定、可预期，避免“看见的是表单，落库却是别的变量”。
- **怎么做**：
  - 明确“提交=输出 CSV 一行；取消=输出空值”，不做额外弹窗。

### 2) 统一快捷指令写入变量链路（`docs/developer_distribution_guide.md`）
- **改什么**：
  - 语音与截图两条分支统一为同一链路：
    - `AIResult(JSON) -> ConfirmHTML -> 显示网页视图 -> FinalCSVRaw -> 从输入中获取文本 -> FinalCSVText -> 追加到CSV`
  - 明确“追加到文件”只能接 `FinalCSVText`，禁止接 `AIResult/请求输入/更新后的文本`。
  - 删除文档中的“显示文本/调试展示”动作，避免误连线。
  - 去掉“取消后再次提示”的步骤（满足“不要再次弹窗”）。
- **为什么**：
  - 用户当前问题本质是“写入源变量错接”或“对象文本化不一致”。
- **怎么做**：
  - 在文档中用固定变量名+步骤顺序，确保执行者按图搭建不会跑偏。

### 3) 构建与发布一致性（`scripts/build.py` 与 `public/confirm.txt`）
- **改什么**：
  - 确认构建后 `public/confirm.txt` 与 `src/confirm.txt` 同步。
- **为什么**：
  - 线上访问的确认页来自 `public/confirm.txt`，若不同步会出现“本地修了线上没生效”。
- **怎么做**：
  - 构建后校验 `public/confirm.txt` 包含关键逻辑：`window.completion(csvLine)` 与中文类目集合。

## Assumptions & Decisions
- 决策 1：保留确认页（用户可改），移除所有额外确认弹窗（包括 `alert` 和取消提示通知）。
- 决策 2：CSV 仍为最终落库格式，AI 输出 JSON 仅用于填充确认页。
- 决策 3：语音与截图分支必须共用同一“最终写入变量”规范，避免一条链路修复另一条仍异常。

## Verification Steps
1. **确认页回传验证**：
   - 提交前修改金额/类目/事项，提交后检查写入行与页面值一致。
2. **不修改直提验证**：
   - AI 默认值不改，直接确认，写入行应正确且不是 JSON。
3. **取消路径验证**：
   - 点击取消不写入任何内容，不出现二次提示弹窗。
4. **分支一致性验证**：
   - 分别测试语音记账与截图记账，两者都写入同格式 CSV。
5. **回归验证（查看账单）**：
   - 仪表盘可正常读取新增记录，无 JSON 残留行。
