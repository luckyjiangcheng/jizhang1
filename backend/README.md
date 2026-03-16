# 记账小助手后端服务

基于Python + FastAPI的后端服务，为记账小助手提供服务端能力。

## 技术栈

- **后端框架**: FastAPI 0.104.1
- **数据库**: MySQL 8.0
- **缓存**: Redis 7
- **认证**: JWT + bcrypt
- **部署**: Docker + Docker Compose

## 功能特性

- 用户认证系统（注册、登录、JWT）
- 家庭管理功能（创建家庭、邀请成员）
- 交易数据管理（CRUD、筛选、同步）
- 统计分析功能（汇总、分类、趋势）
- AI服务代理（语音、图片识别）
- 版本管理功能（切换、迁移）

## 快速开始

### 前置要求

- Python 3.11+
- Docker 和 Docker Compose
- Git

### 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd jizhang1/backend
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，设置数据库密码、API密钥等
```

3. 启动服务
```bash
docker-compose up -d
```

4. 访问API文档
```
http://localhost:8000/docs
```

## API端点

### 认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 家庭管理
- `POST /api/families/` - 创建家庭
- `GET /api/families/` - 获取用户家庭列表
- `POST /api/families/{family_id}/invite` - 邀请成员
- `GET /api/families/{family_id}/members` - 获取家庭成员

### 交易管理
- `POST /api/transactions/` - 添加交易
- `GET /api/transactions/` - 获取交易列表
- `GET /api/transactions/{transaction_id}` - 获取交易详情
- `PUT /api/transactions/{transaction_id}` - 更新交易
- `DELETE /api/transactions/{transaction_id}` - 删除交易

### 统计分析
- `GET /api/stats/summary` - 获取收支汇总
- `GET /api/stats/category` - 获取分类统计
- `GET /api/stats/trend` - 获取收支趋势

### AI服务
- `POST /api/ai/extract` - 提取交易信息

## 数据库结构

### 用户表 (users)
- id (UUID) - 用户唯一标识
- username - 用户名
- email - 邮箱
- password_hash - 密码哈希
- created_at - 创建时间
- updated_at - 更新时间

### 家庭表 (families)
- id (UUID) - 家庭唯一标识
- name - 家庭名称
- creator_id - 创建者ID
- created_at - 创建时间

### 家庭成员表 (family_members)
- id (UUID) - 记录唯一标识
- family_id - 家庭ID
- user_id - 用户ID
- role - 角色（管理员/成员）
- joined_at - 加入时间

### 交易表 (transactions)
- id (UUID) - 交易唯一标识
- family_id - 家庭ID
- user_id - 录入用户ID
- date - 交易日期
- time - 交易时间
- amount - 金额
- category - 分类
- item - 项目
- merchant - 商家
- notes - 备注
- created_at - 创建时间
- updated_at - 更新时间

## 性能优化

- 数据库连接池（pool_size=10, max_overflow=20）
- Redis缓存
- 数据库索引优化
- 异步处理

## 安全措施

- JWT认证
- 密码bcrypt加密
- HTTPS传输
- API Key保护
- 请求限流

## 开发指南

### 运行开发环境
```bash
# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
uvicorn main:app --reload
```

### 运行测试
```bash
# 安装测试依赖
pip install pytest pytest-asyncio httpx

# 运行测试
pytest
```

## 部署

### Docker部署
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 云服务器部署
1. 配置云服务器（AWS、阿里云、腾讯云等）
2. 安装Docker和Docker Compose
3. 上传项目文件
4. 配置环境变量
5. 启动服务
6. 配置域名和HTTPS

## 故障排查

### 数据库连接失败
- 检查MySQL容器是否运行
- 验证数据库连接字符串
- 检查防火墙设置

### AI服务调用失败
- 验证API Key是否正确
- 检查网络连接
- 查看AI服务状态

### 性能问题
- 检查数据库索引
- 优化查询语句
- 增加缓存

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License