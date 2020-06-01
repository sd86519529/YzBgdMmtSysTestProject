from common.request_base import RequestBase
from common.constants import Constants


def zfb_in_transit_data():
    """
    支付宝制造在途数据的方法
    """


def init_data():
    """支付记账data"""
    data_list = [['jinweiceshi_zfb_002', '300', 'test01', '300'], ['jinweiceshi_zfb_003', '28000', 'test02', '28000'],
                 ['jinweiceshi_zfb_004', '320', 'test03', '320'], ['jinweiceshi_zfb_005', '300', 'test04', '300']]
    for i in data_list:
        data = zfb_pay_data(i)
        print(data)
        RequestBase.send_request(**data)


def zfb_pay_data(args):
    data = Constants.PRE_DATA.PAY_DATA
    data['data']['biz_content']['trans_no'] = args[0]  # 'jinweiceshi_zfb_001'
    data['data']['biz_content']['trans_time'] = '2020-05-19 11:33:44'
    data['data']['biz_content']['trans_amt'] = args[1] # '300'
    data['data']['biz_content']['split_accnt_detail'][0]['order_no'] = args[2]  # 'test01'
    data['data']['biz_content']['split_accnt_detail'][0]['amount'] = args[3]  # '300'
    return data


if __name__ == '__main__':
    init_data()
