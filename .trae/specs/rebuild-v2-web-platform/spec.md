# 记账小助手V2 Web前后端重构 Spec

## Why
现有实现在交互稳定性、前后端一致性和可维护性上存在较多历史问题，难以持续迭代。需要按 `v2_guide.md` 重新定义并落地完整的 Web 前后端能力，确保功能完整、可用、可调试。

## What Changes
- 基于 V2 指南重建后端服务边界：认证、家庭、交易、统计、预算、AI、导出、版本管理。
- 重建 Web 前端信息架构与页面流：登录注册、交易首页、统计分析、预算管理、家庭协作、数据导出与版本管理入口。
- 统一接口契约与错误处理规范，消除前后端字段不一致、时间格式不一致、异常返回非 JSON 等问题。
- 建立端到端验证与联调清单，覆盖核心用户路径与异常路径。
- 优化 UI 设计系统与交互反馈（加载、空态、错误提示、成功反馈、移动端适配、深色模式）。
- **BREAKING**：替换现有后端模块实现与部分前端页面结构；旧接口行为若不符合新契约将不再兼容。

## Impact
- Affected specs: 用户认证、家庭共享、交易管理、统计分析、预算管理、AI增强、数据导出、版本管理、PWA体验
- Affected code: `backend/main.py`、`backend/app/api/*`、`backend/app/schemas.py`、`backend/app/models/*`、`backend/alembic/*`、`frontend/index.html`、`frontend/sw.js`、`frontend/manifest.json`

## ADDED Requirements
### Requirement: 统一的V2 API契约
系统 SHALL 提供与 `v2_guide.md` 一致的 REST API 能力，所有错误响应返回结构化 JSON（包含可读 message/detail）。

#### Scenario: API 成功响应一致
- **WHEN** 用户调用任一 V2 核心接口（如登录、添加交易、统计查询）
- **THEN** 返回字段与约定数据类型一致，前端可直接渲染

#### Scenario: API 异常响应一致
- **WHEN** 请求参数不合法、权限不足或服务内部异常
- **THEN** 返回标准 JSON 错误体，前端不会出现 JSON 解析崩溃

### Requirement: 完整的V2 Web功能闭环
系统 SHALL 在 Web 端提供从注册登录到家庭协作、交易录入、统计分析、预算与导出的完整闭环体验。

#### Scenario: 新用户首日可完成核心流程
- **WHEN** 新用户完成注册并首次登录
- **THEN** 可在单次会话中完成创建家庭、添加交易、查看统计与设置预算

### Requirement: 现代化UI与可用性
系统 SHALL 提供统一设计风格、清晰层级、稳定反馈和移动端友好交互。

#### Scenario: 操作反馈明确
- **WHEN** 用户执行保存、删除、切换统计周期等关键操作
- **THEN** 页面展示即时反馈（加载中、成功、失败）且状态可恢复

## MODIFIED Requirements
### Requirement: 后端服务实现方式
系统从“增量修补旧模块”修改为“按V2能力清单重建模块化服务”，并通过统一 DTO 与错误中间件保障行为一致性。

### Requirement: 前端页面结构
系统从“单文件内散乱功能拼接”修改为“按功能域组织的页面与状态流”，并保证导航、表单、图表、预算与家庭模块交互一致。

## REMOVED Requirements
### Requirement: 旧版不一致接口/交互行为
**Reason**: 与 V2 指南不一致，且导致联调成本高与线上不稳定。  
**Migration**: 前端改用新契约；后端保留必要兼容提示并在发布说明中列出变更映射。
