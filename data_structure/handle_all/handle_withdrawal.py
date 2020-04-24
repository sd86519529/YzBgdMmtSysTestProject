import json
from common.config_manager import ConfigManager
from common.constants import Constants
from util import send_bug_cd


class HandleWithdrawal(object):
    """提现___用于读取excle时做数据处理,或封装预期结果"""

    @staticmethod
    def public_handle(data, exc_data):
        """回填商户号"""
        if not isinstance(data, dict):
            data = json.loads(exc_data['data'])
        i = data.get('biz_content')
        if i.get('mch_accnt_no') in Constants.SubMerchant.MUCSUB.keys():
            i['mch_accnt_no'] = ConfigManager.get_service(Constants.SubMerchant.MUCSUB[i.get('mch_accnt_no')])
        if i.get('mch_accnt_no') in Constants.SubMerchant.PROFIT.keys():
            i['mch_accnt_no'] = ConfigManager.get_service(Constants.SubMerchant.PROFIT[i.get('mch_accnt_no')])
        if i.get('mch_accnt_no') in Constants.SubMerchant.PREPAY.keys():
            i['mch_accnt_no'] = ConfigManager.get_service(Constants.SubMerchant.PREPAY[i.get('mch_accnt_no')])
        return data

    @staticmethod
    def machaccnt_withdraw_handle(exc_data):
        """请求数据处理"""
        data = exc_data['data']
        data = HandleWithdrawal.public_handle(data, exc_data)
        print('请求data::::>>' + str(data))
        exc_data['data'] = data
        return exc_data

    @staticmethod
    def public_assert(self, html, excepted):
        # 校验请求后的code,msg是否正确
        if excepted.get('code') is not None:
            self.assertEqual(str(html.get('code')), str(excepted['code']),
                             msg='接口请求code %s != %s' % (html.get('code'), excepted['code']))
        if excepted.get('message') is not None:
            if len(excepted.get('message').split('-')) > 1:  # 判断字符串在不在里面
                self.assertIn(excepted['message'][0], html.get('message'),
                              msg='接口请求message: %s 不在 %s 里面' % (excepted['message'], html.get('message')))
            else:
                self.assertEqual(html.get('message'), excepted['message'],
                                 msg='接口请求message: %s != %s' % (html.get('message'), excepted['message']))

    @staticmethod
    def assert_timer_withdraw(self, befor_tuple, after_tuple):
        """校验定时器处理提现数据 type 为true 为预期， flase为实际 结构为 withdraw_status,status,remark,request_num"""
        msg1 = 'withdraw_status预期结果 %s 不等于 withdraw_status实际结果%s'
        msg2 = 'status预期结果 %s 不等于 status实际结果%s'
        msg3 = 'remark预期结果 %s 不等于 remark实际结果%s'
        msg4 = 'request_num预期结果 %s 不等于 request_num实际结果%s'
        self.assertEqual(befor_tuple[0], after_tuple[0][0], msg=msg1)
        self.assertEqual(befor_tuple[1], after_tuple[0][1], msg=msg2)
        self.assertEqual(befor_tuple[2], after_tuple[0][2], msg=msg3)
        self.assertEqual(befor_tuple[3], after_tuple[0][3], msg=msg4)

    @staticmethod
    def assert_withdraw(self, befor_dic, after_dic):
        """拆分比对预期结果json和实际结果json"""
        # 比对depository_amt 对比存管户的账面余额
        if not befor_dic.get('depository_amt') is None:
            befor_depository_amt = befor_dic['depository_amt']
            after_depository_amt = after_dic['depository_amt']
            msg = '预期结果：存管户账面余额%s 不等于 实际结果：存管户账面余额%s' % (befor_depository_amt, after_depository_amt)
            self.assertEqual(befor_depository_amt, after_depository_amt, msg=msg)
        # 比对提现账户账面余额和可结算余额
        if not befor_dic.get('mch_amt') is None:
            befor_mch_amt = befor_dic['mch_amt'][0]
            after_mch_amt = after_dic['mch_amt'][0]
            befor_set_amt = befor_dic['mch_amt'][1]
            after_set_amt = after_dic['mch_amt'][1]
            msg_0 = '预期结果：提现账户账面余额%s 不等于 实际结果：提现账户账面余额%s' % (befor_mch_amt, after_mch_amt)
            msg_1 = '预期结果：提现账户可结算余额余额%s 不等于 实际结果：提现账户可结算余额%s' % (befor_set_amt, after_set_amt)
            self.assertEqual(befor_mch_amt, after_mch_amt, msg=msg_0)
            self.assertEqual(befor_set_amt, after_set_amt, msg=msg_1)
        if not befor_dic.get('profit_amt') is None:
            befor_profit_amt = befor_dic['profit_amt'][0]
            after_profit_amt = after_dic['profit_amt'][0]
            befor_set_amt = befor_dic['profit_amt'][1]
            after_set_amt = after_dic['profit_amt'][1]
            msg_0 = '预期结果：分润账户账面余额%s 不等于 实际结果：提现账户账面余额%s' % (befor_profit_amt, after_profit_amt)
            msg_1 = '预期结果：分润账户可结算余额余额%s 不等于 实际结果：提现账户可结算余额%s' % (befor_set_amt, after_set_amt)
            self.assertEqual(befor_profit_amt, befor_profit_amt, msg=msg_0)
            self.assertEqual(befor_set_amt, after_set_amt, msg=msg_1)
        if not befor_dic.get('profit') is None:
            befor_prepay_amt = befor_dic['prepay_amt']
            after_prepay_amt = after_dic['prepay_amt']
            msg = '预期结果：准备金余额%s 不等于 实际结果：存管户账面余额%s' % (befor_prepay_amt, after_prepay_amt)
            self.assertEqual(befor_prepay_amt, after_prepay_amt, msg=msg)

        # 比对表中数据条目数
        befor_info_index = befor_dic['info_index']
        after_info_index = after_dic['info_index']
        self.assertDictEqual(befor_info_index, after_info_index, msg='提现明细条目数有误，具体请排查')

    @staticmethod
    def machaccnt_withdraw_assert(self, html, excepted, befor_dic, after_dic, part=Constants.RESULT.FALSE,
                                  put=Constants.RESULT.FALSE):
        if put.__eq__(Constants.RESULT.FALSE):
            HandleWithdrawal.public_assert(self, html, excepted)
            if part.__eq__(Constants.RESULT.TRUE):
                return
            HandleWithdrawal.assert_withdraw(self, befor_dic, after_dic)
        else:
            try:
                HandleWithdrawal.public_assert(self, html, excepted)
                if part.__eq__(Constants.RESULT.TRUE):
                    return
                HandleWithdrawal.assert_withdraw(self, befor_dic, after_dic)
            except Exception as msg:
                severity, module, title, pri, steps, assignedTo = send_bug_cd.data_util(self.after_treatment_data, html,
                                                                                        msg)
                send_bug_cd.send_bug_to_cd(severity=severity, module=module, title=title, pri=pri, steps=steps,
                                           assignedTo=assignedTo)
                raise msg

    @staticmethod
    def timer_withdraw_assert(self, html, excepted, befor_tuple, after_tuple, part=Constants.RESULT.FALSE,
                              put=Constants.RESULT.FALSE):

        if put.__eq__(Constants.RESULT.FALSE):
            HandleWithdrawal.public_assert(self, html, excepted)
            if part.__eq__(Constants.RESULT.TRUE):
                return
            HandleWithdrawal.assert_timer_withdraw(self, befor_tuple, after_tuple)
        else:
            try:
                HandleWithdrawal.public_assert(self, html, excepted)
                if part.__eq__(Constants.RESULT.TRUE):
                    return
                HandleWithdrawal.assert_timer_withdraw(self, befor_tuple, after_tuple)
            except Exception as msg:
                severity, module, title, pri, steps, assignedTo = send_bug_cd.data_util(self.after_treatment_data, html,
                                                                                        msg)
                send_bug_cd.send_bug_to_cd(severity=severity, module=module, title=title, pri=pri, steps=steps,
                                           assignedTo=assignedTo)
                raise msg
