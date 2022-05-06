#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2022/04/23 20:39
from datetime import date
from typing import Optional, List, Union
from pydantic import BaseModel, Field
from house_rental.commons.request_models import ListPageRequestModel

from house_rental.constants.enums import RentType, HouseType, RentState, HouseState, HouseDirectionEnum, \
    RentTimeUnitEnum, HouseElevatorEnum
from house_rental.routers.house.response_models import HouseFacilityListItem, HouseContactDataItem
from house_rental.routers.house.common_models import HouseDisplayContentItem, HouseLocationItem


class HouseListQueryItem(BaseModel):
    """ 房源列表查询参数 """
    house_id: Optional[int] = Field(description='房屋id')
    rent_money_range: Optional[List[int]] = Field(description='月租金范围')
    area_range: Optional[List[int]] = Field(description='房屋面积范围')
    house_owner: Optional[int] = Field(description='房屋拥有者')
    title: Optional[str] = Field(description='房屋标题')
    address: Optional[str] = Field(description='房源地址')
    city: Optional[str] = Field(mdescription='所在城市')

    rent_type: Optional[
        Union[
            List[RentType],
            str
        ]
    ] = Field(description='租赁类型')

    house_type: Optional[
        Union[
            List[HouseType],
            HouseType
        ]
    ] = Field(description='房屋类型')

    state: Optional[
        Union[
            List[HouseState],
            HouseState
        ]
    ] = Field(description='房源状态')

    rent_state: Optional[
        Union[
            List[RentState],
            RentState
        ]
    ] = Field(default=RentState.not_rent, description='房源出租状态')

    area: Optional[int] = Field(gt=0, description='面积')
    bedroom_num: Optional[int] = Field(gt=0, description='卧室数量')
    living_room_num: Optional[int] = Field(ge=0, description='客厅数量')
    kitchen_num: Optional[int] = Field(ge=0, description='厨房数量')
    toilet_num: Optional[int] = Field(ge=0, description='卫生间数量')


class HouseListInRequest(ListPageRequestModel):
    """ 房源列表入参 """
    query_params: Optional[HouseListQueryItem] = Field(default={}, description='房源列表查询参数')


class PublishHouseIn(BaseModel):
    """ 发布房源入参数据 """
    title: str = Field(description='房源标题')
    index_img: Union[str, None] = Field(description='房源首页展示图片')
    address: str = Field(description='房源地址')
    rent_money: int = Field(description='月租金')
    rent_time_unit: RentTimeUnitEnum = Field(default=RentTimeUnitEnum.month, description='租赁时间单位，默认month（月结）')
    water_rent: int = Field(default=0, description='水费 (单位/元)')
    electricity_rent: int = Field(default=0, description='电费 (单位/元)')
    strata_fee: int = Field(default=0, description='管理费 (单位/元)')
    deposit_ratio: int = Field(description='租赁费用的押金倍数 (押几付几)')
    pay_ratio: int = Field(description='租赁费用的支付倍数 (押几付几)')
    rent_type: RentType = Field(description='租赁类型')
    house_type: HouseType = Field(description='房屋类型')
    city: str = Field(description='所在城市')
    district: str = Field(description='所在区县')
    bedroom_num: int = Field(description='卧室数量')
    living_room_num: int = Field(default=0, description='客厅数量')
    house_owner: Union[int, None] = Field(description='房屋拥有者')
    house_desc: Union[str, None] = Field(description='房屋描述')
    area: Union[int, None] = Field(description='房间面积')
    room_num: Union[int, None] = Field(description='房间号')
    toilet_num: Union[int, None] = Field(description='卫生间数量')
    display_content: Union[HouseDisplayContentItem, None] = Field(description='房屋展示内容')
    floor: Union[int, None] = Field(description='房屋所在楼层')
    max_floor: Union[int, None] = Field(description='房屋最大楼层')
    has_elevator: Union[HouseElevatorEnum, None] = Field(description='是否有电梯')
    build_year: Union[date, None] = Field(description='建成年份')
    direction: Union[HouseDirectionEnum, None] = Field(description='房屋朝向')
    near_traffic_json: Union[dict, None] = Field(description='附近交通信息')
    certificate_no: Union[str, None] = Field(max_length=50, description='房产证号')
    location_info: Union[HouseLocationItem, None] = Field(description='房源地理位置信息')
    house_facility_list: List[HouseFacilityListItem] = Field([], description='房源设施数据')
    house_contact_info: Optional[HouseContactDataItem] = Field(description='房源联系人信息')


class HouseFacilityAddIn(BaseModel):
    """ 添加房源设施入参 """
    name: str = Field(description='房屋设施名称')
    icon: Union[str, None] = Field(description='房屋设施图标')


class HouseCollectIn(BaseModel):
    """ 房源收藏入参 """
    user_id: int = Field(description='用户id')
    house_id: int = Field(description='房源id')
