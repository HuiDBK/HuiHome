#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 文件上传API模块 }
# @Date: 2022/02/27 21:48
from typing import List

from fastapi import File, UploadFile
from house_rental.logic.upload_logic import upload_logic
from house_rental.commons.responses import success_response


async def upload_file(file: UploadFile = File(..., description='上传的文件')):
    """ 单文件上传 """
    data = await upload_logic.upload_file_logic(file)
    return success_response(data)


async def batch_upload_file(files: List[UploadFile] = File(..., description='文件列表')):
    """ 多文件上传 """
    data = await upload_logic.batch_upload_file_logic(files)
    return success_response(data)
