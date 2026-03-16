# Tasks

- [x] Task 1: 清理前端 V1 入口与跳转
  - [x] SubTask 1.1: 删除登录页与导航中的 V1 入口按钮/链接
  - [x] SubTask 1.2: 删除前端中与 V1 相关的路由分支与状态判断
  - [x] SubTask 1.3: 登录后统一落到 V2 页面流并校验角色分流

- [x] Task 2: 收敛后端到 V2 通道
  - [x] SubTask 2.1: 关闭或限制 V1 对外接口入口（保留内部可控开关）
  - [x] SubTask 2.2: 统一核心接口授权逻辑到 V2 校验链路
  - [x] SubTask 2.3: 对 V1 路径返回明确迁移提示或标准拒绝错误

- [x] Task 3: 迁移与文档更新
  - [x] SubTask 3.1: 更新产品文案为“仅支持 V2 授权模式”
  - [x] SubTask 3.2: 增加 V1 用户迁移提示（授权码激活引导）
  - [x] SubTask 3.3: 更新部署与验收说明，移除 V1 回归项

- [x] Task 4: 联调与验收
  - [x] SubTask 4.1: 验证 root/用户登录后均无 V1 入口
  - [x] SubTask 4.2: 验证未带授权码调用被拒绝且不落库
  - [x] SubTask 4.3: 验证 V2 安装、调用、查询主链路全部通过

- [x] Task 5: 修复本轮验收失败项
  - [x] SubTask 5.1: 用户端账单读写切换到 V2 接口并接入授权码请求头
  - [x] SubTask 5.2: 页面提示文案统一为“仅 V2”并补充迁移激活引导入口
  - [x] SubTask 5.3: 补充发码到安装再到调用查询的端到端自动化验证

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1 and Task 2
- Task 4 depends on Task 2 and Task 3
- Task 5 depends on Task 4
