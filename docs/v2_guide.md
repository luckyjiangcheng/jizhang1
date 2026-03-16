# 记账小助手 V2 版本安装与使用文档（接口在线存储）

## 1. 版本定义

V2 是迭代后的在线存储方案，核心特征：

- 通过后端 API 存储与查询数据
- 使用授权码驱动安装、激活、写入、查询
- 支持按手机号聚合多个授权码的数据
- 支持返回 JSON 与 dashboard 可直接消费的 CSV

## 2. 适用对象

- 管理员：负责建户、发码、维护授权码状态
- 终端用户：通过快捷指令安装并完成记账
- 集成人员：对接快捷指令与 API

## 3. 前置准备

- 后端服务可访问（示例：`https://api.example.com`）
- 管理端已创建用户并分配授权码
- iPhone 已安装“快捷指令”App
- 快捷指令具备网络访问权限

## 4. 安装流程（用户侧）

### 步骤 1：安装快捷指令

安装以下快捷指令（按你的实际发布链接为准）：

- 记账小助手安装器
- 记账小助手
- 记账小助手账单

### 步骤 2：首次运行安装器

在安装器中输入：

- API Base URL（例如 `https://api.example.com`）
- 授权码（`LC-XXXXXXXXXXXX`）

### 步骤 3：安装器自动交互链路

安装器应按以下顺序调用：

1. `POST /api/v2/shortcut/install/check`
2. `POST /api/v2/shortcut/install/activate`

仅当检查结果 `allowed=true` 时执行激活。

### 步骤 4：安装完成

激活成功后，该授权码状态变为 `used`，不可再次安装。

## 5. 记账流程（用户侧）

### 5.1 写入记账数据

调用：

- `POST /api/v2/shortcut/transactions`

请求体需携带授权码（`code` 或 `license_code`）以及交易字段（日期、金额、分类等）。

### 5.2 查看清单（JSON）

调用：

- `GET /api/v2/shortcut/transactions/dashboard?license_code=...`

返回该授权码关联手机号下“全部授权码”的聚合交易清单（时间倒序）。

### 5.3 查看清单（CSV）

调用：

- `GET /api/v2/shortcut/transactions/dashboard.csv?license_code=...`

返回 `text/csv`，字段可直接给 `src/dashboard.txt`/`public/dashboard.txt` 消费。

## 6. 接口清单

### 6.1 安装可用性检查

- Method: `POST`
- Path: `/api/v2/shortcut/install/check`
- 用途：校验授权码是否允许安装

### 6.2 安装激活

- Method: `POST`
- Path: `/api/v2/shortcut/install/activate`
- 用途：将可安装授权码标记为已激活

### 6.3 记账写入

- Method: `POST`
- Path: `/api/v2/shortcut/transactions`
- 用途：将交易写入授权码及所属账号

### 6.4 聚合清单（JSON）

- Method: `GET`
- Path: `/api/v2/shortcut/transactions/dashboard`
- 用途：按授权码反查手机号并返回全码聚合数据

### 6.5 聚合清单（CSV）

- Method: `GET`
- Path: `/api/v2/shortcut/transactions/dashboard.csv`
- 用途：返回 dashboard 可直接消费的 CSV 数据

## 7. 推荐快捷指令分支逻辑

### 安装器分支

1. 调用 `install/check`
2. 若 `allowed=false`：
   - 弹窗显示 `reason`
   - 结束流程
3. 若 `allowed=true`：
   - 调用 `install/activate`
   - 提示“安装完成”

### 记账分支

1. 收集交易数据
2. 调用 `shortcut/transactions`
3. 成功后提示“已记账”
4. 失败显示服务端 `message`

### 账单分支

1. 优先拉取 `dashboard.csv`
2. 若 CSV 拉取失败，回退 `dashboard` JSON
3. 呈现错误文案与重试按钮

## 8. 错误语义建议

- 授权码不存在：提示“授权码不存在，请检查输入”
- 授权码已安装激活：提示“该授权码已使用，请联系管理员发码”
- 授权码已禁用：提示“授权码已禁用，请联系管理员”
- 授权码未激活：提示“请先通过安装器完成激活”
- 参数校验失败：提示“提交字段不完整，请重试”

## 9. 验收清单

- 安装器可完成检查→激活链路
- 同一授权码二次激活被拒绝
- 记账写入可落库并关联授权码与用户
- JSON 聚合可返回同手机号下所有授权码数据
- CSV 聚合可直接驱动 dashboard 展示

## 10. 相关文件

- 后端接口实现：`backend/app/api/v2.py`
- 接口模型定义：`backend/app/schemas.py`
- Dashboard 模板：`src/dashboard.txt`、`public/dashboard.txt`
