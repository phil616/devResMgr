FROM python:3.9

WORKDIR /app

# 复制代码和依赖（排除 .env）
COPY requirements.txt .
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 声明环境变量（可选，仅为文档说明）
ENV TOKEN_SECRET=$TOKEN_SECRET \
    DB_HOST=$DB_HOST \
    DB_PORT=$DB_PORT \
    DB_USER=$DB_USER \
    DB_PASS=$DB_PASS \
    DB_NAME=$DB_NAME

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000