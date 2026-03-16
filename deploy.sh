#!/bin/bash

echo "🚀 开始部署记账小助手服务..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down

# 构建镜像
echo "🔨 构建Docker镜像..."
docker-compose build

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."

# 检查MySQL
if docker ps | grep -q jizhang_mysql; then
    echo "✅ MySQL服务运行正常"
else
    echo "❌ MySQL服务启动失败"
    docker-compose logs mysql
fi

# 检查Redis
if docker ps | grep -q jizhang_redis; then
    echo "✅ Redis服务运行正常"
else
    echo "❌ Redis服务启动失败"
    docker-compose logs redis
fi

# 检查后端
if docker ps | grep -q jizhang_backend; then
    echo "✅ 后端服务运行正常"
else
    echo "❌ 后端服务启动失败"
    docker-compose logs backend
fi

# 检查前端
if docker ps | grep -q jizhang_frontend; then
    echo "✅ 前端服务运行正常"
else
    echo "❌ 前端服务启动失败"
    docker-compose logs frontend
fi

# 测试API连接
echo "🧪 测试API连接..."
sleep 5

if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ API健康检查通过"
else
    echo "❌ API健康检查失败"
fi

# 测试前端访问
echo "🌐 测试前端访问..."
if curl -s http://localhost/ > /dev/null; then
    echo "✅ 前端访问正常"
else
    echo "❌ 前端访问失败"
fi

echo ""
echo "🎉 部署完成！"
echo ""
echo "📋 服务信息："
echo "   - 后端API: http://localhost:8000"
echo "   - API文档: http://localhost:8000/docs"
echo "   - 前端页面: http://localhost"
echo "   - 健康检查: http://localhost:8000/health"
echo ""
echo "📝 查看日志："
echo "   docker-compose logs -f [服务名]"
echo ""
echo "🛑 停止服务："
echo "   docker-compose down"
echo ""
echo "🔄 重启服务："
echo "   docker-compose restart [服务名]"