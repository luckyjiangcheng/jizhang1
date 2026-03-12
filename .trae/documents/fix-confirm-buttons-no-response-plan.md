# Plan：修复 confirm 页面“确认记账/取消无反应”

## Summary
- 目标：修复 iOS 快捷指令 WebView 中，点击“确认记账”或“取消”后无明显响应的问题。
- 成功标准：
  - 点击“确认记账”后可稳定返回 CSV（或关闭页面）；
  - 点击“取消”后可稳定返回空值（或关闭页面）；
  - 不再出现“按钮点击了但页面无变化”的体验。

## Current State Analysis
- 按钮事件绑定存在，非“未绑定”问题：
  - 取消按钮绑定：[public/confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/public/confirm.txt#L249-L251)
  - 提交绑定：[public/confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/public/confirm.txt#L253-L261)
- 根因风险 1（高）：`src` 与 `public` 存在逻辑漂移。
  - `src` 的 `endWith` 有回退关闭逻辑：[src/confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/src/confirm.txt#L182-L191)
  - `public` 的 `endWith` 仅写文本，不关闭页面：[public/confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/public/confirm.txt#L181-L187)
  - 线上使用 `public/confirm.txt`，会导致部分 WebView 场景下看起来“无反应”。
- 根因风险 2（中）：校验阻断时只显示内联文案，用户可能误判为“无反应”。
  - 金额/类目未满足时直接 return：[public/confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/public/confirm.txt#L256-L258)
- 根因风险 3（中）：占位符替换异常会让脚本异常，导致交互失效。
  - 占位符注入点：[public/confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/public/confirm.txt#L169-L169)

## Proposed Changes

### 1) 统一发布模板与源码逻辑（高优先）
- **文件**：`src/confirm.txt`、`public/confirm.txt`
- **What**：
  - 以 `src/confirm.txt` 为单一真源；
  - 重新构建并覆盖 `public/confirm.txt`，确保 `endWith` 完整回退路径生效。
- **Why**：
  - 当前线上行为取决于 `public`，必须消除版本漂移。
- **How**：
  - 变更后执行 `python3 scripts/build.py`；
  - 验证 `public/confirm.txt` 的 `endWith` 与 `src` 一致。

### 2) 增强按钮交互可感知性（中优先）
- **文件**：`src/confirm.txt`
- **What**：
  - 在提交与取消路径上保持“completion 优先，关闭回退”；
  - 保持校验提示为页面内提示，不引入弹窗；
  - 必要时增加按钮防抖/提交态，避免重复点击误判。
- **Why**：
  - 让用户在所有 WebView 分支都有明确结果，不误判“无反应”。
- **How**：
  - 保持 `endWith(value)` 统一出口；
  - 校验失败时高亮错误区域并保留已有内联提示。

### 3) 修正文档中的排障指引（中优先）
- **文件**：`docs/developer_distribution_guide.md`
- **What**：
  - 增加“若按钮无反应，优先检查是否拉取到最新 `confirm.txt`”；
  - 强调不要在快捷指令里残留调试动作（显示文本/旧变量写入）。
- **Why**：
  - 该问题在设备端常由旧模板缓存或旧流程引起。
- **How**：
  - 在主程序配置章节增加“检查清单”。

## Assumptions & Decisions
- 决策 1：不新增系统弹窗，保持“确认页内提示 + 自动回传/关闭”。
- 决策 2：`src/confirm.txt` 作为模板唯一来源，`public/confirm.txt` 仅由构建产出。
- 决策 3：优先修复线上可见问题（发布文件逻辑漂移），再做交互细化。

## Verification Steps
1. **模板一致性**：确认 `src/public` 两份 `endWith` 一致。
2. **确认路径**：点击“确认记账”后，快捷指令拿到 CSV 且继续执行。
3. **取消路径**：点击“取消”后，快捷指令拿到空值且不写入。
4. **校验路径**：金额或类目缺失时显示内联错误，不出现“假死”。
5. **端到端**：语音与截图两分支都能完成“确认页 -> 回传 -> 写入CSV”。
