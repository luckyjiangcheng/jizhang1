# 记账小助手服务端解决方案

## 1. 服务端架构设计

### 技术选型
- **后端框架**：Node.js + Express 或 Python + FastAPI
- **数据库**：PostgreSQL 或 MongoDB
- **认证**：JWT (JSON Web Token)
- **部署**：云服务器（AWS、阿里云、腾讯云等）
- **API设计**：RESTful API

### 核心组件
1. **用户服务**：处理用户注册、登录、认证
2. **账本服务**：管理账本数据，支持多用户共享
3. **API代理**：保护API Key，处理AI请求
4. **数据同步**：确保多设备数据一致性

## 2. 数据模型设计

### 用户表 (users)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | UUID | 用户唯一标识 |
| username | String | 用户名 |
| email | String | 邮箱（唯一） |
| password_hash | String | 密码哈希 |
| created_at | Timestamp | 创建时间 |
| updated_at | Timestamp | 更新时间 |

### 家庭表 (families)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | UUID | 家庭唯一标识 |
| name | String | 家庭名称 |
| creator_id | UUID | 创建者ID |
| created_at | Timestamp | 创建时间 |

### 家庭成员表 (family_members)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | UUID | 记录唯一标识 |
| family_id | UUID | 家庭ID |
| user_id | UUID | 用户ID |
| role | String | 角色（管理员/成员） |
| joined_at | Timestamp | 加入时间 |

### 交易表 (transactions)
| 字段名 | 类型 | 描述 |
|-------|------|------|
| id | UUID | 交易唯一标识 |
| family_id | UUID | 家庭ID |
| user_id | UUID | 录入用户ID |
| date | Date | 交易日期 |
| time | String | 交易时间 |
| amount | Decimal | 金额 |
| category | String | 分类 |
| item | String | 项目 |
| merchant | String | 商家 |
| notes | String | 备注 |
| created_at | Timestamp | 创建时间 |
| updated_at | Timestamp | 更新时间 |

## 3. API接口设计

### 认证接口
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/refresh` - 刷新Token

### 家庭接口
- `POST /api/families` - 创建家庭
- `GET /api/families` - 获取用户所属家庭
- `POST /api/families/{id}/invite` - 邀请成员加入家庭
- `GET /api/families/{id}/members` - 获取家庭成员

### 交易接口
- `POST /api/transactions` - 添加交易
- `GET /api/transactions` - 获取交易列表（支持筛选）
- `PUT /api/transactions/{id}` - 更新交易
- `DELETE /api/transactions/{id}` - 删除交易

### 统计接口
- `GET /api/stats/summary` - 获取收支汇总
- `GET /api/stats/category` - 获取分类统计
- `GET /api/stats/trend` - 获取收支趋势

### AI接口
- `POST /api/ai/extract` - 提取交易信息（语音/图片）

## 4. 安全措施

### API Key保护
- API Key存储在服务端环境变量中，不暴露给前端
- 所有AI请求通过服务端代理发送，前端只与服务端API交互

### 数据加密
- 用户密码使用bcrypt加密存储
- JWT密钥定期轮换
- 敏感数据传输使用HTTPS

### 访问控制
- 基于JWT的认证机制
- 基于角色的权限控制（RBAC）
- API请求限流，防止滥用

### 数据备份
- 定期数据库备份
- 多地域备份，确保数据安全

## 5. 前端适配

### 快捷指令修改
- 移除本地API Key配置
- 添加用户登录/注册流程
- 交易数据通过API发送到服务端
- 从服务端获取交易数据和统计信息

### 仪表盘优化
- 支持多用户切换
- 显示家庭成员各自的消费情况
- 提供家庭总支出和个人支出对比

## 6. 实施步骤

### 第一阶段：后端服务搭建
1. 初始化后端项目，配置依赖
2. 设计数据库 schema
3. 实现用户认证系统
4. 开发核心API接口
5. 部署到云服务器

### 第二阶段：前端适配
1. 修改快捷指令，集成服务端API
2. 优化仪表盘页面，支持多用户
3. 测试端到端流程

### 第三阶段：家庭共享功能
1. 实现家庭创建和成员管理
2. 开发交易数据共享机制
3. 测试多用户并发操作

### 第四阶段：VIP功能
1. 实现订阅管理系统
2. 开发高级统计功能
3. 集成支付系统

## 7. 优势与收益

### 技术优势
- **更高的安全性**：API Key不暴露，数据存储在服务端
- **更便捷的共享**：无需配置iCloud共享，直接通过服务端同步
- **更强大的功能**：支持实时统计、多设备同步等高级功能
- **更好的扩展性**：易于添加新功能和服务

### 商业收益
- **可控的API使用**：通过服务端代理，可监控和限制API调用
- **增值服务**：VIP功能可带来持续收入
- **用户粘性**：家庭共享功能增加用户依赖性
- **数据价值**：聚合的消费数据可用于分析和优化

## 8. 风险与应对

### 技术风险
- **服务可用性**：部署多实例，配置负载均衡
- **数据安全**：定期安全审计，加密存储敏感数据
- **性能优化**：数据库索引优化，缓存热点数据

### 运营风险
- **API成本**：实施请求限流，合理使用API资源
- **用户隐私**：严格遵守隐私政策，透明数据使用
- **服务成本**：优化服务器配置，合理控制成本

## 9. 结论

通过将数据存储在服务端，可以实现更安全、更便捷的用户认证和数据共享。服务端架构不仅解决了API Key保护问题，还为家庭共享功能提供了更可靠的技术基础。同时，VIP模式可以为产品带来持续的收入，支持进一步的功能开发和服务优化。

这种方案不仅提升了用户体验，还为产品的长期发展奠定了坚实的技术基础。