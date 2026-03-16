# Tasks

- [x] Task 1: 基础设计系统重构
  - [x] SubTask 1.1: 建立 CSS Design Token（颜色、排版、间距、圆角、阴影），支持 Dark Mode
  - [x] SubTask 1.2: 提取并标准化通用组件（Button, Input, Card, Modal, Toast, Skeleton）
  - [x] SubTask 1.3: 重构全局布局（Mobile Bottom Tab Bar + Desktop Sidebar + PWA Shell）

- [x] Task 2: 首页/仪表盘 (Dashboard) 视图优化
  - [x] SubTask 2.1: 实现“账户总览”卡片（收支/结余），支持快捷切换月份
  - [x] SubTask 2.2: 实现“最近交易”摘要列表与“预算告警”卡片
  - [x] SubTask 2.3: 优化“记账 FAB”悬浮按钮交互（动画与位置）

- [x] Task 3: 交易列表 (Transactions) 视图优化
  - [x] SubTask 3.1: 实现按日期分组展示交易列表（Header显示日期+日收支）
  - [x] SubTask 3.2: 优化单笔交易项视觉（分类图标、备注预览、金额正负色）
  - [x] SubTask 3.3: 增加筛选器（按月份/分类/家庭）与加载骨架屏

- [x] Task 4: 统计分析 (Stats) 视图优化
  - [x] SubTask 4.1: 优化 ECharts 图表样式与交互（Tooltip、图例、配色）
  - [x] SubTask 4.2: 增加统计卡片（最高单笔、平均支出、分类Top3）与时间范围选择器
  - [x] SubTask 4.3: 适配 Dark Mode 下的图表展示

- [x] Task 5: 预算与家庭管理 (Budget & Family) 视图优化
  - [x] SubTask 5.1: 重构预算列表为进度条卡片样式，增加可视化反馈
  - [x] SubTask 5.2: 优化家庭成员列表与邀请流程（头像、角色标签、操作反馈）
  - [x] SubTask 5.3: 增加设置页（个人资料、家庭管理入口、预算入口、API配置、退出登录）

- [x] Task 6: 认证与引导流程优化
  - [x] SubTask 6.1: 美化登录/注册页面（全屏背景、卡片居中、表单验证提示）
  - [x] SubTask 6.2: 增加 PWA 安装引导与离线提示

- [x] Task 7: 整体集成与 polish
  - [x] SubTask 7.1: 统一所有页面的转场动画与 Loading 状态
  - [x] SubTask 7.2: 全面测试响应式适配（Mobile/Tablet/Desktop）与 Dark Mode
  - [x] SubTask 7.3: （可选）同步更新 `src/confirm.txt` 与 `src/dashboard.txt` 视觉风格

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1
- Task 4 depends on Task 1
- Task 5 depends on Task 1
- Task 6 depends on Task 1
- Task 7 depends on Task 2, Task 3, Task 4, Task 5, Task 6
