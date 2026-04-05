#!/bin/bash
# ============================================================
# jizhang1 一键重启部署脚本
# 用法: bash restart.sh [选项]
# 选项:
#   -a, --all       完整重启（拉取代码 + 重建所有服务）(默认)
#   -b, --backend   仅重启后端服务
#   -f, --frontend  仅重启前端服务
#   -c, --code      仅拉取最新代码（不重启）
#   -s, --status    查看服务状态
#   -l, --logs      查看后端日志
#   -h, --help      显示帮助信息
# ============================================================

set -e

PROJECT_DIR="/root/jizhang1"
BACKEND_DIR="${PROJECT_DIR}/backend"
FRONTEND_DIR="${PROJECT_DIR}/frontend"
COMPOSE_CMD="docker compose"

echo "============================================="
echo "  jizhang1 一键重启部署工具"
echo "  项目目录: ${PROJECT_DIR}"
echo "============================================="

cd "${BACKEND_DIR}" || { echo "错误: 无法进入 ${BACKEND_DIR}"; exit 1; }

show_status() {
    echo ""
    echo "=== 服务状态 ==="
    ${COMPOSE_CMD} ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

pull_code() {
    echo ""
    echo "=== 拉取最新代码 ==="
    cd "${PROJECT_DIR}"
    git pull origin main
    cd "${BACKEND_DIR}"
}

restart_all() {
    pull_code
    echo ""
    echo "=== 停止并删除旧容器 ==="
    ${COMPOSE_CMD} down
    echo ""
    echo "=== 重新构建并启动所有服务 ==="
    ${COMPOSE_CMD} up -d --build
    echo ""
    show_status
    echo ""
    echo "=== 部署完成，等待服务就绪... ==="
    sleep 5
    check_health
}

restart_backend() {
    pull_code
    echo ""
    echo "=== 重启后端服务 ==="
    ${COMPOSE_CMD} up -d --build backend
    sleep 3
    show_status
    check_health
}

restart_frontend() {
    pull_code
    echo ""
    echo "=== 重启前端服务 ==="
    ${COMPOSE_CMD} up -d --build frontend
    sleep 3
    show_status
}

check_health() {
    echo ""
    echo "=== 健康检查 ==="
    if curl -sf http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo "✅ 后端健康检查通过: http://127.0.0.1:8000/health"
    else
        echo "❌ 后端健康检查失败，请查看日志: docker compose logs -f backend"
        return 1
    fi
    
    if curl -sf http://127.0.0.1:80 > /dev/null 2>&1; then
        echo "✅ 前端访问正常: http://127.0.0.1:80"
    else
        echo "⚠️ 前端可能还在启动中，请稍后重试"
    fi
}

show_logs() {
    echo ""
    echo "=== 后端日志 (Ctrl+C 退出) ==="
    ${COMPOSE_CMD} logs -f --tail 100 backend
}

show_help() {
    cat << 'EOF'

用法: bash restart.sh [选项]

选项:
  -a, --all       完整重启（拉取代码 + 重建所有服务）(默认)
  -b, --backend   仅重启后端服务
  -f, --frontend  仅重启前端服务
  -c, --code      仅拉取最新代码（不重启）
  -s, --status    查看服务状态
  -l, --logs      查看后端日志
  -h, --help      显示帮助信息

示例:
  bash restart.sh                  # 完整重启
  bash restart.sh -b               # 仅重启后端
  bash restart.sh -f               # 仅重启前端
  bash restart.sh -s               # 查看状态
  bash restart.sh -l               # 查看日志

EOF
}

case "${1:-all}" in
    -a|--all|all)          restart_all ;;
    -b|--backend|backend)  restart_backend ;;
    -f|--frontend|frontend) restart_frontend ;;
    -c|--code|code)        pull_code ;;
    -s|--status|status)    show_status ;;
    -l|--logs|logs)        show_logs ;;
    -h|--help|help|*)      show_help ;;
esac

echo ""
echo "============================================="
echo "  操作完成！"
echo "  Web 访问地址: http://10.250.26.182"
echo "  API 地址: http://10.250.26.182:8000"
echo "============================================="
