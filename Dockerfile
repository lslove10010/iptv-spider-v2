# 使用官方 Python 轻量镜像
FROM python:3.9-slim

WORKDIR /app

# 复制依赖并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY main.py .
# 复制前端代码 (在这个简单的例子中，我们将前端作为静态文件由后端稍后集成，或者直接本地打开)
# 在实际生产中，你会用 Nginx 容器来 serve index.html

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]