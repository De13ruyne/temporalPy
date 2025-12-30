# 基础镜像：Python3.9（与项目要求一致，slim版轻量无冗余）
FROM python:3.9-slim

# 设置工作目录（容器内）
WORKDIR /app

# 设置环境变量：解决Python编码问题 + 禁用缓冲（日志实时输出）
ENV PYTHONUTF8=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 复制依赖清单，安装所有Python包（优先安装，利用Docker缓存）
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制项目所有代码到容器工作目录
COPY . .

# 容器健康检查（可选，验证Python环境）
# HEALTHCHECK --interval=10s --timeout=3s CMD python -c "import temporalio, fastapi" || exit 1