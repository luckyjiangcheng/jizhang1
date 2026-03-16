# Tasks

- [x] Task 1: 盘点并冻结V2范围与接口清单
  - [x] SubTask 1.1: 对照 `docs/v2_guide.md` 提取功能矩阵与接口清单
  - [x] SubTask 1.2: 定义统一请求/响应与错误码约定
  - [x] SubTask 1.3: 输出前后端联调字段映射（日期、时间、金额、family_id）

- [x] Task 2: 重建后端基础架构与数据模型
  - [x] SubTask 2.1: 重建应用入口、路由注册、配置与中间件
  - [x] SubTask 2.2: 重建核心模型与迁移（用户、家庭、交易、预算）
  - [x] SubTask 2.3: 建立统一异常处理与健康检查接口

- [x] Task 3: 实现V2核心后端能力
  - [x] SubTask 3.1: 实现认证与权限（注册、登录、当前用户）
  - [x] SubTask 3.2: 实现家庭共享（创建、成员、邀请、上限5人）
  - [x] SubTask 3.3: 实现交易管理（增删改查、软删除、筛选）
  - [x] SubTask 3.4: 实现统计分析（汇总、分类、趋势、周期）
  - [x] SubTask 3.5: 实现预算管理与超支提醒
  - [x] SubTask 3.6: 实现导出与版本管理（Excel/PDF、迁移、状态）

- [x] Task 4: 重建Web前端页面与交互体验
  - [x] SubTask 4.1: 重构登录注册与全局会话状态
  - [x] SubTask 4.2: 重构交易录入、列表、删除与反馈
  - [x] SubTask 4.3: 重构统计页面周期切换与图表渲染
  - [x] SubTask 4.4: 重构预算管理与家庭协作页面
  - [x] SubTask 4.5: 完善UI视觉系统（响应式、暗黑模式、空态/错误态）

- [x] Task 5: 完整联调与质量验证
  - [x] SubTask 5.1: 执行后端接口测试与关键用例回归
  - [x] SubTask 5.2: 执行前后端端到端联调（核心流程 + 异常流程）
  - [x] SubTask 5.3: 修复阻断问题并完成最终验收记录

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 2
- Task 4 depends on Task 1 and Task 3
- Task 5 depends on Task 3 and Task 4
