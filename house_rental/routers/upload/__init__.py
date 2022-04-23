#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 文件上传模块路由 }
# @Date: 2022/02/27 21:43
from fastapi import APIRouter
from .apis import upload_api
from .response_models import upload_out

router = APIRouter()

router.add_api_route(
    '/',
    upload_api.upload_file,
    methods=['post'],
    response_model=upload_out.UploadFileOut,
    summary='单文件上传'
)

router.add_api_route(
    '/batch',
    upload_api.batch_upload_file,
    methods=['post'],
    response_model=upload_out.BatchUploadFileOut,
    summary='多文件上传'
)
