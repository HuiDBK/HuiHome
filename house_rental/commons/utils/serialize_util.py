#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 对象序列化工具模块 }
# @Date: 2022/04/23 21:22
from pydantic import BaseModel
from typing import Union, Dict, List
from tortoise.models import Model


def obj2model(
        data_obj: Union[
            Dict,
            Model,
            List[Dict],
            List[Model]
        ],
        data_model: BaseModel
):
    """
    将数据对象转换成 pydantic的响应模型对象
    :param data_obj: 支持 字典对象, 列表对象
    :param data_model: 转换后数据模型
    :return:
    """

    if isinstance(data_obj, dict):
        # 字典处理
        return data_model(**data_obj)

    if isinstance(data_obj, list):
        return [data_model(**item) for item in data_obj if isinstance(item, dict)]
