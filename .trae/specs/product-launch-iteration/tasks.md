# Tasks

- [x] Task 1: 优化记账指令 Prompt
  - [x] SubTask 1.1: 更新 `src/prompt.txt`，加入“今天”、“昨天”等相对日期的处理逻辑，强制使用 `Current Date` 上下文。
  - [x] SubTask 1.2: 验证 Prompt 在“昨天买西瓜”等场景下的准确性。

- [x] Task 2: 重构 Dashboard 页面 (`src/dashboard.txt`)
  - [x] SubTask 2.1: 界面完全中文化，优化 CSS 样式（清爽自然风格）。
  - [x] SubTask 2.2: 实现 Tab 切换逻辑（今天、本周、本月、本年）。
  - [x] SubTask 2.3: 实现“统计汇总”模块：
    - [x] 显示：总金额、平均金额、交易笔数。
    - [x] 对比：环比（昨、上周、上月、去年）涨跌幅，用箭头和颜色标识。
  - [x] SubTask 2.4: 实现“图表分布”模块（ECharts）：
    - [x] 饼图：按消费类目分布。
    - [x] 趋势图：按时间维度（日/周/月）分布。
  - [x] SubTask 2.5: 实现“明细列表”模块：
    - [x] 包含：时间、类目、事项、金额 (¥)。
    - [x] 支持按时间倒序排列。
  - [x] SubTask 2.6: 实现 CSV 解析逻辑，确保能正确处理日期范围。

- [x] Task 3: 更新用户手册 (`docs/user_manual.md`)
  - [x] SubTask 3.1: 新增“高效调用”章节：
    - [x] 设置“背面轻拍”教程。
    - [x] 设置“操作按钮”教程 (iPhone 15 Pro+)。
    - [x] 设置“桌面小组件”教程。
  - [x] SubTask 3.2: 完善“安装与配置”流程说明。

- [x] Task 4: 更新开发者指南 (`docs/developer_distribution_guide.md`)
  - [x] SubTask 4.1: 更新快捷指令逻辑，增加“提取结果确认”步骤说明。
  - [x] SubTask 4.2: 确保所有路径均为 `ZenLedger/` 开头。

- [x] Task 5: 构建发布
  - [x] SubTask 5.1: 运行 `scripts/build.py` 重新生成 `public/` 资源。
  - [x] SubTask 5.2: 验证生成的 `config.json` 和 `dashboard.txt` 内容正确。

# Task Dependencies
- Task 2 依赖 Task 1 (Prompt 确定后，Dashboard 才能解析准确的数据结构)。
- Task 5 依赖 Task 1, 2。
