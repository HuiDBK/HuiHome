#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 公共逻辑模块 }
# @Date: 2022/04/22 15:59
import re
from pydantic import BaseModel
from house_rental.managers.house_manager import HouseInfoManager, HouseDetailManager, HouseFacilityManager
from house_rental.managers.order_manager import OrderManager
from house_rental.managers.template_manager import TemplateManager
from house_rental.managers.user_manager import UserProfileManager, UserBasicManager


def get_list_page_response_data(
        total: int,
        data_list: list,
        offset: int,
        limit: int,
        data_model: BaseModel = None,
):
    """
    获取分页响应数据
    :param total:
    :param data_list:
    :param offset:
    :param limit:
    :param data_model: 数据模型，转换成对应业务数据模型
    :return:
    """
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


class DBManagerFactory(object):
    """ 数据库模型管理者工厂类 """
    USER_BASIC_MANAGER = 'UserBasicManager'
    USER_PROFILE_MANAGER = 'UserProfileManager'
    HOUSE_INFO_MANAGER = 'HouseInfoManager'
    HOUSE_DETAIL_MANAGER = 'HouseDetailManager'
    HOUSE_FACILITY_MANAGER = 'HouseFacilityManager'
    ORDER_MANAGER = 'OrderManager'
    TEMPLATE_MANAGER = 'TemplateManager'

    _db_manager_mapping = {
        'UserBasicManager': UserBasicManager,
        'UserProfileManager': UserProfileManager,
        'HouseInfoManager': HouseInfoManager,
        'HouseDetailManager': HouseDetailManager,
        'HouseFacilityManager': HouseFacilityManager,
        'OrderManager': OrderManager,
        'TemplateManager': TemplateManager,
    }

    # 模型实例对象池
    # key => {db_manager_name}:{model_id}   value => {model_instance}
    _model_instance_pool = dict()

    def __init__(self, db_manager_name):
        self.db_manager_name = db_manager_name

    @property
    def instance(self):
        """ 获取数据库模型管理实例 """
        return self._db_manager_mapping.get(self.db_manager_name)

    async def model_instance(self, model_id):
        """ 获取数据库模型实例 """
        key = f'{self.db_manager_name}:{model_id}'
        model_obj = self._model_instance_pool.get(key)
        if not model_obj:
            # 可能会重复创建相同的实例对象，因此把创建过的对象放到模型实例对象池中
            model_obj = await self.instance.get_by_id(model_id)
            self._model_instance_pool[key] = model_obj
        return model_obj


async def generate_contract_content(order_id: int, template_id=1):
    """
    生成电子合同内容
    :param order_id: 订单id
    :param template_id: 电子合同模板id 默认1
    :return:
    """
    order = await OrderManager.get_by_id(order_id)
    # 订单参数与模型管理器映射
    order_params_mapping = {
        'OrderManager': 'id',
        'UserProfileManager:tenant': 'tenant_id',
        'UserProfileManager:landlord': 'landlord_id',
        'HouseInfoManager': 'house_id'
    }

    # 获取用户（租客、房东）信息、房屋信息
    template_obj = await TemplateManager.get_by_id(template_id)

    # 获取模板的内容和渲染参数
    """
    render_params:{
        外层的key就是渲染的参数
        "landlord_name": { 值为标识数据源在哪
            "db_model_manager": 数据库模型管理者,
            "field_name": 数据库模型对应的字段
            "role": 这个字段是对数据库模型管理者和字段名相同时用于区分是谁的数据
        }
    }
    """
    render_params, template_content = template_obj.render_params, template_obj.template_content
    for render_key, data_src in render_params.items():
        db_manager_name = data_src.get('db_model_manager')
        field_name = data_src.get('field_name')
        role = data_src.get('role')

        # 先通过数据库模型管理器名称和role来获取对应的参数名称
        order_params_key = db_manager_name
        if role:
            order_params_key = f'{db_manager_name}:{role}'
        model_id_name = order_params_mapping.get(order_params_key)

        # 通过参数名称来获取 model_id
        model_id = getattr(order, model_id_name)

        # 再通过 db_manager_name 和 model_id 获取具体数据库模型实例对象
        db_model = await DBManagerFactory(db_manager_name).model_instance(model_id)

        # 最后根据模型实例对象和 field_name 来获取具体的内容
        model_dict = db_model.to_dict()
        render_value = model_dict.get(field_name)
        render_value = str(render_value)

        # 根据渲染key、渲染值与模板内容进行渲染
        render_key_pattern = re.compile(r"{{\s*" + render_key + r"\s*}}")
        render_result = re.sub(render_key_pattern, render_value, str(template_content))
        template_content = render_result

    return template_content
