# 配置清单

## MySQL 账号密码

- Host: `localhost`
- Port: `3306`
- 数据库: `jizhang_db`
- 普通账号: `jizhang_user`
- 普通密码: `jizhang_password`
- Root 密码: `rootpassword`

## 系统登录账号密码

### 登录地址

- 前端地址: `http://localhost/`
- 后端地址: `http://localhost:8000`

### 管理员账号（root）

- 用户名: `root`
- 邮箱: `root@local.dev`
- 密码: `root123456`
- 登录方式: 管理端使用邮箱登录（root）

### 普通用户账号规则

- 登录账号: 管理员创建时填写的手机号
- 初始密码: 手机号后 6 位
- 登录方式: 用户端使用手机号 + 密码登录
- 当前默认: 系统不预置固定普通用户，需在 root 后台新增后才可登录

### 普通用户账号密码（填写区）

- 用户1手机号（个人版）: `13910010001`
- 用户1密码: `010001`
- 用户2手机号（家庭版）: `13910010002`
- 用户2密码: `010002`

## 登录说明（重要）

- 管理端 root 登录参数: `email + password`（不是 `phone`）
- 用户端登录参数: `phone + password`
- 如果出现 `phone: Field required`，说明你在用户登录接口传了邮箱字段，请改为手机号字段
