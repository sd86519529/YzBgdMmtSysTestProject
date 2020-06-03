from common.request_base import RequestBase
from common.constants import Constants


class CreatReconciliation(object):

    def zfb_in_transit_data(self):
        """
        支付宝制造在途数据的方法 对不平
        """
        self.__init_data(button='zfb')

    def cib_in_transit_data(self):
        """
        cib制造在途数据的方法 对不平
        """
        self.__init_data(button='cib')

    def zfb_in_transit_true_data(self):
        """
        支付宝对平数据产生
        :return:
        """
        self.__init_true_data()

    @staticmethod
    def info_assert_kwargs(trans_fee, recon_amt, account_type, info_len, info_list):
        """
        对账预期结果的构造
        trans_fee 手续费总额
        recon_amt 对账单扣除手续费总额
        account_type 是否对平
        info_len 问题件数量
        info_list 问题件列表
        """
        kwargs = {'trans_fee': trans_fee, 'recon_amt': recon_amt, 'account_type': account_type, 'info_len': info_len,
                  'info_list': info_list}
        return kwargs

    @staticmethod
    def get_data():
        data = {"请求类型": '',
                "data": {
                    "biz_content": {"trans_no": "MH20181229115220NBUu", "trans_time": "2020-05-20 17:25:58",
                                    'trans_channel': '20251', 'settle_type': '1', 'trans_amt': '1',
                                    "split_accnt_detail": [
                                        {"order_no": "test10", "amount": 1, "dispatch_event": "pay",
                                         'dispatch_type': '1', "mch_accnt_no": "T0020181229184441000000",
                                         'accnt_amt_before': 1}]},
                    "biz_type": "mchaccnt.pay.dispatch",
                    "out_trans_no": "225295c2068ae5405cada7edf1670749a6", "sign_type": "MD5",
                    "timestamp": "20191028022240", "mch_no": "MH20181229115220NBUu"}}
        return data

    def __init_true_data(self):
        data_list = Constants.CREATE.creat_pay_true_list
        data = self.zfb_pay_data(data_list)
        RequestBase.send_request(**data)

    def __init_data(self, button):
        """支付记账,退款data"""
        if button == 'zfb':
            data_list = Constants.CREATE.zfb_pay
            data_refund_list = Constants.CREATE.zfb_refund
        elif button == 'cib':
            data_list = Constants.CREATE.zfb_pay
            data_refund_list = Constants.CREATE.zfb_refund
            for d in data_list:
                for x in range(len(d)):
                    if d[x] == '20251':
                        d[x] = '20692'
            for d in data_refund_list:
                for x in range(len(d)):
                    if d[x] == '20251':
                        d[x] = '20692'
        else:
            data_list = ''
            data_refund_list = ''
        for i in data_list:
            data = self.zfb_pay_data(i)
            RequestBase.send_request(**data)
        for r in data_refund_list:
            data = self.zfb_pay_data(r, refund=True)
            RequestBase.send_request(**data)

    def zfb_pay_data(self, args, refund=False):
        data = CreatReconciliation.get_data()
        data['data']['biz_content']['trans_channel'] = args[5]
        data['data']['biz_content']['trans_no'] = args[0]  # 'jinweiceshi_zfb_001'
        data['data']['biz_content']['trans_time'] = args[4]
        data['data']['biz_content']['trans_amt'] = args[1]  # '300'
        data['data']['biz_content']['split_accnt_detail'][0]['order_no'] = args[2]  # 'test01'
        data['data']['biz_content']['split_accnt_detail'][0]['amount'] = args[3]  # '300'
        # todo:暂时支持两个pay或者两个refund，可以通过除法生成多个
        if len(args) != 6:
            data['data']['biz_content']['split_accnt_detail'].append(
                {"order_no": "test10", "amount": 1, "dispatch_event": "pay",
                 'dispatch_type': '1', "mch_accnt_no": "T0020181229184441000000",
                 'accnt_amt_before': 1})
            data['data']['biz_content']['split_accnt_detail'][1]['order_no'] = args[6]  # 'test01'
            data['data']['biz_content']['split_accnt_detail'][1]['amount'] = args[7]  # '300'\
        if refund is True:
            data['data']['biz_type'] = 'mchaccnt.refund.dispatch'
            data['data']['biz_content']['refund_trans_no'] = args[0]
            for g in data['data']['biz_content']['split_accnt_detail']:
                g['dispatch_event'] = 'refund'
                g['dispatch_type'] = '2'
        return data


if __name__ == '__main__':
    CreatReconciliation().cil_in_transit_data()
