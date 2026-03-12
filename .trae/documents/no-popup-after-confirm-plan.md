# Plan：点击“确认记账”后无任何弹窗

## Summary
- 目标：用户在确认页点击“确认记账”后，流程直接保存并返回，不出现任何额外弹窗或提示框。
- 成功标准：
  - 点击“确认记账”后立即结束网页视图并回传 CSV；
  - 不出现 `alert`、额外通知、调试文本展示；
  - 写入内容仍为用户在确认页最终值（非原始 JSON）。

## Current State Analysis
- 确认页当前提交逻辑位于 [confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/src/confirm.txt#L253-L261)，已使用 `endWith(toCsvLine())` 回传。
- 回传实现位于 [confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/src/confirm.txt#L181-L187)，优先 `window.completion(value)`，fallback 为 `document.body.innerText = value`。
- 当前无 JS 弹窗 `alert`，仅有页内错误提示文本 [confirm.txt](file:///Users/zyb/Documents/trae/jizhang1/src/confirm.txt#L255-L258)。
- 快捷指令文档链路已统一为 `FinalCSVRaw -> Get Text -> FinalCSVText -> Append`，见 [developer_distribution_guide.md](file:///Users/zyb/Documents/trae/jizhang1/docs/developer_distribution_guide.md#L98-L142)。
- 用户截图显示仍存在“显示文本”等动作，说明设备端快捷指令可能仍有历史调试步骤，导致“确认后还有弹窗/中断感”。

## Proposed Changes

### 1) 强化确认页“无弹窗完成”行为（`src/confirm.txt`）
- **What**：
  - 保持“提交即 completion 回传”单一路径；
  - 移除/弱化所有可能被误解为弹窗的交互（包括阻断式提示）；
  - 取消时仅返回空值，不再显示任何提示。
- **Why**：
  - 将“确认即完成”做成确定行为，减少 iOS WebView 差异带来的体验波动。
- **How**：
  - 提交逻辑只做：校验 -> 生成 CSV -> `window.completion(csvLine)`；
  - 不使用任何 `alert/confirm/prompt` 与额外过渡页面。

### 2) 固化快捷指令接线规范（`docs/developer_distribution_guide.md`）
- **What**：
  - 在“显示网页视图”后明确只保留：
    - `从输入中获取文本(FinalCSVRaw)`；
    - `如果 FinalCSVText 有值 -> 追加到文件`；
  - 明确删除“显示文本/显示通知/额外要求输入”等调试或提示动作。
- **Why**：
  - 当前“弹窗感”高概率来自设备端旧动作，而非网页模板本身。
- **How**：
  - 在文档增加“必须删除的旧动作清单”与“最终最小动作序列”。

### 3) 发布一致性与缓存规避（`public/confirm.txt`）
- **What**：
  - 构建并确认 `public/confirm.txt` 与 `src/confirm.txt` 一致；
  - 指导用户更新安装器资源并强制刷新缓存。
- **Why**：
  - 若线上仍是旧版模板，用户会继续看到旧交互。
- **How**：
  - 构建后核验关键标记（`window.completion`、无弹窗调用）；
  - 通过版本参数或重新运行 Installer 拉取最新 `confirm.txt`。

## Assumptions & Decisions
- 决策 1：页面内轻量错误文案允许保留，但不出现系统弹窗。
- 决策 2：确认成功后不再追加“成功提示弹窗/通知”步骤。
- 决策 3：若设备端存在历史动作（如“显示文本”），以文档给出的最小链路为准进行清理。

## Verification Steps
1. **确认提交无弹窗**：点击“确认记账”，不出现任何额外提示框，直接返回快捷指令。
2. **保存值正确**：修改金额/类目后提交，CSV 中写入为修改后值。
3. **默认值直提**：不修改直接确认，CSV 写入为确认页默认填充值。
4. **取消不写入**：点击取消后不写入新行，也不出现额外提示。
5. **链路回归**：语音与截图两条分支均按 `FinalCSVText` 写入，且不存在“显示文本”动作。
