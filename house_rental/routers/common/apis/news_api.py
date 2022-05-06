#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 系统公告API模块 }
# @Date: 2022/05/06 20:10
from house_rental.commons.responses import success_response
from house_rental.logic.common_logic import news_logic
from house_rental.routers.common.request_models.news_in import NewsListInRequest


async def get_news(request: NewsListInRequest):
    """ 获取系统公告 """
    data = await news_logic.get_news_logic(request)
    return success_response(data)
