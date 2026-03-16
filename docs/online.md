# 阿里云服务器部署操作手册（ECS）

本文档用于把当前项目部署到阿里云 ECS，并验证 V2 接口与快捷指令可正常使用。

## 1. 部署目标

- 前端访问地址：`http://<你的服务器公网IP>/`
- 后端接口地址：`http://<你的服务器公网IP>:8000`
- 关键接口：
  - `POST /api/v2/shortcut/transactions`
  - `GET /api/v2/shortcut/transactions/dashboardforcsv`

## 2. 阿里云资源准备

### 2.1 创建 ECS

- 地域：就近（如华东/华北）
- 规格：建议至少 `2核4G`
- 系统：Ubuntu 22.04 LTS
- 系统盘：建议 40G+

### 2.2 安全组放行

至少放行以下入方向端口：

- `22`（SSH）
- `80`（前端）
- `8000`（后端 API）
- `3306`（可选，仅调试，不建议公网放开）
- `6379`（可选，仅调试，不建议公网放开）

建议：生产环境仅放行 `22/80/443`，数据库和 Redis 仅内网访问。

## 3. 服务器初始化

SSH 登录 ECS 后执行：

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg git
```

安装 Docker：

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable docker
sudo systemctl start docker
```

## 4. 上传项目代码

方式一（推荐）：

```bash
git clone <你的仓库地址> jizhang1
cd jizhang1
```

方式二（本地打包上传）：

- 本地压缩项目上传到服务器
- 解压到如 `/opt/jizhang1`

## 5. 部署前配置检查（重点）

### 5.1 后端配置文件

确认以下文件存在并正确：

- `backend/docker-compose.yml`
- `public/config.json`

当前部署依赖 `public/config.json`（包含 `api_base`、`text_model`、`jj_prompt`）挂载到后端容器：

- 挂载路径：`/app/config.json`

### 5.2 生产安全建议（必须做）

请修改以下敏感信息，不要用默认值：

- `public/config.json` 的 `api_key`
- `backend/docker-compose.yml` 中数据库密码
- `backend/.env`（若使用）中的 `SECRET_KEY`

## 6. 启动服务

在服务器执行：

```bash
cd /opt/jizhang1/backend
docker compose down
docker compose up -d --build
```

查看服务状态：

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

预期容器：

- `jizhang_mysql`
- `jizhang_redis`
- `jizhang_backend`
- `jizhang_frontend`

## 7. 部署成功验证

### 7.1 基础健康检查

```bash
curl http://127.0.0.1:8000/health
```

预期：

```json
{"status":"healthy"}
```

### 7.2 外网访问检查

在你本地电脑执行：

```bash
curl http://<公网IP>:8000/health
curl -I http://<公网IP>/
```

### 7.3 关键接口检查

```bash
curl -X POST "http://<公网IP>:8000/api/v2/shortcut/transactions" \
  -H "Content-Type: application/json" \
  -d '{
    "license_code":"LC-你的授权码",
    "text":"昨天晚上和朋友吃火锅花了258元，在海底捞"
  }'
```

CSV：

```bash
curl -G "http://<公网IP>:8000/api/v2/shortcut/transactions/dashboardforcsv" \
  --data-urlencode "license_code=LC-你的授权码"
```

## 8. 快捷指令侧配置

把快捷指令中的接口域名统一改为公网地址：

- 写入接口：`http://<公网IP>:8000/api/v2/shortcut/transactions`
- CSV 接口：`http://<公网IP>:8000/api/v2/shortcut/transactions/dashboardforcsv?license_code=...`

注意：

- `dashboardforcsv` 使用 `GET`
- 不要在 URL 字段里混入多行文本或字典对象
- 手机若使用 5G，不能访问内网 IP（10.x/192.168.x），必须公网地址或 VPN

## 9. 常用运维命令

查看日志：

```bash
cd /opt/jizhang1/backend
docker compose logs -f backend
docker compose logs -f frontend
```

重启服务：

```bash
docker restart jizhang_backend
docker restart jizhang_frontend
```

仅重建后端：

```bash
cd /opt/jizhang1/backend
docker compose up -d --build backend
```

## 10. 常见问题排查

### 10.1 502 Bad Gateway

表现：前端能打开，接口 502  
排查：

```bash
docker logs --tail 200 jizhang_frontend
docker logs --tail 200 jizhang_backend
```

若前端日志出现 `connect() failed (111: Connection refused)`，说明后端未就绪或挂了。

### 10.2 快捷指令超时但电脑 curl 正常

- 检查手机是否走 5G（不能访问内网 IP）
- 检查安全组是否放行 8000
- 检查 URL 是否写成公网地址

### 10.3 接口返回 `jj_prompt 未配置`

- 检查 `public/config.json` 是否存在
- 检查 `backend/docker-compose.yml` 的 config 挂载是否生效
- 重启后端容器

## 11. 建议的上线增强

- 绑定域名并启用 HTTPS（Nginx + 证书）
- 关闭公网 3306/6379
- 定期备份 MySQL 数据卷
- 增加应用监控与日志轮转

