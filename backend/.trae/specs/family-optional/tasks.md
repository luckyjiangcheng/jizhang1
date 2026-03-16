# 记账小助手 - 家庭可选功能实施计划

## [x] Task 1: 修改交易数据库模型，将 family_id 字段设为可选
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 修改 Transaction 模型中的 family_id 字段，将 nullable 设置为 True
  - 确保数据库迁移脚本正确处理这一变更
  - 保持现有数据的完整性
- **Acceptance Criteria Addressed**: AC-1, AC-2
- **Test Requirements**:
  - `programmatic` TR-1.1: 数据库迁移成功执行
  - `programmatic` TR-1.2: 交易表结构中 family_id 字段允许 NULL 值
- **Notes**: 这是核心变更，需要谨慎处理数据库迁移

## [x] Task 2: 修改交易创建 API，支持无家庭情况下的交易创建
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 修改 create_transaction 函数，移除强制家庭会员检查
  - 当用户未加入家庭时，交易不关联家庭
  - 当用户已加入家庭时，交易自动关联家庭
- **Acceptance Criteria Addressed**: AC-1, AC-2
- **Test Requirements**:
  - `programmatic` TR-2.1: 未加入家庭的用户可以成功创建交易
  - `programmatic` TR-2.2: 已加入家庭的用户创建的交易自动关联家庭
  - `programmatic` TR-2.3: API 响应时间保持在合理范围内
- **Notes**: 需要修改 transactions.py 中的核心逻辑

## [x] Task 3: 修改交易查询 API，支持个人和家庭模式的查询
- **Priority**: P0
- **Depends On**: Task 1, Task 2
- **Description**:
  - 修改 get_transactions 函数，支持查询个人交易和家庭交易
  - 个人模式下只返回用户自己的交易
  - 家庭模式下返回用户和家庭成员的交易
- **Acceptance Criteria Addressed**: AC-1, AC-2
- **Test Requirements**:
  - `programmatic` TR-3.1: 未加入家庭的用户只能查询到自己的交易
  - `programmatic` TR-3.2: 已加入家庭的用户可以查询到家庭交易
  - `programmatic` TR-3.3: 查询性能不受影响
- **Notes**: 需要调整查询逻辑，确保数据安全和性能

## [x] Task 4: 修改家庭管理 API，支持模式切换
- **Priority**: P1
- **Depends On**: Task 1, Task 2, Task 3
- **Description**:
  - 修改家庭创建和加入逻辑，支持将个人交易关联到新家庭
  - 提供 API 端点，允许用户选择是否将现有交易与家庭关联
- **Acceptance Criteria Addressed**: AC-3
- **Test Requirements**:
  - `programmatic` TR-4.1: 用户创建家庭后可以选择关联现有交易
  - `programmatic` TR-4.2: 交易关联过程不丢失数据
  - `human-judgment` TR-4.3: API 设计符合 RESTful 规范
- **Notes**: 需要考虑数据迁移的性能和可靠性

## [ ] Task 5: 修改前端界面，支持个人和家庭模式
- **Priority**: P1
- **Depends On**: Task 1, Task 2, Task 3
- **Description**:
  - 修改交易表单，根据用户状态显示不同的界面
  - 当用户未加入家庭时，不显示家庭相关选项
  - 当用户已加入家庭时，显示家庭关联信息
- **Acceptance Criteria Addressed**: AC-1, AC-2
- **Test Requirements**:
  - `programmatic` TR-5.1: 未加入家庭的用户看到个人模式界面
  - `programmatic` TR-5.2: 已加入家庭的用户看到家庭模式界面
  - `human-judgment` TR-5.3: 界面设计符合用户体验要求
- **Notes**: 需要确保前端与后端 API 同步

## [x] Task 6: 实现使用模式识别，支持定价计划
- **Priority**: P1
- **Depends On**: Task 1, Task 2, Task 3
- **Description**:
  - 添加 API 端点，返回用户的使用模式（个人或家庭）
  - 实现使用模式的判断逻辑
  - 为后续的定价计划集成做准备
- **Acceptance Criteria Addressed**: AC-4
- **Test Requirements**:
  - `programmatic` TR-6.1: API 正确返回用户的使用模式
  - `programmatic` TR-6.2: 使用模式判断逻辑准确
  - `human-judgment` TR-6.3: API 设计符合系统架构
- **Notes**: 具体的定价逻辑将在后续实现

## [x] Task 7: 测试和验证
- **Priority**: P0
- **Depends On**: 所有其他任务
- **Description**:
  - 运行完整的测试套件
  - 验证所有功能正常工作
  - 确保系统稳定性和性能
- **Acceptance Criteria Addressed**: 所有
- **Test Requirements**:
  - `programmatic` TR-7.1: 所有单元测试通过
  - `programmatic` TR-7.2: 集成测试通过
  - `human-judgment` TR-7.3: 系统整体运行正常
- **Notes**: 需要全面测试，确保功能完整性和系统稳定性