# iOS快捷指令配置文件

## 快捷指令名称
- **主程序**：记账小助手
- **安装器**：记账小助手安装器

## API配置
- **基础URL**：http://localhost:8000
- **认证端点**：
  - 注册：POST /api/auth/register
  - 登录：POST /api/auth/login
  - 获取用户信息：GET /api/auth/me

## 家庭管理端点
- **创建家庭**：POST /api/families/
- **获取家庭列表**：GET /api/families/
- **邀请成员**：POST /api/families/{family_id}/invite
- **获取家庭成员**：GET /api/families/{family_id}/members

## 交易管理端点
- **添加交易**：POST /api/transactions/
- **获取交易列表**：GET /api/transactions/
- **更新交易**：PUT /api/transactions/{transaction_id}
- **删除交易**：DELETE /api/transactions/{transaction_id}

## 统计分析端点
- **收支汇总**：GET /api/stats/summary
- **分类统计**：GET /api/stats/category
- **收支趋势**：GET /api/stats/trend

## AI服务端点
- **提取交易信息**：POST /api/ai/extract

## 版本管理端点
- **迁移到服务端**：POST /api/version/migrate-to-server
- **导出CSV**：GET /api/version/export-csv
- **切换版本**：POST /api/version/switch-version
- **获取版本状态**：GET /api/version/version-status

## 使用流程

### 1. 首次使用（注册）
1. 用户输入邮箱、用户名、密码
2. 调用 POST /api/auth/register
3. 保存返回的用户信息和JWT token
4. 将token存储在快捷指令的变量中

### 2. 日常使用（登录）
1. 用户输入邮箱、密码
2. 调用 POST /api/auth/login
3. 保存返回的JWT token
4. 将token存储在快捷指令的变量中

### 3. 语音记账
1. 用户说出消费内容
2. 调用 POST /api/ai/extract，传入文本
3. 获取AI提取的交易信息
4. 调用 POST /api/transactions/，传入交易数据
5. 显示记账成功提示

### 4. 截图记账
1. 用户选择支付截图
2. 将图片转换为Base64编码
3. 调用 POST /api/ai/extract，传入图片
4. 获取AI提取的交易信息
5. 调用 POST /api/transactions/，传入交易数据
6. 显示记账成功提示

### 5. 查看账单
1. 调用 GET /api/stats/summary 获取汇总
2. 调用 GET /api/stats/category 获取分类统计
3. 调用 GET /api/stats/trend 获取趋势分析
4. 在网页仪表盘中显示数据

### 6. 家庭管理
1. 创建家庭：调用 POST /api/families/
2. 邀请成员：调用 POST /api/families/{family_id}/invite
3. 查看成员：调用 GET /api/families/{family_id}/members

### 7. 版本切换
1. 检查版本状态：调用 GET /api/version/version-status
2. 迁移数据：调用 POST /api/version/migrate-to-server
3. 切换版本：调用 POST /api/version/switch-version

## 数据格式

### 请求格式
```json
{
  "username": "用户名",
  "email": "邮箱",
  "password": "密码"
}
```

### 响应格式
```json
{
  "id": "用户ID",
  "username": "用户名",
  "email": "邮箱",
  "created_at": "创建时间"
}
```

## 错误处理
- 400：请求参数错误
- 401：认证失败
- 403：权限不足
- 404：资源不存在
- 500：服务器内部错误

## 安全建议
1. JWT token存储在快捷指令变量中，不要暴露给用户
2. 敏感信息不要在快捷指令中显示
3. 定期更新token（30分钟过期）
4. 使用HTTPS传输数据（生产环境）