# 使用官方 Python 镜像作为基础镜像
# 因为GWF的限制,导致我只能从本地下载.
# 然后 limiter 0.5.0的版本需要3.10 而不是3.9
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到容器的工作目录
COPY . .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用运行的端口
EXPOSE 8000

# 运行 Flask 应用
CMD ["python", "main.py"]