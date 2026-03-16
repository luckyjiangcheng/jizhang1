# 记账小助手V2 - 家庭可选功能产品需求文档

## Overview
- **Summary**: 改进记账小助手V2的交易管理功能，支持个人独立使用和家庭共享两种模式，家庭从必选项变为可选项，为后续的个人/家庭套餐定价做准备。
- **Purpose**: 解决当前强制要求家庭的问题，让用户可以选择个人独立使用或家庭共享模式，同时为商业定价模型做准备。
- **Target Users**: 个人用户和家庭用户

## Goals
- 支持个人独立使用模式，无需创建家庭即可记账
- 保持家庭共享模式的现有功能
- 为个人和家庭套餐的不同定价做准备
- 确保数据结构和API的向后兼容性

## Non-Goals (Out of Scope)
- 实现具体的定价和支付系统
- 改变现有的家庭管理功能
- 影响已有的家庭共享功能
- 修改用户认证系统

## Background & Context
- 当前系统强制要求用户必须加入家庭才能记账
- 数据库模型中 `transactions` 表的 `family_id` 字段为必填
- 前端和API都依赖家庭ID进行操作
- 产品需要支持个人和家庭两种使用场景的不同定价

## Functional Requirements
- **FR-1**: 支持个人独立记账，无需家庭
- **FR-2**: 保持家庭共享记账功能
- **FR-3**: 交易API支持无家庭ID的情况
- **FR-4**: 数据模型支持 `family_id` 为可选
- **FR-5**: 前端支持个人和家庭两种模式的切换

## Non-Functional Requirements
- **NFR-1**: 向后兼容，不影响现有家庭用户
- **NFR-2**: 性能保持稳定，无明显性能下降
- **NFR-3**: 数据安全，确保个人交易的隐私性
- **NFR-4**: 可扩展性，便于后续添加定价系统

## Constraints
- **Technical**: 需要修改数据库模型和API实现
- **Business**: 保持与现有功能的兼容性
- **Dependencies**: 现有数据库结构和API设计

## Assumptions
- 个人用户的交易只对自己可见
- 家庭用户的交易对家庭成员可见
- 个人用户可以随时创建或加入家庭
- 家庭用户可以查看所有家庭成员的交易

## Acceptance Criteria

### AC-1: 个人用户可以直接记账
- **Given**: 用户未创建或加入任何家庭
- **When**: 用户尝试添加交易
- **Then**: 交易成功保存，`family_id` 为 NULL 或空
- **Verification**: `programmatic`

### AC-2: 家庭用户可以记账
- **Given**: 用户已加入家庭
- **When**: 用户尝试添加交易
- **Then**: 交易成功保存，`family_id` 为用户的家庭ID
- **Verification**: `programmatic`

### AC-3: 个人用户可以查看自己的交易
- **Given**: 用户未加入家庭
- **When**: 用户查询交易列表
- **Then**: 只返回该用户的交易
- **Verification**: `programmatic`

### AC-4: 家庭用户可以查看家庭交易
- **Given**: 用户已加入家庭
- **When**: 用户查询交易列表
- **Then**: 返回该家庭所有成员的交易
- **Verification**: `programmatic`

### AC-5: 前端支持两种模式
- **Given**: 不同使用场景
- **When**: 用户使用前端应用
- **Then**: 前端根据用户状态显示相应的界面和功能
- **Verification**: `human-judgment`

## Open Questions
- [ ] 如何处理现有的交易数据迁移
- [ ] 定价系统的具体实现方式
- [ ] 个人和家庭模式的UI差异设计