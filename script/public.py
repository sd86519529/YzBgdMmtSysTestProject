import hashlib
import json
import time
import requests
import uuid
from common.config_manager import ConfigManager
from common.constants import Constants


def get_url():
    url = ConfigManager.get_service(Constants.HOST.TEST)
    return url


def get_sign(data, time_stamp, token=None):
    """获取请求时需要的sign"""
    if isinstance(data, dict):
        data = json.dumps(data)
    if token is None:
        token = get_token()
    else:
        token = token
    sign = ''.join((data, "&", time_stamp, token))
    sign_md5 = hashlib.md5(sign.encode(encoding='utf-8')).hexdigest()
    return sign_md5


def get_token():
    """token"""
    token = ConfigManager.get_service(Constants.MD5Token.CS)
    return token


def get_mch_no():
    """子商户号"""
    mch_no = ConfigManager.get_service(Constants.Merchant.CS)
    return mch_no


def get_sub_mch(type_mch):
    """
    type 值为以下几种形式
    much_sub = ['mucsub_1','mucsub_2','mucsub_3','mucsub_4'] # 商户子商户
    profit = ['profit_1', 'profit_2']  # 商户分润商户
    prepay = ['prepay_1', 'prepay_2']  # 准备金账户
    """
    sub_mch_no = ConfigManager.get_service(Constants.SubMerchant.MUCSUB[type_mch])
    return sub_mch_no


def get_out_trans_no():
    """外部追踪号"""
    return '225295c2068ae5405cada7edf1670749a6'


def get_strip_id():
    """获取不重复的随机数"""
    strip_id = str(uuid.uuid1()).replace('-', '')[:21]
    return strip_id


def get_time_str():
    """获取年月日字符串"""
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    return timestamp


def get_sign_type():
    return 'MD5'


def public_data(biz_type, **biz_content):
    """构造外部请求"""
    time_stamp = get_time_str()
    data = {'timestamp': time_stamp, 'sign_type': get_sign_type(), 'out_trans_no': get_out_trans_no(),
            'biz_type': biz_type, 'mch_no': get_mch_no(), 'biz_content': biz_content}
    data = json.dumps(data)
    return {'data': data, 'sign': get_sign(data, time_stamp)}


def get_deposit():
    """制造分账数据"""
    pass


if __name__ == '__main__':
    # while True:
    for i in range(20):
        print(get_strip_id())
