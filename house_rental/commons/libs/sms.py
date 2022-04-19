#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 发送短信验证码模块 }
# @Date: 2022/04/18 22:54
import json
import random
from ronglian_sms_sdk import SmsSDK
from house_rental.commons import settings


def generate_sms_code():
    """
    随机生成6位短信验证码
    :return: sms_code
    """
    # 随机6位短信验证码
    sms_code = random.randint(100000, 999999)
    sms_code = list(str(sms_code))
    random.shuffle(sms_code)
    sms_code = ''.join(sms_code)
    return sms_code


async def send_sms_code_message(
        sms_tips: tuple,
        sms_template_id: str = settings.sms_template_id,
        receive_mobile: str = settings.test_mobile
):
    """
    发送短信验证码
    :param sms_tips: 验证码提示信息 eg: (验证码, 有效期) 有效期单位是分钟
    :param sms_template_id: 短信模板id
    :param receive_mobile: 接受的手机号
    :return:
    """
    sdk = SmsSDK(settings.accId, settings.accToken, settings.appId)
    sms_resp_json_str = sdk.sendMessage(sms_template_id, receive_mobile, sms_tips)
    sms_resp_dict = json.loads(sms_resp_json_str)
    print(sms_resp_dict)
    if sms_resp_dict.get('statusCode') == '000000':
        # 发送成功
        return True
    else:
        return False


def main():
    sms_code = generate_sms_code()
    sms_tips = (sms_code, settings.sms_code_ttl)
    send_sms_code_message(sms_tips)


if __name__ == '__main__':
    main()
