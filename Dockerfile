#
FROM python:3.8

# 容器的工作目录
WORKDIR /app

# 复制项目依赖文件到容器中
COPY ./requirements.txt /app/requirements.txt

# 运行容器时执行的命令
RUN pip3 install -i https://mirrors.cloud.tencent.com/pypi/simple --no-cache-dir -r /app/requirements.txt

# 将宿主机项目复制到容器中
COPY . /opt/hui/code/PythonProject/house_rental

# 在容器内部执行的命令
CMD ["uvicorn", "house_rental.server:app", "--host", "127.0.0.1", "--port", "8080"]
