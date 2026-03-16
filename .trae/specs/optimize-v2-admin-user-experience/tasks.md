# Tasks

- [x] Task 1: 切换用户登录为手机号
  - [x] SubTask 1.0: 移除用户端首页“仅支持 V2 授权模式”提示板块
  - [x] SubTask 1.1: 更新后端登录请求模型与查询逻辑为手机号
  - [x] SubTask 1.2: 更新前端登录表单与登录请求字段
  - [x] SubTask 1.3: 增加手机号登录回归测试并验证旧邮箱入口下线

- [ ] Task 2: 重构root用户管理页面与建户流程
  - [ ] SubTask 2.1: 将用户管理拆为查询区与新增弹窗
  - [ ] SubTask 2.2: 新建用户仅保留手机号与账号类型字段
  - [ ] SubTask 2.3: 在创建反馈中明确默认密码规则并自动发码
  - [ ] SubTask 2.4: 用户列表新增手机号列与账号类型展示

- [ ] Task 3: 重构root授权码管理与账单管理展示
  - [ ] SubTask 3.1: 授权码管理改为查询区与新增区
  - [ ] SubTask 3.2: 增加授权码启用与删除操作入口
  - [ ] SubTask 3.3: 授权码列表展示手机号与授权码
  - [ ] SubTask 3.4: 账单管理列表增加手机号与授权码列

- [ ] Task 4: 调整家庭管理规则与用户信息只读
  - [ ] SubTask 4.1: 去除家庭成员管理员角色判断并允许全员管理
  - [ ] SubTask 4.2: 增加“至少保留1名成员”后端保护
  - [ ] SubTask 4.3: 用户信息页改为只读展示并移除编辑动作

- [ ] Task 5: 全局UI优化（管理端+用户端）
  - [ ] SubTask 5.0: 产出统一视觉规范（配色、字体、间距、圆角、阴影、状态色）
  - [ ] SubTask 5.1: 统一字体层级与字号，降低整体视觉体量
  - [ ] SubTask 5.2: 优化表单、按钮、表格、弹窗间距与圆角
  - [ ] SubTask 5.2.1: 收窄桌面端左侧导航栏宽度并校验文案不截断
  - [ ] SubTask 5.3: 优化页面模块分布与对齐规则，提升信息层级清晰度
  - [ ] SubTask 5.4: 优化移动端与桌面端响应式细节，保持美观一致
  - [ ] SubTask 5.5: 补齐交互细节状态（hover/active/loading/disabled）并统一反馈样式

- [ ] Task 6: 联调与验收
  - [ ] SubTask 6.1: 验证手机号登录、建户发码、授权码操作主流程
  - [ ] SubTask 6.2: 验证家庭成员全员管理与最少1人保护
  - [ ] SubTask 6.3: 验证用户信息只读与root账单展示字段完整
  - [ ] SubTask 6.4: 执行 UI 回归检查（配色/字体/布局/细节状态）并更新文档说明

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 2
- Task 4 depends on Task 1 and Task 2
- Task 5 depends on Task 2 and Task 3
- Task 6 depends on Task 1, Task 3, Task 4 and Task 5
