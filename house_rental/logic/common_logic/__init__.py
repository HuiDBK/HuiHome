#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 公共逻辑模块 }
# @Date: 2022/04/22 15:59
from pydantic import BaseModel


def get_list_page_response_data(
        data_list: list,
        offset: int,
        limit: int,
        data_model: BaseModel = None,
):
    """
    获取分页响应数据
    :param data_list:
    :param offset:
    :param limit:
    :param data_model: 数据模型，转换成对应业务数据模型
    :return:
    """
    total = len(data_list)
    next_offset = offset + limit
    if data_model and issubclass(data_model, BaseModel):
        data_list = [data_model(**item) for item in data_list]
    response_data = dict(
        total=total,
        data_list=data_list,
        has_more=True if total > next_offset else False,
        next_offset=next_offset,
    )
    return response_data
