#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 对象序列化工具模块 }
# @Date: 2022/04/23 21:22
from pydantic import BaseModel
from typing import Union, Dict, List
from tortoise.models import Model


def obj2DataModel(
        data_obj: Union[
            Dict,
            Model,
            List[Dict],
            List[Model]
        ],
        data_model: BaseModel
) -> Union[BaseModel, List[BaseModel], None]:
    """
    将数据对象转换成 pydantic的响应模型对象, 如果是数据库模型对象则调用to_dict()后递归
    :param data_obj: 支持 字典对象, 列表对象
    :param data_model: 转换后数据模型
    :return:
    """

    if isinstance(data_obj, dict):
        # 字典处理
        return data_model(**data_obj)

    elif isinstance(data_obj, Model):
        # 数据模型对象处理, to_dict()后递归调用
        return obj2DataModel(data_obj.to_dict(), data_model=data_model)

    elif isinstance(data_obj, list):
        # 列表处理
        return [obj2DataModel(item, data_model=data_model) for item in data_obj]

    else:
        print(f'不支持此{data_obj}类型的转换')
    return
