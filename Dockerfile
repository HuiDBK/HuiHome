#
FROM python:3.8-alpine

# 容器的工作目录
WORKDIR /opt/hui/code/PythonProject/house_rental

# 复制项目依赖文件到容器中
COPY ./requirements.txt /opt/hui/code/PythonProject/house_rental/requirements.txt

# 运行容器时执行的命令
RUN pip3 install -i http://mirrors.tencentyun.com/pypi/simple --trusted-host mirrors.tencentyun.com --no-cache-dir --upgrade -r /opt/hui/code/PythonProject/house_rental/requirements.txt && pip3 install pyopenssl --upgrade

# 将宿主机项目复制到容器中
COPY . /opt/hui/code/PythonProject/house_rental

# 在容器内部执行的命令
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8080"]
