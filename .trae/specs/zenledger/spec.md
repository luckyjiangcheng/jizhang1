# ZenLedger (禅记账) Spec

## Why
用户需要一款基于iOS生态的“无感”AI财务助理，解决传统记账App操作繁琐、界面复杂的问题。通过利用iOS快捷指令（Shortcuts）和Gemini 1.5 Pro的多模态能力，实现极简的记账体验。

## What Changes
- **核心交互**：
  - 实现“一键捕捉”：通过长按或轻点背面触发截图，识别消费金额、分类和项目，并自动记录。
  - 实现“随口记录”：通过Siri语音交互，自然语言输入消费信息，AI自动解析并入账。
- **极简安装**：
  - 通过iCloud链接分发快捷指令，无需App Store下载。
  - 首次运行引导配置API Key。
  - 数据存储在用户iCloud Drive的CSV文件中，保障隐私。
- **智能分析**：
  - 通过快捷指令加载本地HTML/JS（Web View）展示账单。
  - 包含消费饼图（ECharts）、月度预算曲线。
  - 包含预算预警功能（超过80%变橙色）。
- **技术架构**：
  - 输入层：iOS Shortcuts（截图/语音）。
  - 处理层：Gemini 1.5 Pro API（多模态解析）。
  - 持久层：iCloud Drive CSV文件。
  - 展示层：HTML + ECharts。

## Impact
- **Affected specs**: 新增ZenLedger功能模块。
- **Affected code**: 
  - 新增 `dashboard.html` (用于展示层)。
  - 新增 `prompt.txt` (用于Gemini系统提示词)。
  - 新增 `README.md` (包含安装和配置指南)。

## ADDED Requirements
### Requirement: One-click Capture (一键捕捉)
系统应支持通过快捷指令处理屏幕截图。
#### Scenario: Screenshot Analysis
- **WHEN** 用户触发快捷指令并传入截图
- **THEN** 系统调用Gemini API识别图片内容（金额、商家、分类）
- **THEN** 系统将识别结果追加到CSV文件
- **THEN** 系统发送通知并删除截图

### Requirement: Voice Recording (随口记录)
系统应支持通过Siri进行语音记账。
#### Scenario: Voice Input
- **WHEN** 用户通过Siri说“记账”并描述消费
- **THEN** 系统调用Gemini API解析文本（金额、分类、项目）
- **THEN** 系统将解析结果追加到CSV文件
- **THEN** Siri语音反馈确认

### Requirement: Analysis Dashboard (智能分析)
系统应提供基于Web View的账单分析界面。
#### Scenario: View Dashboard
- **WHEN** 用户点击“查看账单”
- **THEN** 快捷指令读取CSV文件并注入到HTML模板
- **THEN** Web View展示消费饼图和月度预算曲线
- **THEN** 若当月消费超过预算80%，背景变更为橙色警告

### Requirement: Data Privacy (隐私安全)
所有数据必须存储在用户的iCloud Drive中，不上传至第三方服务器（除Gemini API处理外）。

## MODIFIED Requirements
无

## REMOVED Requirements
无
