from common.ftp_connect import FtpConnect
from common.request_base import RequestBase
from common.constants import Constants
from data_structure.precodition_all.precondition_dowload_statement import PreconditionDowStatement


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

    def dlb_in_transit_data(self):
        """
        cib制造在途数据的方法 对不平
        """
        self.__init_data(button='dlb')

    def yl_in_transit_data(self):
        """
        yl制造在途数据方法 对不平
        :return:
        """
        self.__init_data(button='yl')

    def qq_in_transit_data(self):
        """
        yl制造在途数据方法 对不平
        :return:
        """
        self.__init_data(button='qq')

    def zfb_in_transit_true_data(self):
        """
        支付宝对平数据产生
        :return:
        """
        self.__init_true_data()

    def creat_settle_data(self, channel='zfb'):
        """传入不同的channel"""
        kwargs = {'zfb': [Constants.CHANNEL.zfb, 'zfb', Constants.RECONCILIATION.true_zfb_path]}
        CreatReconciliation().zfb_in_transit_true_data()  # 制造对平的在途数据
        path_name = FtpConnect().push_file_csv_on_ftp(kwargs[channel][2])
        PreconditionDowStatement.creat_download_info(kwargs[channel][0], path_name, '20200519', kwargs[channel][1])
        PreconditionDowStatement.statement_analyze_send()
        PreconditionDowStatement.recondition()

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

        button_list = ['zfb','cib','dlb','yl','qq']

        for button in button_list:
            if button == 'zfb':
                data_creat_pay_true_list = Constants.CREATE().get_creat_pay_true_list()
                data_creat_refund_true_list = Constants.CREATE().get_creat_refund_true_list()
                data_creat_dispatch_true_list = Constants.CREATE().get_creat_dispatch_true_list()
                data_creat_dispatch_refund_true_list = Constants.CREATE().get_creat_dispatch_refund_true_list()

            elif button == 'cib':
                data_creat_pay_true_list = Constants.CREATE().get_creat_pay_true_list()
                data_creat_refund_true_list = Constants.CREATE().get_creat_refund_true_list()
                data_creat_dispatch_true_list = Constants.CREATE().get_creat_dispatch_true_list()
                data_creat_dispatch_refund_true_list = Constants.CREATE().get_creat_dispatch_refund_true_list()

                self.__u_t(data_creat_pay_true_list, key='20692')
                self.__u_t(data_creat_refund_true_list, key='20692')
                self.__u_t(data_creat_dispatch_true_list, key='20692')
                self.__u_t(data_creat_dispatch_refund_true_list, key='20692')
            elif button == 'dlb':
                data_creat_pay_true_list = Constants.CREATE().get_creat_pay_true_list()
                data_creat_refund_true_list = Constants.CREATE().get_creat_refund_true_list()
                data_creat_dispatch_true_list = Constants.CREATE().get_creat_dispatch_true_list()
                data_creat_dispatch_refund_true_list = Constants.CREATE().get_creat_dispatch_refund_true_list()

                self.__u_t(data_creat_pay_true_list, key='2091')
                self.__u_t(data_creat_refund_true_list, key='2091')
                self.__u_t(data_creat_dispatch_true_list, key='2091')
                self.__u_t(data_creat_dispatch_refund_true_list, key='2091')

            elif button == 'yl':
                data_creat_pay_true_list = Constants.CREATE().get_creat_pay_true_list()
                data_creat_refund_true_list = Constants.CREATE().get_creat_refund_true_list()
                data_creat_dispatch_true_list = Constants.CREATE().get_creat_dispatch_true_list()
                data_creat_dispatch_refund_true_list = Constants.CREATE().get_creat_dispatch_refund_true_list()

                self.__u_t(data_creat_pay_true_list, key='2056')
                self.__u_t(data_creat_refund_true_list, key='2056')
                self.__u_t(data_creat_dispatch_true_list, key='2056')
                self.__u_t(data_creat_dispatch_refund_true_list, key='2056')

            elif button == 'qq':
                data_creat_pay_true_list = Constants.CREATE().get_creat_pay_true_list()
                data_creat_refund_true_list = Constants.CREATE().get_creat_refund_true_list()
                data_creat_dispatch_true_list = Constants.CREATE().get_creat_dispatch_true_list()
                data_creat_dispatch_refund_true_list = Constants.CREATE().get_creat_dispatch_refund_true_list()

                self.__u_t(data_creat_pay_true_list, key='20061')
                self.__u_t(data_creat_refund_true_list, key='20061')
                self.__u_t(data_creat_dispatch_true_list, key='20061')
                self.__u_t(data_creat_dispatch_refund_true_list, key='20061')

            else:
                data_creat_pay_true_list = ''
                data_creat_refund_true_list = ''
                data_creat_dispatch_true_list = ''
                data_creat_dispatch_refund_true_list = ''

            for i in data_creat_pay_true_list:
                data = self.zfb_pay_data(i, refund=False)
                RequestBase.send_request(**data)

            for i in data_creat_refund_true_list:
                data = self.zfb_pay_data(i, refund=True)
                RequestBase.send_request(**data)

            for i in data_creat_dispatch_true_list:
                data = self.diapatch_data(i, refund=False)
                RequestBase.send_request(**data)

            for i in data_creat_dispatch_refund_true_list:
                data = self.diapatch_data(i, refund=True)
                RequestBase.send_request(**data)

    def __u_t(self, lis, key):
        for d in lis:
            for x in range(len(d)):
                if d[x] == '20251':
                    d[x] = key
                # todo:流水号，订单号未处理
                if 'jinweiceshis' in d[x]:
                    d[x] = d[x] + key
                elif 'refundtransno' in d[x]:
                    d[x] = d[x] + key
                if isinstance(d[x], list):
                    for y in d[x]:
                        y[-1] = y[-1] + key
                elif 'test' in d[x]:
                    d[x] = d[x] + key

    def __init_data(self, button):
        """支付记账,退款data"""
        if button == 'zfb':
            data_list = Constants.CREATE.zfb_pay
            data_refund_list = Constants.CREATE.zfb_refund
        elif button == 'cib':
            data_list = Constants.CREATE.zfb_pay
            data_refund_list = Constants.CREATE.zfb_refund
            self.__u_t(data_list, key='20692')
            self.__u_t(data_refund_list, key='20692')
        elif button == 'dlb':
            data_list = Constants.CREATE.zfb_pay
            data_refund_list = Constants.CREATE.zfb_refund
            self.__u_t(data_list, key='2091')
            self.__u_t(data_refund_list, key='2091')
        elif button == 'yl':
            data_list = Constants.CREATE.zfb_pay
            data_refund_list = Constants.CREATE.zfb_refund
            self.__u_t(data_list, key='2056')
            self.__u_t(data_refund_list, key='2056')
        elif button == 'qq':
            data_list = Constants.CREATE.zfb_pay
            data_refund_list = Constants.CREATE.zfb_refund
            self.__u_t(data_list, key='20061')
            self.__u_t(data_refund_list, key='20061')
        else:
            data_list = Constants.CREATE.zfb_pay
            data_refund_list = Constants.CREATE.zfb_refund
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

    @staticmethod
    def get_dispatch_data():
        """构造分账的请求接口"""
        data = {"请求类型": '',
                "data": {"mch_no": "MH20181229115220NBUu",
                         "out_trans_no": "ZZ20200604155127",
                         "biz_type": "mchaccnt.dispatch",
                         "biz_content": {
                             "split_accnt_detail": [
                                 {"mch_accnt_no": "T0020181229184441000000", "amount": "1000", "dispatch_event": "pay",
                                  "dispatch_type": "1", "order_no": "DD120200604155127",
                                  "trans_no": "JY120200604155127", "refund_trans_no": "",
                                  "trans_time": "2020-06-04 15:51:27", "card_no": "", "promotion_type": "",
                                  "promotion_amt": "", "business_type": "", "charge_rate": "", "trans_channel": "2051"},
                                 {"mch_accnt_no": "T0020181229115338000002", "amount": "100",
                                  "dispatch_event": "transfer", "dispatch_type": "1", "order_no": "DD220200604155127",
                                  "trans_no": "JY120200604155127", "refund_trans_no": "",
                                  "trans_time": "2020-06-04 15:51:27", "card_no": "", "promotion_type": "",
                                  "promotion_amt": "", "business_type": "", "charge_rate": "", "trans_channel": "2051"},
                                 {"mch_accnt_no": "T0020181229184441000000", "amount": "100",
                                  "dispatch_event": "transfer", "dispatch_type": "2", "order_no": "DD320200604155127",
                                  "trans_no": "JY120200604155127", "refund_trans_no": "",
                                  "trans_time": "2020-06-04 15:51:27", "card_no": "", "promotion_type": "",
                                  "promotion_amt": "", "business_type": "", "charge_rate": "",
                                  "trans_channel": "2051"}]},
                         "sign_type": "MD5",
                         "timestamp": "20200604155127",
                         "request_operation": "1"}}
        return data

    # ["trans_no","refund_trans_no","trans_time","trans_channel",["amount","order_no"]]
    def diapatch_data(self, args, refund=False):
        """处理分账的参数"""
        data = CreatReconciliation.get_dispatch_data()
        order_list = args[4]
        for i in range(0, len(order_list)):
            data['data']['biz_content']['split_accnt_detail'][i]['amount'] = order_list[i][0]
            data['data']['biz_content']['split_accnt_detail'][i]['order_no'] = order_list[i][1]
            data['data']['biz_content']['split_accnt_detail'][i]['trans_channel'] = args[3]
            data['data']['biz_content']['split_accnt_detail'][i]['trans_no'] = args[0]
            data['data']['biz_content']['split_accnt_detail'][i]['trans_time'] = args[2]

        if refund is True:
            for i in range(0, len(order_list)):

                data['data']['biz_content']['split_accnt_detail'][i]['refund_trans_no'] = args[1]
                data['data']['biz_content']['split_accnt_detail'][0]['dispatch_event'] = 'refund'

                data['data']['biz_content']['split_accnt_detail'][0]['dispatch_type'] = '2'
                data['data']['biz_content']['split_accnt_detail'][1]['dispatch_type'] = '2'
                data['data']['biz_content']['split_accnt_detail'][2]['dispatch_type'] = '1'

        return data


if __name__ == '__main__':
    CreatReconciliation().zfb_in_transit_true_data()
