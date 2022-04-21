#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 七牛云工具模块 }
# @Date: 2022/04/21 11:41
from house_rental.commons import settings
from qiniu import Auth, put_data


async def upload_image_to_qiniu(file_data: bytes):
    """
    上传图片到七牛
    :param file_data: bytes 文件
    :return: file_name
    """
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = settings.QINIU_BUCKET_NAME

    # 上传到七牛后保存的文件名
    # key = 'my-python-七牛.png'
    key = None

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, expires=1800)

    # # 要上传文件的本地路径
    # localfile = '/Users/jemy/Documents/qiniu.png'

    # ret, info = put_file(token, key, localfile)
    ret, info = put_data(token, key, file_data)
    return ret['key']


def main():
    with open('./test.jpg', mode='rb') as file:
        file_bytes = file.read()
        upload_image_to_qiniu(file_bytes)


if __name__ == '__main__':
    main()
