#!/bin/bash

cd ../

# 创建目录（如果不存在）
mkdir -p /opt/hui/data/mysql/{conf,data,log}
mkdir -p /opt/hui/data/redis/{conf,data,log}
mkdir -p /opt/hui/data/nginx/{conf,data,log}


# 定义源文件路径和目标文件路径
mysql_src_file="conf/mysql.cnf"
mysql_tgt_file="/opt/hui/data/mysql/conf/mysql.cnf"

redis_src_file="conf/redis.conf"
redis_tgt_file="/opt/hui/data/redis/conf/redis.conf"

nginx_src_file="conf/nginx.conf"
nginx_tgt_file="/opt/hui/data/nginx/conf/nginx.conf"

# 将源文件内容写入目标文件
cat "$mysql_src_file" > "$mysql_tgt_file"
cat "$redis_src_file" > "$redis_tgt_file"
cat "$nginx_src_file" > "$nginx_tgt_file"

# 前端文件放到nginx中
cp -r home_front /opt/hui/data/nginx/data

# 启动 Docker Compose
docker-compose up -d
