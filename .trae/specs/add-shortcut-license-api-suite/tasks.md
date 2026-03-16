# Tasks

- [ ] Task 1: 定义快捷指令接口契约与响应模型
  - [ ] SubTask 1.1: 明确安装校验接口请求/响应字段与状态码
  - [ ] SubTask 1.2: 明确安装激活接口请求/响应字段与状态码
  - [ ] SubTask 1.3: 明确记账写入接口请求/响应字段与状态码
  - [ ] SubTask 1.4: 明确聚合清单 JSON/CSV 接口字段并覆盖 dashboard 字段需求
  - [ ] SubTask 1.5: 产出快捷指令调用顺序与失败分支处理约定

- [ ] Task 2: 实现安装前授权码可用性检查接口
  - [ ] SubTask 2.1: 增加可用性判定逻辑（unused 可安装）
  - [ ] SubTask 2.2: 返回统一错误语义（used/disabled/not-found）

- [ ] Task 3: 实现安装激活接口
  - [ ] SubTask 3.1: 安装成功后将授权码状态更新为 used
  - [ ] SubTask 3.2: 重复安装返回明确错误并禁止状态回退

- [ ] Task 4: 实现授权码记账写入接口
  - [ ] SubTask 4.1: 校验授权码与账号关系
  - [ ] SubTask 4.2: 交易写入并绑定 `license_code_id` 与 `user_id`
  - [ ] SubTask 4.3: 输出标准化写入结果

- [ ] Task 5: 实现跨授权码聚合清单接口（JSON + CSV）
  - [ ] SubTask 5.1: 通过输入授权码定位手机号归属
  - [ ] SubTask 5.2: 查询该手机号下全部授权码对应交易数据
  - [ ] SubTask 5.3: 输出 JSON 清单（时间倒序）
  - [ ] SubTask 5.4: 输出 dashboard 可直接消费的 CSV（固定表头与字段顺序）

- [ ] Task 6: 验证与回归
  - [ ] SubTask 6.1: 覆盖安装校验、安装激活、写入、聚合（JSON/CSV）主链路
  - [ ] SubTask 6.2: 覆盖异常场景（无效码、不可安装、重复安装、越权访问）
  - [ ] SubTask 6.3: 校验 dashboard.txt 对 CSV 直接消费无二次转换
  - [ ] SubTask 6.4: 校验旧接口兼容性与现有前端不回归

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1 and Task 2
- Task 4 depends on Task 1 and Task 3
- Task 5 depends on Task 1 and Task 4
- Task 6 depends on Task 2, Task 3, Task 4 and Task 5
