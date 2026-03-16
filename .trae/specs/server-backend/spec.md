# 记账小助手后端服务 - 产品需求文档

## Overview

* **Summary**: 设计并实现一个独立的后端服务模块，为基于iOS快捷指令的记账小助手提供服务端能力，同时保留现有MVP的单机版本功能，实现双版本并存。

* **Purpose**: 解决API Key安全问题，实现家庭共享功能，为后续扩展更多服务能力奠定基础。

* **Target Users**: 记账小助手用户，包括个人用户和家庭用户。

* **Implementation Form**: 基于iOS快捷指令的插件形式，配合网页仪表盘，后端服务作为支撑。

## Goals

* 构建独立的后端服务模块，支持用户认证和数据管理

* 实现家庭共享功能，支持多用户共同记账

* 保护API Key安全，通过服务端代理处理AI请求

* 保留现有MVP的单机版本功能，实现双版本并存

* 为后续扩展更多服务能力提供基础架构

## Non-Goals (Out of Scope)

* 完全替代现有单机版本

* 实现复杂的财务分析功能

* 支持多语言国际化

* 开发移动应用原生客户端

## Background & Context

* 现有记账小助手是基于iOS快捷指令和本地CSV文件存储的单机应用

* 存在API Key暴露和无法实现家庭共享的问题

* 需要一个独立的后端服务来解决这些问题，同时为未来功能扩展做准备

## Functional Requirements

* **FR-1**: 用户认证系统

  * 支持用户注册、登录、密码重置

  * 基于JWT的身份验证

  * 支持邮箱和手机号注册

* **FR-2**: 家庭管理功能

  * 创建家庭

  * 邀请成员加入家庭

  * 管理家庭成员权限

* **FR-3**: 交易数据管理

  * 添加、查询、更新、删除交易记录

  * 支持按时间、分类、用户等维度筛选

  * 数据同步和冲突处理

* **FR-4**: 统计分析功能

  * 收支汇总

  * 分类统计

  * 收支趋势分析

* **FR-5**: AI服务代理

  * 处理语音和图片识别请求

  * 保护API Key安全

  * 优化AI请求处理

* **FR-6**: 版本管理

  * 支持单机版本和服务端版本并存

  * 提供版本切换机制

  * 数据迁移功能

## Non-Functional Requirements

* **NFR-1**: 安全性

  * API Key存储在服务端，不暴露给前端

  * 用户密码加密存储

  * 所有数据传输使用HTTPS

* **NFR-2**: 性能

  * API响应时间不超过500ms

  * 支持并发用户数不少于1000

  * 数据同步延迟不超过1秒

* **NFR-3**: 可靠性

  * 服务可用性达到99.9%

  * 数据定期备份

  * 错误处理和日志记录

* **NFR-4**: 可扩展性

  * 模块化架构设计

  * 支持水平扩展

  * 易于添加新功能

## Constraints

*- **Technical**: 
  - 后端框架：Python + FastAPI
  - 数据库：MySQL
  - 部署：Docker容器 + 云服务器
  - 性能优化：数据库索引、缓存机制、连接池
  - iOS方案：快捷指令 + 网页仪表盘
  - Android方案：PWA（渐进式Web应用）

* **Business**:

  * 成本控制：初期使用云服务免费额度

  * 开发周期：2-4周完成MVP

* **Dependencies**:

  * 第三方AI服务API

  * 云服务提供商

## Assumptions

* 用户拥有iOS设备和iCloud账户

* 网络连接稳定

* 用户接受基本的注册登录流程

## Acceptance Criteria

### AC-1: 用户认证

* **Given**: 用户未注册

* **When**: 用户提交注册信息

* **Then**: 系统创建用户账户并返回JWT token

* **Verification**: `programmatic`

### AC-2: 家庭管理

* **Given**: 用户已登录

* **When**: 用户创建家庭并邀请成员

* **Then**: 家庭成员收到邀请并能加入家庭

* **Verification**: `programmatic`

### AC-3: 交易管理

* **Given**: 用户已加入家庭

* **When**: 用户添加交易记录

* **Then**: 所有家庭成员能看到该交易记录

* **Verification**: `programmatic`

### AC-4: 统计分析

* **Given**: 家庭有交易记录

* **When**: 用户查看统计数据

* **Then**: 系统显示正确的收支汇总和趋势

* **Verification**: `programmatic`

### AC-5: AI服务

* **Given**: 用户提交语音或图片

* **When**: 系统处理AI请求

* **Then**: 系统返回提取的交易信息

* **Verification**: `programmatic`

### AC-6: 版本并存

* **Given**: 用户使用单机版本

* **When**: 用户切换到服务端版本

* **Then**: 数据成功迁移到服务端

* **Verification**: `programmatic`

## Open Questions

* [ ] 具体的云服务提供商选择

* [ ] 数据库选型（PostgreSQL vs MongoDB）

* [ ] 具体的API rate limiting策略

* [ ] 数据迁移的具体实现方案

