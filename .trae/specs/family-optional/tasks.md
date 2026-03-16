# 记账小助手V2 - 家庭可选功能实现计划

## [ ] 任务1: 修改数据库模型
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 修改 `transactions` 表的 `family_id` 字段为可选
  - 更新数据库迁移脚本
  - 确保现有数据的兼容性
- **Acceptance Criteria Addressed**: AC-1, AC-4
- **Test Requirements**:
  - `programmatic` TR-1.1: 数据库迁移成功，`family_id` 字段变为可选
  - `programmatic` TR-1.2: 现有交易数据保持不变
- **Notes**: 需要修改 alembic 迁移文件，确保向后兼容

## [ ] 任务2: 修改交易API - 添加交易
- **Priority**: P0
- **Depends On**: 任务1
- **Description**:
  - 修改 `create_transaction` 函数，支持无家庭ID的情况
  - 当用户无家庭时，`family_id` 设为 NULL
  - 当用户有家庭时，使用默认家庭ID
- **Acceptance Criteria Addressed**: AC-1, AC-2
- **Test Requirements**:
  - `programmatic` TR-2.1: 个人用户可以成功添加交易
  - `programmatic` TR-2.2: 家庭用户可以成功添加交易
  - `programmatic` TR-2.3: 交易数据正确保存
- **Notes**: 需要修改 `transactions.py` 中的逻辑

## [ ] 任务3: 修改交易API - 获取交易列表
- **Priority**: P0
- **Depends On**: 任务1
- **Description**:
  - 修改 `get_transactions` 函数，支持无家庭ID的情况
  - 当用户无家庭时，只返回该用户的交易
  - 当用户有家庭时，返回家庭所有成员的交易
- **Acceptance Criteria Addressed**: AC-3, AC-4
- **Test Requirements**:
  - `programmatic` TR-3.1: 个人用户只能看到自己的交易
  - `programmatic` TR-3.2: 家庭用户可以看到家庭所有交易
  - `programmatic` TR-3.3: 交易列表正确返回
- **Notes**: 需要修改查询逻辑，处理无家庭ID的情况

## [ ] 任务4: 修改交易API - 其他操作
- **Priority**: P1
- **Depends On**: 任务1
- **Description**:
  - 修改 `get_transaction`、`update_transaction`、`delete_transaction` 函数
  - 支持无家庭ID的交易操作
  - 确保权限验证正确
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-3, AC-4
- **Test Requirements**:
  - `programmatic` TR-4.1: 个人用户可以操作自己的交易
  - `programmatic` TR-4.2: 家庭用户可以操作家庭内的交易
  - `programmatic` TR-4.3: 权限验证正确
- **Notes**: 需要修改权限验证逻辑

## [ ] 任务5: 修改统计API
- **Priority**: P1
- **Depends On**: 任务1
- **Description**:
  - 修改统计相关API，支持无家庭ID的情况
  - 当用户无家庭时，统计个人交易
  - 当用户有家庭时，统计家庭交易
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-3, AC-4
- **Test Requirements**:
  - `programmatic` TR-5.1: 个人用户可以查看个人统计
  - `programmatic` TR-5.2: 家庭用户可以查看家庭统计
  - `programmatic` TR-5.3: 统计数据正确计算
- **Notes**: 需要修改 `stats.py` 中的逻辑

## [ ] 任务6: 修改前端代码
- **Priority**: P1
- **Depends On**: 任务2, 任务3
- **Description**:
  - 修改前端交易表单，支持个人和家庭模式
  - 根据用户状态显示相应的界面
  - 处理无家庭时的逻辑
- **Acceptance Criteria Addressed**: AC-5
- **Test Requirements**:
  - `human-judgment` TR-6.1: 前端界面适配个人模式
  - `human-judgment` TR-6.2: 前端界面适配家庭模式
  - `human-judgment` TR-6.3: 切换模式时界面正常
- **Notes**: 需要修改 `index.html` 中的逻辑

## [ ] 任务7: 测试和验证
- **Priority**: P0
- **Depends On**: 所有任务
- **Description**:
  - 测试个人用户功能
  - 测试家庭用户功能
  - 验证向后兼容性
  - 性能测试
- **Acceptance Criteria Addressed**: 所有AC
- **Test Requirements**:
  - `programmatic` TR-7.1: 所有API端点正常工作
  - `programmatic` TR-7.2: 现有功能不受影响
  - `programmatic` TR-7.3: 性能符合要求
- **Notes**: 需要全面测试各种场景