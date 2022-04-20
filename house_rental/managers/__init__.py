#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2022/04/05 23:24
from typing import Union, Tuple, Set, Dict
from house_rental.models import BaseModel


class BaseManager(object):
    """ 数据库模型 Manager基类 """
    model: BaseModel = None

    @classmethod
    def model_test(cls):
        print(cls)
        print(cls.model)

    @classmethod
    async def get_with_params(cls, filter_params: dict):
        """"""
        return cls.model.filter(**filter_params).order_by('id').all()

    @classmethod
    async def update(cls, model_id: int, to_update: Dict) -> bool:
        """
        更新一个
        """
        # 过滤值为None的情况
        # 1. 表设计时尽量不要使值为None
        # 2. 此处可以兼容更新记录时， Pydantic Model 的非必传字段默认为 None 的情况
        to_update = {
            k: v
            for k, v in to_update.items()
            if v is not None
        }
        if not to_update:
            return False
        obj = await cls.get_by_id(model_id)
        if not obj:
            return False
        try:
            effect_rows = await cls.model.filter(id=model_id).update(
                **to_update)
            if effect_rows == 1:
                print(f"{cls.model.__name__}.update model_id: {model_id} to_update: {to_update}")
                return True
            return False
        except Exception:
            print(f"{cls.model.__name__}.update 更新失败")
            return False

    @classmethod
    async def filter_first(
            cls,
            filter_params: dict,
            orderings: list = None
    ) -> Union[BaseModel, None]:
        """
        首条筛选：条件筛选 + 排序规则 + 取第一个
        """
        if not orderings:
            orderings = ['id']
        return await cls.model.filter(**filter_params).order_by(*orderings).first()

    @classmethod
    async def filter_count(cls, filter_params: dict) -> int:
        """
        Count统计
        """
        return await cls.model.filter(**filter_params).count()

    @classmethod
    async def filter_existed(cls, filter_params: dict) -> bool:
        """
        存在性判断
        """
        return await cls.model.filter(**filter_params).exists()

    @classmethod
    async def get_by_id(cls, model_id):
        """
        主键单个查询
        """
        return await cls.model.filter(pk=model_id).first()

    @classmethod
    def danger_keywords(cls) -> Set:
        """高危操作检测关键字"""
        return {"delete", "drop", "select *"}

    @classmethod
    async def execute_sql(cls, sql: str) -> Tuple:
        """
        执行 sql
        """
        check_res = map(lambda x: x in sql.lower(), cls.danger_keywords())
        if any(list(check_res)):
            raise Exception('sql 危险操作')
        con = cls.model.db_conn()
        res = await con.execute_query(sql)
        return res
