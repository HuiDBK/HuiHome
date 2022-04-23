#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 文件上传逻辑模块 }
# @Date: 2022/04/24 6:26
from typing import List

from fastapi import UploadFile
from house_rental.commons import settings

from house_rental.commons.libs import qiniu_tools
from house_rental.routers.upload.response_models import UploadFileDataItem, BatchUploadDataItem


async def upload_file_logic(file: UploadFile) -> UploadFileDataItem:
    """ 单文件上传逻辑 """
    # 把文件上传到七牛云
    file_data = await file.read()
    file_key = await qiniu_tools.upload_image_to_qiniu(file_data)
    file_url = settings.QINIU_DOMAIN + file_key
    return UploadFileDataItem(file_name=file.filename, file_key=file_key, file_url=file_url)


async def batch_upload_file_logic(files: List[UploadFile]):
    """ 批量上传文件逻辑 """
    file_list = [await upload_file_logic(file) for file in files]
    return BatchUploadDataItem(file_list=file_list)
