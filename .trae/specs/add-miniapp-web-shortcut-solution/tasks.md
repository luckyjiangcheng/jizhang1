# Tasks

- [ ] Task 1: 建立小程序代码目录与边界规则
  - [ ] SubTask 1.1: 在项目根目录新增 `miniapp/`（与 `backend/` 平级）
  - [ ] SubTask 1.2: 约束小程序页面、组件、样式、资源仅存放于 `miniapp/`
  - [ ] SubTask 1.3: 明确 V2 现有目录仅做最小必要接口对接，不承载小程序实现代码

- [ ] Task 2: 明确小程序信息架构与页面流转
  - [ ] SubTask 2.1: 定义未登录态/已登录态页面树与路由
  - [ ] SubTask 2.2: 输出分析页、产品介绍页、快捷指令引导页的模块分区
  - [ ] SubTask 2.3: 统一状态流转规则（游客体验、登录切换、异常回退）

- [ ] Task 3: 建立小程序视觉与交互规范
  - [ ] SubTask 3.1: 制定色系、字体、间距、卡片与图表容器规范
  - [ ] SubTask 3.2: 定义按钮、筛选器、分段控件、列表项交互反馈
  - [ ] SubTask 3.3: 补齐加载态、空态、错误态与弱网态设计

- [ ] Task 4: 实现未登录体验版（虚拟数据分析）
  - [ ] SubTask 4.1: 构建虚拟账单数据集（含时间、分类、趋势、明细）
  - [ ] SubTask 4.2: 实现与 dashboard 类似的分析布局并优化移动端交互
  - [ ] SubTask 4.3: 接入时间切换、分类筛选与动效过渡

- [ ] Task 5: 实现产品图文介绍模块
  - [ ] SubTask 5.1: 编写个人版/家庭版功能说明与对比信息
  - [ ] SubTask 5.2: 增加账号申请说明（联系企微 xxx）
  - [ ] SubTask 5.3: 增加授权码便利性说明（不引导安装）

- [ ] Task 6: 实现登录后真实账单分析
  - [ ] SubTask 6.1: 打通登录态识别与账号维度数据拉取
  - [ ] SubTask 6.2: 聚合当前手机账号下全部账单并渲染分析页
  - [ ] SubTask 6.3: 保持与体验版一致的信息架构与视觉层级

- [ ] Task 7: 实现登录后快捷指令引导说明
  - [ ] SubTask 7.1: 输出快捷指令协作流程说明与触发建议
  - [ ] SubTask 7.2: 增加常见问题入口与说明文案
  - [ ] SubTask 7.3: 提供用户主动触发的快捷指令安装跳转入口

- [ ] Task 8: 联调与验收
  - [ ] SubTask 8.1: 验证游客态与登录态切换行为
  - [ ] SubTask 8.2: 验证分析数据正确性与图表交互一致性
  - [ ] SubTask 8.3: 进行视觉走查与可用性回归
  - [ ] SubTask 8.4: 回归验证 V1 单机版与 V2 Web 端既有流程不受影响
  - [ ] SubTask 8.5: 验证小程序实现代码仅位于 `miniapp/` 目录

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1 and Task 2
- Task 4 depends on Task 2 and Task 3
- Task 5 depends on Task 2 and Task 3
- Task 6 depends on Task 2 and Task 3
- Task 7 depends on Task 6
- Task 8 depends on Task 4, Task 5, Task 6, Task 7
