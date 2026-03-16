# 验证V2版本功能 Spec

## Why
用户反馈添加交易时报错"添加失败：无法验证凭据"，需要全面验证V2版本的所有核心功能是否正常工作，确保系统稳定可用。

## What Changes
- 验证用户认证系统（注册、登录、JWT认证）
- 验证交易管理功能（添加、查询、更新、删除交易）
- 验证家庭管理功能（创建家庭、邀请成员）
- 验证统计分析功能（收支汇总、分类统计、趋势分析）
- 验证AI服务功能（文本和图片识别）
- 验证版本管理功能（数据迁移、版本切换）
- 修复发现的问题

## Impact
- Affected specs: server-backend, family-optional
- Affected code: backend/app/api/*, backend/app/schemas.py

## ADDED Requirements
### Requirement: 用户认证验证
系统应验证用户认证功能是否正常工作。

#### Scenario: 用户注册
- **WHEN** 用户提交注册信息
- **THEN** 系统成功创建用户账户并返回用户信息

#### Scenario: 用户登录
- **WHEN** 用户提交正确的邮箱和密码
- **THEN** 系统返回有效的JWT token

#### Scenario: 获取当前用户信息
- **WHEN** 用户使用有效的JWT token请求用户信息
- **THEN** 系统返回正确的用户信息

### Requirement: 交易管理验证
系统应验证交易管理功能是否正常工作。

#### Scenario: 添加交易（个人模式）
- **WHEN** 用户在个人模式下添加交易
- **THEN** 系统成功创建交易记录，family_id为None

#### Scenario: 添加交易（家庭模式）
- **WHEN** 用户在家庭模式下添加交易
- **THEN** 系统成功创建交易记录，family_id为家庭ID

#### Scenario: 查询交易列表
- **WHEN** 用户查询交易列表
- **THEN** 系统返回用户有权访问的所有交易记录

#### Scenario: 更新交易
- **WHEN** 用户更新自己的交易记录
- **THEN** 系统成功更新交易记录

#### Scenario: 删除交易
- **WHEN** 用户删除自己的交易记录
- **THEN** 系统成功删除交易记录

### Requirement: 家庭管理验证
系统应验证家庭管理功能是否正常工作。

#### Scenario: 创建家庭
- **WHEN** 用户创建家庭
- **THEN** 系统成功创建家庭并设置用户为管理员

#### Scenario: 邀请家庭成员
- **WHEN** 用户邀请成员加入家庭
- **THEN** 系统成功发送邀请

#### Scenario: 获取家庭成员列表
- **WHEN** 用户查询家庭成员列表
- **THEN** 系统返回正确的成员列表

### Requirement: 统计分析验证
系统应验证统计分析功能是否正常工作。

#### Scenario: 收支汇总
- **WHEN** 用户查询收支汇总
- **THEN** 系统返回正确的统计数据

#### Scenario: 分类统计
- **WHEN** 用户查询分类统计
- **THEN** 系统返回正确的分类统计数据

#### Scenario: 收支趋势
- **WHEN** 用户查询收支趋势
- **THEN** 系统返回正确的趋势数据

### Requirement: AI服务验证
系统应验证AI服务功能是否正常工作。

#### Scenario: 文本识别
- **WHEN** 用户提交文本描述
- **THEN** 系统返回提取的交易信息

#### Scenario: 图片识别
- **WHEN** 用户提交图片
- **THEN** 系统返回提取的交易信息

### Requirement: 版本管理验证
系统应验证版本管理功能是否正常工作。

#### Scenario: 数据迁移
- **WHEN** 用户提交CSV数据迁移
- **THEN** 系统成功导入数据

#### Scenario: 导出CSV
- **WHEN** 用户请求导出CSV
- **THEN** 系统返回正确的CSV数据

#### Scenario: 版本切换
- **WHEN** 用户切换版本
- **THEN** 系统成功切换版本

## MODIFIED Requirements
### Requirement: TransactionResponse模型
TransactionResponse模型的family_id字段应允许为None，以支持个人模式下的交易记录。

## REMOVED Requirements
无
