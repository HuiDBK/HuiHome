#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2022/04/05 23:24
from typing import Union, Tuple, Set, Dict, List, Type
from house_rental.models import BaseOrmModel


class BaseManager(object):
    """ 数据库模型 Manager基类 """
    model: Type[BaseOrmModel] = None

    @classmethod
    async def get_with_params(cls, filter_params: dict):
        """"""
        return await cls.model.filter(**filter_params).order_by('id').all()

    @classmethod
    async def create(cls, to_create: Dict) -> BaseOrmModel:
        """
        创建一个
        """
        print(to_create)
        model_obj = await cls.model.create(**to_create)
        return model_obj

    @classmethod
    async def create_or_update(cls, data_item: Dict, model_id=None) -> BaseOrmModel:
        """
        创建或更新一个
        """
        data_item.pop('id', None)
        if model_id:
            # 更新
            model_obj = await cls.get_by_id(model_id)
            model_obj = await model_obj.update_from_dict(data_item)
            await model_obj.save(update_fields=data_item.keys())
            return model_obj
        else:
            # 创建
            return await cls.create(data_item)

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
    ) -> Union[BaseOrmModel, None]:
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
    async def filter_page(
            cls,
            filter_params: Dict = None,
            orderings: List = None,
            offset: int = 0, limit: int = 10
    ):
        """
        分页筛选：条件筛选 + 排序规则 + 条数限制
        默认按照主键id排序, 返回模型列表
        :param filter_params: 分页（且条件）过滤参数
        :param orderings: 排序字段列表
        :param offset: 分页偏移量
        :param limit: 每页数据量
        :return:
        """
        if not orderings:
            orderings = ['id']
        if not filter_params:
            filter_params = {}
        total = await cls.model.filter(**filter_params).count()
        data_list = await cls.model.filter(**filter_params).offset(offset).limit(limit).order_by(*orderings)
        return total, data_list

    @classmethod
    async def filter_values_page(
            cls,
            filter_params: Dict,
            values: List,
            orderings: List = None,
            offset: int = 0, limit: int = 10
    ) -> List[Dict]:
        """
        分页字段筛选：分页筛选 + 自定字段列表
        返属性字典
        """
        if orderings is None:
            orderings = ['id']
        return await cls.model.filter(**filter_params).order_by(*orderings).offset(offset).limit(limit).values(*values)

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
