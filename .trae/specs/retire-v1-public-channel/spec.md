# 下线V1公共通道并统一V2 Spec

## Why
你已明确不再需要 V1（`public` 版本）并只保留 V2。继续保留双通道会增加维护成本、权限绕过风险和用户认知混乱，需要统一收敛到 V2 授权体系。

## What Changes
- 下线 V1 公共页面与 V1 入口（含前端按钮、菜单、跳转入口）。
- 关闭或隔离 V1 接口对外访问，仅保留 V2 授权通道。
- 将登录后默认路径统一为 V2 控制台（root/用户按角色展示）。
- 删除“V1 保持不变”的兼容要求，改为“仅 V2 生效”。
- 更新文档与提示文案，明确“仅支持 V2 授权模式”。
- **BREAKING**：V1 原有访问路径将不可用；未升级到 V2 授权流程的调用将被拒绝。

## Impact
- Affected specs: 认证与鉴权、角色后台、快捷指令安装校验、账单查询与写入、前端导航
- Affected code: `frontend/index.html`、`backend/main.py`、`backend/app/api/*`、`public/*`、`docs/*`

## ADDED Requirements
### Requirement: 单一V2入口
系统 SHALL 仅提供 V2 登录与业务入口，不再暴露 V1 入口。

#### Scenario: 登录后路由
- **WHEN** 任意用户登录成功
- **THEN** 进入 V2 功能域（root 管理域或用户域），不存在 V1 入口跳转

### Requirement: 单一V2鉴权
系统 SHALL 对记账安装、写入、查询等核心动作统一执行 V2 授权码校验。

#### Scenario: 未携带V2授权凭证
- **WHEN** 请求未携带有效 V2 授权码
- **THEN** 返回拒绝响应，且不落库

## MODIFIED Requirements
### Requirement: 兼容策略
系统从“V1/V2 并行隔离”修改为“仅 V2 生效”，不再提供 V1 功能入口与兼容保障。

### Requirement: 用户引导
所有用户指引、安装文案、后台提示统一为 V2 授权流程（发码→安装校验→调用）。

## REMOVED Requirements
### Requirement: V1 功能入口与回归保障
**Reason**: 业务策略已明确只保留 V2，继续保留 V1 会增加绕过与维护负担。  
**Migration**: 将 V1 用户迁移到 V2 授权流程；关闭 V1 入口并提供一次性迁移提示页。
