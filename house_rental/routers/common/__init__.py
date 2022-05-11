#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 公共路由模块 }
# @Date: 2022/05/04 22:40
from fastapi import APIRouter
from .apis import upload_api, areas_api, news_api, enum_api
from .response_models import upload_out, areas_out, news_out
from ...commons.responses.response_model import SuccessModel

router = APIRouter()

router.add_api_route(
    '/upload',
    upload_api.upload_file,
    methods=['post'],
    response_model=upload_out.UploadFileOut,
    summary='单文件上传'
)

router.add_api_route(
    '/upload/batch',
    upload_api.batch_upload_file,
    methods=['post'],
    response_model=upload_out.BatchUploadFileOut,
    summary='多文件上传'
)

router.add_api_route(
    '/areas',
    areas_api.get_areas_info,
    methods=['get'],
    response_model=areas_out.AreasOut,
    summary='获取省市区数据'
)


router.add_api_route(
    '/news',
    news_api.get_news,
    methods=['post'],
    response_model=news_out.NewsListOut,
    summary='获取系统公告信息'
)

router.add_api_route(
    '/error_enums',
    enum_api.get_error_enum,
    methods=['get'],
    response_model=SuccessModel,
    summary='获取系统错误码信息'
)

