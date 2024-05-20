# 使用官方 Python 运行时作为基础镜像
FROM python:3.10-slim

# 更新软件包列表并安装FFmpeg和必要的构建工具
# RUN apt-get update && apt-get install -y ffmpeg gcc

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器中的 /app 目录
COPY . /app

# 安装 requirements.txt 中指定的任何需要的程序包
RUN pip install --no-cache-dir -r requirements.txt

# 使端口 8000 可供此容器外的环境使用
EXPOSE 8000

# 使用 Uvicorn 运行 FastAPI 应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
