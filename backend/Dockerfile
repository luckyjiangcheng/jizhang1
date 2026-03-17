FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
    sed -i 's|http://deb.debian.org/debian|https://mirrors.aliyun.com/debian|g; s|http://deb.debian.org/debian-security|https://mirrors.aliyun.com/debian-security|g' /etc/apt/sources.list.d/debian.sources; \
    fi && \
    apt-get -o Acquire::Retries=5 -o Acquire::http::Timeout=30 update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
