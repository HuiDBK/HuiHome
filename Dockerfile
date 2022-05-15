#
FROM python:3.7

# 容器的工作目录
WORKDIR /opt/hui/code/PythonProject/house_rental

# 复制项目依赖文件到容器中
COPY ./requirements.txt /opt/hui/code/PythonProject/house_rental/requirements.txt

# 运行容器时执行的命令
RUN pip3 install --no-cache-dir --upgrade -r /opt/hui/code/PythonProject/house_rental/requirements.txt

# 将宿主机项目复制到容器中
COPY ./house_rental /opt/hui/code/PythonProject/house_rental

# 在容器内部执行的命令
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "80"]
