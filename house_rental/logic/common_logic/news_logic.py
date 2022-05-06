#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 系统公告逻辑模块 }
# @Date: 2022/05/06 20:11
from house_rental.commons.utils import serialize_util
from house_rental.commons.utils.decorators import list_page
from house_rental.managers.news_manager import SystemNoticeManager
from house_rental.routers.common.request_models.news_in import NewsListInRequest
from house_rental.routers.common.response_models.news_out import NewsListItem, NewsListDataItem


@list_page
async def get_news_logic(news_item: NewsListInRequest):
    query_params = news_item.query_params.dict() if news_item.query_params else {}
    query_params = {k: v for k, v in query_params.items() if v is not None}
    total, notice_list = await SystemNoticeManager.filter_page(
        filter_params=query_params,
        limit=news_item.limit,
        offset=news_item.offset,
        orderings=news_item.orderings
    )

    notice_list = serialize_util.obj2DataModel(data_obj=notice_list, data_model=NewsListItem)
    return NewsListDataItem(total=total, data_list=notice_list)
