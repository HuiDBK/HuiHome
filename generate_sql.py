#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 添加房源sql }
# @Date: 2022/08/21 14:50
import random
from datetime import datetime


def generate_house_info_sql():
    """ 生成房源信息sql """
    house_images = [
        "FnZJhJXNddHxPbcBMIE73pB0erkP",
        "FtU-JKqX84HhUmMHK_ue2U_KQNwM",
        "FvLjpo0LBx6Chq9BmuN1g22_ywEs",
        "FvtzSIianax0DXPy_RS0FQ3QQR69",
        "FqqhynG-otP9-m1Y7Dg7yAhXTlFG",
        "FpEpFGIfCWpE62fqTf9eTWyHJNRP",
        "FnkSiv3FujlLU7oYExrleHSKGIim",
        "FhNX_kjrCY0j4MBVZynJUrxfoSzV",
        "FpEpFGIfCWpE62fqTf9eTWyHJNRP",
        "FpEpFGIfCWpE62fqTf9eTWyHJNRP",
        "FpEpFGIfCWpE62fqTf9eTWyHJNRP",
        "FpEpFGIfCWpE62fqTf9eTWyHJNRP",
        "FjgWG5_EGYxJv3yulCHjXrXIH9iK",
        "FqqhynG-otP9-m1Y7Dg7yAhXTlFG",
    ]
    start_id, end_id = 311, 321
    house_info = dict(
        title="'整租-整租鼓楼区-2室1厅'",
        house_desc="'整租-整租鼓楼区-2室1厅'",
        city="'福建省福州市'",
        district="'鼓楼区'",
        address="'福建省福州市鼓楼区鼓东街道'",
    )
    house_info_sql = """
        INSERT
        INTO
        `house_rental`.`house_info`
        (`id`, `rent_type`, `house_type`, `title`, `index_img`, `house_desc`, `city`, `district`, `address`, `rent_state`, `rent_money`, `bargain_money`, `rent_time_unit`, `water_rent`, `electricity_rent`, `strata_fee`, `deposit_ratio`, `pay_ratio`, `bedroom_num`, `living_room_num`, `kitchen_num`, `toilet_num`, `area`, `publish_time`, `state`, `json_extend`, `create_time`, `update_time`, `house_owner`)
        VALUES(
            {house_id},
            'whole',
            'department',
            {title},
            {index_img},
            {house_desc},
            {city},
            {district},
            {address},
            'not_rent',
            {rent_money},
            {bargain_money},
            'month',
             900, 60, 12000, 2, 1, 2, 1, 1, 1, 5000,
            {publish_time}, 'up', NULL, {create_time}, {update_time}, 7);"""

    house_detail_sql = """
        INSERT INTO `house_rental`.`house_detail`
        (`id`, `house_id`, `house_owner`, `contact_id`, `address`, `room_num`, `display_content`, `floor`, `max_floor`, `has_elevator`, `build_year`, `direction`, `lighting`, `near_traffic_json`, `certificate_no`, `location_info`, `json_extend`, `create_time`, `update_time`)
        VALUES(
        {house_detail_id},
        {house_id},
        6,
        6,
        {address},
        {room_num},
        {display_content},
        {floor}, '12', NULL, {build_year}, 'south', NULL, NULL, NULL,
        {location_info},
        {json_extend},
        {create_time}, {update_time});"""

    room_nums = [103, 106, 109, 203, 303, 306, 309, 505, 506, 508, 603, 606, 608, 703, 708, 808, 903]
    for house_id in range(start_id, end_id):
        house_info["house_id"] = house_id
        house_info["house_detail_id"] = house_id
        house_info["room_num"] = random.choice(room_nums)
        house_info["floor"] = f"'{random.randint(1, 13)}'"
        house_info["build_year"] = random.randint(2000, 2022)
        house_info["location_info"] = "'{\"nl\": \"113.35\", \"sl\": \"23.12\"}'"
        house_info[
            "display_content"] = "'{\"images\": [\"FrimFzoDXH9BZiAZ4WlY8c_81xVr\", \"FkPDgiHBNIexUNIgpa6GMrJulRRx\", \"FvHqy_ju-L3GUNF3IAm_GRnqfZRG\", \"FifMTTByOKHA9RuwnOafVrtOI5oE\", \"FkWgRTvIPT0SOMpJzVYHTI_Kp2KH\", \"FshE7rxI-u70GljybpCMYw_0UEMn\", \"Fmj62aiuEDDQuhHJVaUkXPHAZynb\", \"FkJDkoaNAgQ4yl6tsMeozbXFT0Et\"]}'"
        house_info[
            "json_extend"] = "'{\"contact_info\": {\"email\": \"huidbk@163.com\", \"mobile\": 13022331753, \"real_name\": \"汪仙身\"}}'"
        house_info["index_img"] = f"'{random.choice(house_images)}'"
        rent_money = random.randint(5, 10) * 10000
        house_info["rent_money"] = rent_money
        house_info["bargain_money"] = rent_money // 2
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur_time = f"'{cur_time}'"
        house_info["publish_time"] = cur_time
        house_info["create_time"] = cur_time
        house_info["update_time"] = cur_time
        house_info_new_sql = house_info_sql.format(**house_info)
        house_detail_new_sql = house_detail_sql.format(**house_info)
        print(house_info_new_sql)
        print(house_detail_new_sql)


def generate_house_facility_mapping_sql():
    """ 生成房源设施映射sql """
    house_facility_mapping_sql = """
    INSERT
    INTO
    `house_rental`.
    `house_facility_mapping`(`house_id`, `facility_id`, `create_time`, `update_time`)
    VALUES
    ({house_id}, 1, {create_time}, {update_time}),
    ({house_id}, 2, {create_time}, {update_time}),
    ({house_id}, 3, {create_time}, {update_time}),
    ({house_id}, 4, {create_time}, {update_time}),
    ({house_id}, 5, {create_time}, {update_time}),
    ({house_id}, 6, {create_time}, {update_time});
    """
    for house_id in range(113, 302):
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur_time = f"'{cur_time}'"
        house_facility_info = dict(
            house_id=house_id,
            create_time=cur_time,
            update_time=cur_time
        )
        house_facility_mapping_add_sql = house_facility_mapping_sql.format(**house_facility_info)
        print(house_facility_mapping_add_sql)


def main():
    generate_house_info_sql()

    generate_house_facility_mapping_sql()


if __name__ == '__main__':
    main()
