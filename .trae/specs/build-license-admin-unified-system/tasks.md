# Tasks

- [x] Task 1: 设计并落地授权码数据模型
  - [x] SubTask 1.1: 新增用户角色与账号类型字段（root/user, personal/family）
  - [x] SubTask 1.2: 新增授权码表与用户关系字段（状态、创建时间、使用时间）
  - [x] SubTask 1.3: 实现短长度加密字符串授权码生成逻辑与唯一性校验

- [x] Task 2: 实现管理后台核心接口
  - [x] SubTask 2.1: 实现 root 用户登录与权限守卫
  - [x] SubTask 2.2: 实现用户管理（新增用户、查看用户）
  - [x] SubTask 2.3: 实现授权码管理（按类型发码、复制内容、删除/禁用）
  - [x] SubTask 2.4: 实现管理端账单管理（按用户+授权码筛选与删除）

- [x] Task 3: 实现快捷指令授权流程
  - [x] SubTask 3.1: 实现安装校验接口（仅未使用授权码通过）
  - [x] SubTask 3.2: 安装成功后标记授权码为已使用
  - [x] SubTask 3.3: 实现记账调用授权校验（授权码+账号绑定）
  - [x] SubTask 3.4: 实现账单查询授权校验（授权码+账号绑定）

- [x] Task 4: 改造统一前端后台界面
  - [x] SubTask 4.1: 增加角色路由与功能隔离（root 与用户）
  - [x] SubTask 4.2: 增加 root 用户管理与授权码管理页面
  - [x] SubTask 4.3: 增加 root 账单管理页（按授权码分类）
  - [x] SubTask 4.4: 增加用户侧授权码展示（个人1个、家庭最多5个）
  - [x] SubTask 4.5: 保持用户账单展示样式与第一版 dashboard 风格一致
  - [x] SubTask 4.6: 增加 V1 入口与新方案入口隔离，不改动 V1 原功能

- [x] Task 5: 联调与验收
  - [x] SubTask 5.1: 校验“付费后发码-安装校验-首次绑定-后续调用”完整链路
  - [x] SubTask 5.2: 校验 root 与普通用户权限隔离
  - [x] SubTask 5.3: 校验恶意重放（已使用/禁用授权码）被拒绝
  - [x] SubTask 5.4: 执行 V1 回归验证，确认所有 V1 功能不变

- [x] Task 6: 修复初始密码与手机号规则不一致问题
  - [x] SubTask 6.1: 新增手机号字段并在管理员建户时必填
  - [x] SubTask 6.2: 将初始密码生成规则改为“手机号后6位”
  - [x] SubTask 6.3: 更新前端文案与接口校验，避免继续按用户名截取
  - [x] SubTask 6.4: 补充回归用例，覆盖手机号异常与密码初始化场景

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1 and Task 2
- Task 4 depends on Task 2 and Task 3
- Task 5 depends on Task 2, Task 3 and Task 4
- Task 6 depends on Task 2 and Task 4
