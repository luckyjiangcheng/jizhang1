# 快捷指令端到端接口套件 Spec

## Why
当前快捷指令安装与记账链路缺少一组明确、可复用的标准接口，尤其是“安装前可用性判定”“跨授权码聚合查询”“CSV 输出给 dashboard.txt”能力不完整。需要统一快捷指令交互协议，确保安装、写入、查询、展示四阶段可稳定联动。

## What Changes
- 新增“授权码可用性检查”接口，用于安装前判定授权码是否允许安装。
- 新增“授权码记账写入”接口，要求传入授权码并将数据落到授权码及所属注册账号。
- 新增“授权码聚合数据清单”接口，要求传入授权码并返回该手机号下全部授权码的数据。
- 新增“授权码聚合数据 CSV 接口”，返回 `dashboard.txt` 可直接消费的 CSV 文本。
- 新增快捷指令交互流程规范（安装校验 → 安装激活 → 记账写入 → 清单查询/CSV 拉取）。
- 新增清单输出格式约束：JSON 与 CSV 都需覆盖 `dashboard.txt` 展示字段。
- 统一接口错误语义（授权码不存在、不可安装、授权码与账号不匹配、参数错误）。

## Impact
- Affected specs: 授权码安装激活流程、授权码写入流程、账单聚合查询流程、Dashboard 数据输出规范、快捷指令集成流程
- Affected code: `backend/app/api/v2.py`、`backend/app/schemas.py`、`backend/app/core/access.py`、`backend/app/models/models.py`、`src/dashboard.txt`（字段映射约束）

## ADDED Requirements
### Requirement: 安装前授权码可用性判定接口
系统 SHALL 提供安装前可调用的授权码可用性检查接口，并返回“是否可安装”与原因。

#### Scenario: 授权码可安装
- **WHEN** 客户端传入状态为 `unused` 的授权码
- **THEN** 接口返回可安装标记与授权码基础信息

#### Scenario: 授权码不可安装
- **WHEN** 客户端传入 `used` 或 `disabled` 授权码
- **THEN** 接口返回不可安装并给出明确原因

### Requirement: 快捷指令安装激活流程接口
系统 SHALL 提供安装激活接口，供快捷指令在安装成功后调用，将授权码从 `unused` 切换为 `used`，并禁止重复安装。

#### Scenario: 首次安装激活成功
- **WHEN** 安装校验通过后调用安装激活接口
- **THEN** 授权码状态更新为 `used` 并记录 `used_at`

#### Scenario: 重复安装被拒绝
- **WHEN** 已激活授权码再次调用安装激活接口
- **THEN** 返回不可安装错误并拒绝状态变更

### Requirement: 授权码记账写入接口
系统 SHALL 提供需要传入授权码的记账写入接口，并将交易写入到授权码及其绑定用户名下。

#### Scenario: 写入成功
- **WHEN** 客户端传入合法授权码与合法交易数据
- **THEN** 生成交易记录并保存 `license_code_id` 与 `user_id` 关联

#### Scenario: 写入失败
- **WHEN** 授权码无效、不可用或与账号不匹配
- **THEN** 拒绝写入并返回标准错误

### Requirement: 按手机号聚合全部授权码数据清单接口
系统 SHALL 提供“传入任一授权码，返回该授权码关联手机号下全部授权码的交易清单”接口。

#### Scenario: 聚合返回成功
- **WHEN** 客户端传入有效授权码
- **THEN** 返回该手机号下全部授权码相关交易，按时间倒序

#### Scenario: Dashboard 样式字段可直接消费
- **WHEN** 客户端获取聚合清单响应
- **THEN** 响应字段满足 `dashboard.txt` 所需数据维度（日期、时间、金额、分类、项目/商户、备注、授权码等）

### Requirement: Dashboard CSV 输出接口
系统 SHALL 提供“按授权码获取同手机号全授权码聚合数据 CSV”的接口，CSV 头与字段顺序需可直接用于 `dashboard.txt`。

#### Scenario: CSV 返回成功
- **WHEN** 客户端传入有效授权码请求 CSV
- **THEN** 返回 `text/csv`，包含标准表头与按时间倒序的交易数据

#### Scenario: CSV 字段兼容 dashboard
- **WHEN** 快捷指令将 CSV 传给 `dashboard.txt`
- **THEN** 可直接渲染指标、趋势图、分类图、最近交易列表，无需二次字段转换

### Requirement: 快捷指令交互协议
系统 SHALL 提供面向快捷指令的最小交互协议，明确每一步调用顺序、输入输出和失败分支。

#### Scenario: 完整主链路
- **WHEN** 用户首次安装并开始记账
- **THEN** 按“可用性检查 → 安装激活 → 记账写入 → 聚合清单(JSON/CSV)”顺序完成全链路

#### Scenario: 失败分支可恢复
- **WHEN** 任一步骤返回失败
- **THEN** 响应包含可读错误码与提示文案，快捷指令可据此中断或重试

## MODIFIED Requirements
### Requirement: 授权码查询范围
现有授权码查询能力需扩展为“同手机号跨授权码聚合 + CSV 输出”，不再局限于单授权码独立查询。

## REMOVED Requirements
### Requirement: 无
**Reason**: 本次为能力新增与范围扩展，不删除既有能力。  
**Migration**: 旧接口保持兼容，新增接口供快捷指令链路优先使用。
