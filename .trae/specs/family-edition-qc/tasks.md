# Tasks

- [x] Task 1: 功能对照与缺陷清单
  - [x] SubTask 1.1: 对照“家庭版 8 项能力”梳理当前实现覆盖情况（后端/前端）
  - [x] SubTask 1.2: 产出需要修复的缺陷与缺失功能列表（以任务形式落入本 tasks.md）
  - Findings:
    - 家庭共享：无“最多 5 人”限制
    - 预算：预算表未出现在 Alembic 初始迁移；家庭预算不共享（读取按 user_id 过滤）；家庭预算已花费仅统计本人；预算/统计口径未排除收入
    - 多设备同步：交易删除为硬删除；无 deleted_at tombstone；无 updated_since/include_deleted 增量同步参数
    - 导出：仅 CSV 导出，无 Excel/PDF
    - 高级统计：仅 summary/category/trend，缺少“较昨天/较上周/较上月/较去年”对比与预测
    - AI：解析对 code fence/非严格 JSON 容错不足；分类集合与产品侧不一致风险

- [x] Task 2: 家庭共享上限与权限完善
  - [x] SubTask 2.1: 在邀请成员时校验家庭成员数 <= 5（含管理员）
  - [x] SubTask 2.2: 明确并实现家庭预算相关的管理员权限规则
  - [x] SubTask 2.3: 增补相关错误码与返回信息，便于前端展示

- [x] Task 3: 预算口径修复 + 家庭预算可共享 + 超预算提醒
  - [x] SubTask 3.1: 修复预算“已花费金额”口径（仅统计支出，家庭预算统计全家）
  - [x] SubTask 3.2: 调整预算查询与权限（家庭预算对成员可读，管理员可写；个人预算仅本人可见）
  - [x] SubTask 3.3: 新增/完善提醒接口或返回字段（用于客户端轮询提醒）

- [x] Task 4: 多设备同步能力补齐（增量 + 删除同步）
  - [x] SubTask 4.1: 为交易增加 deleted_at（软删除）并提供迁移脚本
  - [x] SubTask 4.2: 调整删除交易接口为软删除
  - [x] SubTask 4.3: 为交易列表接口增加 updated_since/include_deleted 等同步参数
  - [x] SubTask 4.4: 编写同步场景验证用例（增量更新与删除）

- [x] Task 5: 高级统计完善（环比/同比 + 预测）
  - [x] SubTask 5.1: 修复统计口径（仅支出；家庭维度统计全家）
  - [x] SubTask 5.2: 新增统计对比输出（较昨天/较上周/较上月/较去年）
  - [x] SubTask 5.3: 新增基础预测接口（轻量算法，明确输入输出与边界条件）

- [x] Task 6: 数据导出扩展（Excel / PDF）
  - [x] SubTask 6.1: 新增 Excel 导出 API（按家庭/日期范围过滤）
  - [x] SubTask 6.2: 新增 PDF 导出 API（含汇总与明细）
  - [x] SubTask 6.3: 增加必要依赖与最小验证脚本

- [x] Task 7: AI 增强（稳健解析与分类一致）
  - [x] SubTask 7.1: AI 返回解析增强（去 code fence、字段缺失容错、错误信息可诊断）
  - [x] SubTask 7.2: 分类归一与产品分类集合对齐（前后端一致）
  - [x] SubTask 7.3: 明确语音输入形态（客户端转文字后调用；必要时补充接口说明与测试）

- [x] Task 8: 端到端回归验证
  - [x] SubTask 8.1: 运行并补齐后端 API 测试脚本
  - [x] SubTask 8.2: 核对 checklist.md 全项通过

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1
- Task 4 depends on Task 1
- Task 5 depends on Task 1
- Task 6 depends on Task 1
- Task 7 depends on Task 1
- Task 8 depends on Task 2, Task 3, Task 4, Task 5, Task 6, Task 7
