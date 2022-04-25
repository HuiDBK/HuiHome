#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块响应模型 }
# @Date: 2022/04/11 20:23
from datetime import date
from typing import Union, List, Optional
from pydantic import Field, BaseModel
from house_rental.constants.enums import RentType, HouseType, RentState, HouseState, HouseDirectionEnum
from house_rental.commons.responses.response_model import ResponseBaseModel, ListResponseModel, ListResponseDataModel


class HouseListItem(BaseModel):
    """ 房源列表项信息 """
    house_id: int = Field(description='房源id')
    title: str = Field(description='房源标题')
    index_img: Union[str, None] = Field(description='房源图片')
    address: str = Field(description='房源地址')
    rent_money: int = Field(description='月租金')
    state: HouseState = Field(description='房屋状态')
    rent_type: RentType = Field(description='租赁类型')
    house_type: HouseType = Field(description='房屋类型')
    rent_state: RentState = Field(description='出租状态')
    city: str = Field(description='所在城市')
    bedroom_num: int = Field(description='卧室数量')
    living_room_num: int = Field(default=0, description='客厅数量')


class HomeHouseDataItem(BaseModel):
    """ 首页房源数据信息 """
    whole_house_list: List[HouseListItem] = Field(description='整租房源列表')
    share_house_list: List[HouseListItem] = Field(description='合租房源列表')


class HomeHouseInfoOut(ResponseBaseModel):
    """ 首页房源信息出参 """
    data: HomeHouseDataItem


class HouseListDataItem(ListResponseDataModel):
    """ 房源列表数据 """
    data_list: List[HouseListItem] = Field(description='房源列表数据')


class HouseListOut(ListResponseModel):
    """ 房源列表出参 """
    data: HouseListDataItem


class HouseFacilityListItem(BaseModel):
    """ 房屋设施列表项数据 """
    facility_id: int = Field(description='房屋设施id')
    name: str = Field(description='房屋设施名称')
    icon: Union[str, None] = Field(description='房屋设施图标')


class HouseContactDataItem(BaseModel):
    """ 房源联系人信息 """
    user_id: Optional[int] = Field(description='联系人用户id')
    real_name: Optional[str] = Field(description='联系人姓名')
    mobile: str = Field(description='联系人手机号')
    email: Optional[str] = Field(description='联系人邮箱')


class HouseDetailDataItem(HouseListItem):
    """ 房源详情数据 """
    house_owner: Union[int, None] = Field(description='房屋拥有者')
    contact_id: Union[int, None] = Field(description='房源联系人id')
    house_desc: Union[str, None] = Field(description='房屋描述')
    area: Union[int, None] = Field(description='房间面积')
    room_num: Union[int, None] = Field(description='房间号')
    toilet_num: Union[int, None] = Field(description='卫生间数量')
    display_content: Union[dict, None] = Field(description='房屋展示内容')
    floor: Union[int, None] = Field(description='房屋所在楼层')
    max_floor: Union[int, None] = Field(description='房屋最大楼层')
    has_elevator: Union[bool, None] = Field(description='是否有电梯')
    build_year: Union[date, None] = Field(description='建成年份')
    direction: Union[HouseDirectionEnum, None] = Field(description='房屋朝向')
    near_traffic_json: Union[dict, None] = Field(description='附近交通信息')
    certificate_no: Union[str, None] = Field(max_length=50, description='房产证号')

    house_facility_list: List[HouseFacilityListItem] = Field(description='房源设施数据')
    house_contact_info: Optional[HouseContactDataItem] = Field(description='房源联系人信息')


class HouseDetailOut(ResponseBaseModel):
    """ 房源详情出参 """
    data: HouseDetailDataItem


class HouseFacilitiesDataItem(BaseModel):
    """ 所有房屋设施信息 """
    house_facility_list: List[HouseFacilityListItem] = Field(description='房源设施数据')


class HouseFacilitiesOut(ResponseBaseModel):
    """ 所有房源设施出参 """
    data: HouseFacilitiesDataItem
