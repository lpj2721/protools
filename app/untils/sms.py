#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/6/30 17:39
"""
# from aliyunsdkcore.client import AcsClient
# from app.bin.aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
import uuid
from app.conf.config import R_SMS
from framework.utils import logging
import top


# REGION = "cn-shenzhen"
# acs_client = AcsClient(R_SMS['ACCESS_KEY_ID'], R_SMS['ACCESS_KEY_SECRET'], REGION)
#
#
# def send_sms(business_id, phone_number, template_param=None):
#     logging.info('fun_input: [business:%2s, phone_number:%2s, template_param:%2s]', business_id, phone_number, template_param)
#     sms_request = SendSmsRequest.SendSmsRequest()
#     # 申请的短信模板编码,必填
#     sms_request.set_TemplateCode(R_SMS['template_code'])
#     # 短信模板变量参数
#     if template_param is not None:
#         sms_request.set_TemplateParam(template_param)
#     # 设置业务请求流水号，必填。
#         sms_request.set_OutId(business_id)
#     # 短信签名
#         sms_request.set_SignName(R_SMS['sign_name'])
#     # 短信发送的号码，必填。支持以逗号分隔的形式进行批量调用，批量上限为20个手机号码,批量调用相对于单条调用及时性稍有延迟,验证码类型的短信推荐使用单条调用的方式
#         sms_request.set_PhoneNumbers(phone_number)
#     # 发送请求
#     sms_response = acs_client.do_action_with_exception(sms_request)
#     logging.info('fun_out: [sms_response: %2s]', sms_response)
#     return sms_response


def send_sms_dy(__business_id,phone_number,template_param):
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo("23540144", "7236df0084d8eb061a0d2e3bef85b71d"))
    req.extend = __business_id
    req.sms_type = "normal"
    req.sms_free_sign_name = "中绿平台"
    req.sms_param = template_param
    req.rec_num = phone_number
    req.sms_template_code = "SMS_32580051"
    try:
        resp = req.getResponse()
        print resp
        logging.info('fun_out: [sms_response: %2s]', resp)
        if resp['alibaba_aliqin_fc_sms_num_send_response']['result']['err_code']=="0":
            return True
    except Exception, e:
        logging.info('fun_out: [sms_response: %2s]', e)
# if __name__ == '__main__':
#
#     __business_id = uuid.uuid1()
#     print __business_id
#     params = "{\"num\":\"12345\"}"
#     print send_sms_dy(__business_id, "13247780947", params)


