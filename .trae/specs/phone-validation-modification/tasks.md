# 手机号验证逻辑修改 - 实现计划

## [x] 任务1: 修改前端登录页面验证逻辑
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 修改前端 index.html 中的登录验证逻辑
  - 移除11位数字限制，改为支持数字、中文、英文组合
  - 添加100个字符的长度限制验证
  - 更新输入框占位符和错误提示
- **Acceptance Criteria Addressed**: AC-1, AC-2
- **Test Requirements**:
  - `programmatic` TR-1.1: 输入超过100个字符时显示错误提示
  - `human-judgement` TR-1.2: 输入包含中文、英文的账号时不显示格式错误
- **Notes**: 需修改 frontend/index.html 文件中的 login 函数

## [x] 任务2: 修改后端登录API逻辑
- **Priority**: P0
- **Depends On**: 任务1
- **Description**: 
  - 修改后端 auth.py 中的登录API
  - 确保通过用户名字段查找用户的逻辑正确
  - 保持现有通过手机号查找用户的逻辑不变
- **Acceptance Criteria Addressed**: AC-3, AC-4
- **Test Requirements**:
  - `programmatic` TR-2.1: 使用非数字账号登录成功
  - `programmatic` TR-2.2: 使用现有手机号登录成功
- **Notes**: 需修改 backend/app/api/auth.py 文件中的 login 函数

## [x] 任务3: 测试验证
- **Priority**: P1
- **Depends On**: 任务1, 任务2
- **Description**: 
  - 测试非数字账号登录
  - 测试现有手机号登录
  - 测试账号长度限制
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-3, AC-4
- **Test Requirements**:
  - `programmatic` TR-3.1: 所有测试用例通过
  - `human-judgement` TR-3.2: 用户体验良好
- **Notes**: 可使用 curl 命令或浏览器测试