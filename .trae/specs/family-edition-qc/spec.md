# 记账小助手家庭版功能完善与缺陷修复 Spec

## Why
当前已新增“家庭版”能力，需要在对外发布前核对功能闭环、补齐缺失能力并修复关键缺陷，确保可用性与一致的产品承诺。

## What Changes
- 家庭共享：限制家庭成员最多 5 人；邀请/成员列表/权限校验完善
- 云端存储：确认交易、预算、家庭等数据均持久化；修复统计与预算计算口径缺陷
- 多设备同步：提供可增量同步的数据接口；补齐删除同步能力（软删除与 tombstone）
- 高级统计：提供更详细的消费分析与环比/同比；提供基础趋势预测（轻量算法）
- AI 增强：提升文本/图片识别稳健性与分类一致性；明确语音识别输入形态
- 数据导出：新增 Excel、PDF 导出（在既有 CSV 导出基础上扩展）
- 预算管理：支持家庭预算与个人预算；预算状态计算覆盖家庭维度；权限规则明确
- 消费提醒：提供“超预算提醒”能力（后端输出提醒事件/状态，前端轮询展示）

## Impact
- Affected specs: server-backend, verify-v2-features, family-optional
- Affected code:
  - 后端 API：backend/app/api/families.py, transactions.py, stats.py, budgets.py, version.py, ai.py
  - 数据模型/迁移：backend/app/models/models.py, backend/alembic/versions/*
  - 前端/客户端集成点（如有）：frontend/*（仅接口对接与展示，不包含新端开发）

## ADDED Requirements
### Requirement: 家庭共享（最多 5 人）
系统 SHALL 限制同一家庭的成员数量最多为 5（包含管理员）。

#### Scenario: 管理员邀请第 6 位成员
- **WHEN** 家庭成员数已为 5，管理员继续邀请新成员
- **THEN** 返回 400，并给出明确错误信息（例如“家庭成员已满(5人)”）

### Requirement: 多设备同步（增量 + 删除同步）
系统 SHALL 提供交易数据的增量同步能力，且删除操作可被其他设备同步感知。

#### Scenario: 设备 A 删除交易，设备 B 同步
- **WHEN** 设备 A 删除一笔交易
- **AND** 设备 B 以“自上次同步时间”请求增量同步
- **THEN** 设备 B 能获得该交易的删除 tombstone（或等价标记），从而在本地删除

### Requirement: Excel 导出
系统 SHALL 支持导出交易数据为 Excel（.xlsx），字段至少包含 Date、Time、Amount、Category、Item、Merchant、Notes，并支持按家庭与日期范围过滤。

### Requirement: PDF 导出
系统 SHALL 支持导出交易数据为 PDF，内容至少包含导出范围、汇总信息与交易明细列表，并支持按家庭与日期范围过滤。

### Requirement: 预算提醒（超预算）
系统 SHALL 在预算超支时提供可被客户端消费的“提醒状态/事件”输出。

#### Scenario: 当月预算超支
- **WHEN** 已花费金额超过预算金额
- **THEN** 预算状态接口返回 is_over_budget=true
- **AND** 提醒接口/状态输出包含“超支金额、预算周期、预算对象（个人/家庭）”

### Requirement: 高级统计（环比/同比 + 预测）
系统 SHALL 提供消费统计的环比/同比对比，并提供基础趋势预测（例如下一周/下月消费预测）。

#### Scenario: 获取本月支出与较上月波动
- **WHEN** 用户请求本月统计
- **THEN** 返回本月支出金额与“较上月”百分比（口径一致且可解释）

### Requirement: AI 增强（稳健解析与分类一致）
系统 SHALL 对 AI 返回内容做稳健 JSON 解析（去除 Markdown 包裹、容错字段缺失），并将分类归一到产品分类集合。

#### Scenario: AI 返回 ```json 包裹内容
- **WHEN** AI 返回 Markdown code fence 包裹的 JSON
- **THEN** 系统仍能正确解析并返回结构化交易信息

## MODIFIED Requirements
### Requirement: 预算（家庭预算可共享）
当 Budget.family_id 不为空时，该预算 SHALL 被视为“家庭预算”，对家庭成员可读；仅家庭管理员可创建/修改/删除（默认）。

### Requirement: 统计口径（仅支出口径一致）
统计与预算“已花费金额” SHALL 仅统计支出（排除收入类别或负数金额），并在个人/家庭维度保持一致。

### Requirement: 删除交易（软删除）
删除交易 SHALL 变更为软删除（例如 deleted_at 置值），以支持跨设备删除同步；默认列表接口不返回已删除记录。

## REMOVED Requirements
无

