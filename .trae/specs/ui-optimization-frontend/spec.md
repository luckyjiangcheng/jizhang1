# 后端系统 UI 交互优化 Spec

## Why
当前的后端系统 UI（即 `frontend/index.html` 单页应用）虽然功能基本完备，但在视觉美观度、交互流畅性、以及用户体验细节上仍有欠缺。为了达到“可交付给用户使用”的商业化标准，需要进行全面的 UI/UX 升级，打造美观大方、操作便捷的现代化界面。

## What Changes
- **设计系统升级**：
  - 统一色彩规范（Violet/Indigo 主色调），优化深色模式适配。
  - 引入更现代的排版系统与圆角/阴影规范。
  - 标准化组件库（按钮、输入框、卡片、Toast、Modal、Skeleton）。
- **布局重构**：
  - **移动端**：引入底部导航栏（Bottom Tab Bar），符合原生应用习惯。
  - **桌面端**：引入侧边导航栏（Sidebar），充分利用宽屏空间。
  - 响应式适配：确保在不同尺寸屏幕下均有最佳展示效果。
- **核心页面优化**：
  - **仪表盘（Dashboard）**：新增“账户概览”卡片、快捷操作入口、最近交易摘要。
  - **交易列表**：优化列表项视觉（图标、分类标签、金额颜色），增加按日期分组展示。
  - **统计分析**：优化图表配色与交互，增加时间范围切换器。
  - **设置/个人中心**：重构为分组列表样式，增加家庭成员管理与预算设置的独立入口。
- **交互体验增强**：
  - 全局加载骨架屏（Skeleton Screen）。
  - 页面切换转场动画。
  - 操作反馈（Toast 提示、按钮 Loading 状态）。
  - 表单验证与即时反馈。

## Impact
- Affected specs: 无直接关联 Spec，属于前端独立优化。
- Affected code: 
  - `frontend/index.html`: 全面重构 HTML/CSS/JS。
  - `frontend/sw.js`: 配合 PWA 体验优化。
  - （可选）`src/confirm.txt`, `src/dashboard.txt`: 保持视觉风格一致性。

## ADDED Requirements
### Requirement: 现代化导航布局
系统 SHALL 提供响应式导航结构：移动端底部 Tab 栏，桌面端左侧 Sidebar。

#### Scenario: 移动端访问
- **WHEN** 屏幕宽度 < 768px
- **THEN** 显示底部固定导航栏（交易、统计、记账FAB、预算、我的）
- **AND** 隐藏顶部传统 Header

#### Scenario: 桌面端访问
- **WHEN** 屏幕宽度 >= 768px
- **THEN** 显示左侧固定导航栏
- **AND** 内容区域居中或流式布局

### Requirement: 仪表盘（Home）视图
系统 SHALL 新增“首页”视图，聚合关键信息。

#### Scenario: 进入首页
- **THEN** 展示：本月收支概览卡片、快捷记账入口、最近 5 笔交易、预算告警（如有）。

### Requirement: 交易列表分组
交易列表 SHALL 按“日期”进行分组展示，提升阅读效率。

#### Scenario: 查看交易列表
- **THEN** 交易按天聚合，头部显示“日期 + 当日收支小计”。
- **AND** 列表项展示分类图标、备注、金额。

### Requirement: 深色模式（Dark Mode）
系统 SHALL 完美适配系统深色主题，并支持手动切换（可选）。

#### Scenario: 系统开启深色模式
- **WHEN** `prefers-color-scheme: dark`
- **THEN** 界面自动切换为深色背景、浅色文字，降低亮度但保持对比度。

## MODIFIED Requirements
### Requirement: 视觉风格统一
现有 CSS 变量 SHALL 被重构为更系统的 Design Token（颜色、字号、间距），并应用到所有组件。

### Requirement: 加载体验
所有数据加载过程 SHALL 展示骨架屏（Skeleton），而非简单的“加载中”文字或空白。

## REMOVED Requirements
### Requirement: 顶部 Tabs 导航
**Reason**: 在移动端单手操作不便，且不符合现代 App 习惯。
**Migration**: 迁移至底部 Tab Bar。
