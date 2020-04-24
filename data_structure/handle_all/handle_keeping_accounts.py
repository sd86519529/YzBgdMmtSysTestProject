import json
import copy
from common.base import Base
from common.config_manager import ConfigManager
from common.constants import Constants
from util import send_bug_cd


class HandleKeepingAccounts(object):
    """记账___用于读取excle时做数据处理,或封装预期结果"""

    @staticmethod
    def public_handle(data, exc_data):
        """回填商户号"""
        if not isinstance(data, dict):
            data = json.loads(exc_data['data'])
        for i in data.get('biz_content').get('split_accnt_detail'):
            if i.get('mch_accnt_no') in Constants.SubMerchant.MUCSUB.keys():
                i['mch_accnt_no'] = ConfigManager.get_service(Constants.SubMerchant.MUCSUB[i.get('mch_accnt_no')])
            if i.get('mch_accnt_no') in Constants.SubMerchant.PROFIT.keys():
                i['mch_accnt_no'] = ConfigManager.get_service(Constants.SubMerchant.PROFIT[i.get('mch_accnt_no')])
            if i.get('mch_accnt_no') in Constants.SubMerchant.PREPAY.keys():
                i['mch_accnt_no'] = ConfigManager.get_service(Constants.SubMerchant.PREPAY[i.get('mch_accnt_no')])
        return data

    @staticmethod
    def machaccnt_pay_dispatch_handle(exc_data):
        """请求数据处理"""
        data = exc_data['data']
        data = HandleKeepingAccounts.public_handle(data, exc_data)
        print('请求data::::>>' + str(data))
        exc_data['data'] = data
        return exc_data

    @staticmethod
    def machaccnt_pay_channel_rate_common(exc_data):
        """
        含有手续费的handle处理  exc_data 是给构造预期结果用 copy是给请求用
        回填 计算手续费后的金额
        """
        copy_exc_data = copy.deepcopy(exc_data)
        comparison_muc_sub_list = []
        for key, value in Constants.SubMerchant.MUCSUB.items():
            comparison_muc_sub_list.append(ConfigManager.get_service(value))
        data = copy_exc_data['data']
        if not isinstance(data, dict):
            data = json.loads(copy_exc_data['data'])
        trans_amt = data.get('biz_content').get('trans_amt')
        for i in data.get('biz_content').get('split_accnt_detail'):
            if i.get('mch_accnt_no') in comparison_muc_sub_list:
                new_amount = Base.count_charge(trans_amt, i.get('amount'))
                i['amount'] = new_amount
        copy_exc_data['data'] = HandleKeepingAccounts.public_handle(data, copy_exc_data)
        return copy_exc_data

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
    def mch_amt_assert(self, mch_ant_after, mch_ant_bef, mach_pay_up_obj, button='pay'):
        """不同子商户在请求前和请求后的金额变化"""
        # 校验各个子商户金额变化正确
        if button.__eq__('pay'):
            for key, value in mch_ant_after.items():
                self.assertEqual(int(value[0][0]) - int(mch_ant_bef[key][0][0]),
                                 int(mach_pay_up_obj.trans_amt_dict[key]),
                                 msg='子商户号为:%s的商户，对比子商户金额时 请求后的金额：%s -  请求前的金额 %s 不等于 预期金额：%s' % (
                                     key, value[0][0], mch_ant_bef[key][0][0], mach_pay_up_obj.trans_amt_dict[key]))
        else:
            for key, value in mch_ant_after.items():
                self.assertEqual(int(value[0][0]) - int(mch_ant_bef[key][0][0]),
                                 -int(mach_pay_up_obj.trans_amt_dict[key]),
                                 msg='子商户号为:%s的商户，对比子商户金额时 请求后的金额：%s -  请求前的金额 %s 不等于 预期金额：%s' % (
                                     key, value[0][0], mch_ant_bef[key][0][0], mach_pay_up_obj.trans_amt_dict[key]))

    @staticmethod
    def mch_sttled_amt(self, settled_ant_aft, settled_ant_bef, mach_pay_up_obj):
        """不同子商户在请求前和请求后可结算金额变化"""
        for key, value in settled_ant_aft.items():
            self.assertEqual(int(value[0][0]) - int(settled_ant_bef[key][0][0]),
                             -(int(mach_pay_up_obj.trans_amt_dict[key])),
                             msg='子商户号为:%s的商户，对比子商户可结算金额时 请求前的金额：%s -  请求后的金额 %s 不等于 预期金额：-%s' % (
                                 key, value[0][0], settled_ant_bef[key][0][0], mach_pay_up_obj.trans_amt_dict[key]))

    @staticmethod
    def mch_promotion_sttled_amt(self, settled_ant_aft, settled_ant_bef, mach_pay_up_obj, button='pay'):
        """准备金账户或子商户在请求前和请求后可结算金额变化"""
        for key, value in settled_ant_aft.items():
            if button.__eq__('pay'):
                if key.__eq__(ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_1'])):
                    self.assertEqual(int(value[0][0]) - int(settled_ant_bef[key][0][0]),
                                     int(mach_pay_up_obj.trans_amt_dict[key]),
                                     msg='准备金账户号为:%s的商户，对比子商户可结算金额时 请求后的金额：%s -  请求前的金额 %s 不等于 预期金额：-%s' % (
                                         key, value[0][0], settled_ant_bef[key][0][0],
                                         mach_pay_up_obj.trans_amt_dict[key]))
                continue
            else:
                if key != ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_1']):
                    self.assertEqual(int(value[0][0]) - int(settled_ant_bef[key][0][0]),
                                     -int(mach_pay_up_obj.trans_amt_dict[key]),
                                     msg='商户账户号为:%s的商户，对比子商户可结算金额时 请求后的金额：%s -  请求前的金额 %s 不等于 预期金额：%s' % (
                                         key, value[0][0], settled_ant_bef[key][0][0],
                                         mach_pay_up_obj.trans_amt_dict[key]))

    @staticmethod
    def amt_dict_assert(self, v, k, amt_info_after, on_way_amt, type):
        """
        比对传入金额和实际记录金额是否正确
        :return:
        """

        for amt_number in range(len(v)):
            # 比对传入金额和实际记录金额是否正确
            if type.__eq__('pay'):
                self.assertEqual(v[amt_number][1], amt_info_after[k][amt_number][0],
                                 msg='%s 表中数金额 %s != %s' % (k, v[amt_number][1], amt_info_after[k][amt_number][0],))
            if type.__eq__('refund'):
                self.assertEqual(v[amt_number][1], -amt_info_after[k][amt_number][0],
                                 msg='%s 表中数金额 %s != %s' % (k, v[amt_number][1], amt_info_after[k][amt_number][0],))
            # 记录在途的金额变化情况
            on_way_amt += v[amt_number][1]
        return on_way_amt

    @staticmethod
    def on_way_amt_assert(self, amt_info_after, on_way_amt, type='pay'):
        # 对比在途表的金额
        on_way_actual_amt = 0
        # 计算实际在途总金额
        for zaitu in amt_info_after[Constants.TableName.HIS_ACCNT_ONWAY]:
            on_way_actual_amt += zaitu[0]
        # 比对预期在途总金额和实际在途总金额是否相等
        if type.__eq__('pay'):
            self.assertEqual(int(on_way_amt) + int(on_way_actual_amt), 0,
                             msg='在途表记录金额出现错误%s != %s' % (int(on_way_amt), int(on_way_actual_amt)))
        if type.__eq__('refund'):
            self.assertEqual(int(on_way_amt) - int(on_way_actual_amt), 0,
                             msg='在途表记录金额出现错误%s != %s' % (int(on_way_amt), int(on_way_actual_amt)))

    @staticmethod
    def has_amt_prepay(self, amt_info_after, mach_pay_up_obj, button='pay'):
        """校验准备金明细是否插入记录"""
        if button.__eq__('pay'):
            self.assertNotEqual(0, len(amt_info_after.get(Constants.TableName.HIS_ACCNT_PREPAY)),
                                msg='准备金明细表中没有插入数据，查出条目数为0')
        else:
            # 若为活动记账退款，则准备金明细表中记录必大于两条
            self.assertGreater(len(amt_info_after.get(Constants.TableName.HIS_ACCNT_PREPAY)), 2)
        for k, v in mach_pay_up_obj.amt_dict.items():
            # 比对不同子商户表的数据条目数是否正确
            # 对比请求之后查询出来的不同子商户条目数是否正确而
            self.assertEqual(len(amt_info_after[k]), len(v),
                             msg='%s 表中数据条目数应为%s,实际只有%s' % (k, len(v), len(amt_info_after[k])))

    @staticmethod
    def all_type_mch_len_amt_assert(self, mach_pay_up_obj, amt_info_after, type):
        """针对记账   所有类型表中的数据数量和准确性比较"""
        # 校验不同子商户表的数量和金额正确
        # 1 校验数据结构保存的条目数在对应表中查询数目正确
        # 2 校验数据金额是否正确
        on_way = 0
        on_way_amt = 0
        for k, v in mach_pay_up_obj.amt_dict.items():
            # 比对不同子商户表的数据条目数是否正确
            # 记录在途的预期结果数量
            on_way = len(v) + on_way
            # 对比请求之后查询出来的不同子商户条目数是否正确而
            self.assertEqual(len(amt_info_after[k]), len(v),
                             msg='%s 表中数据条目数应为%s,实际只有%s' % (k, len(v), len(amt_info_after[k])))
            on_way_amt = HandleKeepingAccounts.amt_dict_assert(self, v, k, amt_info_after, on_way_amt,
                                                               type)  # 对比每张表中的金额
        # 对比在途表是否条目数正确
        self.assertEqual(len(amt_info_after[Constants.TableName.HIS_ACCNT_ONWAY]), on_way,
                         msg='在途表记录条数出现错误%s != %s' % (len(amt_info_after[Constants.TableName.HIS_ACCNT_ONWAY]), on_way))
        HandleKeepingAccounts.on_way_amt_assert(self, amt_info_after, on_way_amt, type)  # 对比在途表中的金额

    @staticmethod
    def machaccnt_pay_dispatch_assert(self, html, excepted, mach_pay_up_obj=None, mch_ant_bef=None, mch_ant_after=None,
                                      amt_info_after=None, part=Constants.RESULT.FALSE, put=Constants.RESULT.FALSE):
        if put.__eq__(Constants.RESULT.FALSE):
            HandleKeepingAccounts.public_assert(self, html, excepted)
            if part.__eq__(Constants.RESULT.TRUE):
                return
            HandleKeepingAccounts.mch_amt_assert(self, mch_ant_after, mch_ant_bef, mach_pay_up_obj, button='pay')
            HandleKeepingAccounts.all_type_mch_len_amt_assert(self, mach_pay_up_obj, amt_info_after, type='pay')
        else:
            try:
                HandleKeepingAccounts.public_assert(self, html, excepted)
                if part.__eq__(Constants.RESULT.TRUE):
                    return
                HandleKeepingAccounts.mch_amt_assert(self, mch_ant_after, mch_ant_bef, mach_pay_up_obj, button='pay')
                HandleKeepingAccounts.all_type_mch_len_amt_assert(self, mach_pay_up_obj, amt_info_after, type='pay')
            except Exception as msg:
                severity, module, title, pri, steps, assignedTo = send_bug_cd.data_util(self.after_treatment_data, html,
                                                                                        msg)
                send_bug_cd.send_bug_to_cd(severity=severity, module=module, title=title, pri=pri, steps=steps,
                                           assignedTo=assignedTo)
                raise msg

    @staticmethod
    def machaccnt_refund_dispatch_assert(self, html, excepted, mach_pay_up_obj=None, mch_ant_bef=None,
                                         mch_ant_after=None, amt_info_after=None, settled_ant_bef=None,
                                         settled_ant_aft=None, part=Constants.RESULT.FALSE,
                                         put=Constants.RESULT.FALSE):
        if put.__eq__(Constants.RESULT.FALSE):
            HandleKeepingAccounts.public_assert(self, html, excepted)
            if part.__eq__(Constants.RESULT.TRUE):
                return
            HandleKeepingAccounts.mch_amt_assert(self, mch_ant_after, mch_ant_bef, mach_pay_up_obj,
                                                 button='refund')  # 校验子商户余额
            HandleKeepingAccounts.mch_sttled_amt(self, settled_ant_aft, settled_ant_bef, mach_pay_up_obj)  # 校验子商户可结算金额
            HandleKeepingAccounts.all_type_mch_len_amt_assert(self, mach_pay_up_obj, amt_info_after,
                                                              type='refund')  # 校验数据数量和在途的数据准确性
        else:
            try:
                HandleKeepingAccounts.public_assert(self, html, excepted)
                if part.__eq__(Constants.RESULT.TRUE):
                    return
                HandleKeepingAccounts.mch_amt_assert(self, mch_ant_after, mch_ant_bef, mach_pay_up_obj,
                                                     button='refund')  # 校验子商户余额
                HandleKeepingAccounts.mch_sttled_amt(self, settled_ant_aft, settled_ant_bef,
                                                     mach_pay_up_obj)  # 校验子商户可结算金额
                HandleKeepingAccounts.all_type_mch_len_amt_assert(self, mach_pay_up_obj, amt_info_after,
                                                                  type='refund')  # 校验数据数量和在途的数据准确性
            except Exception as msg:
                severity, module, title, pri, steps, assignedTo = send_bug_cd.data_util(self.after_treatment_data, html,
                                                                                        msg)
                send_bug_cd.send_bug_to_cd(severity=severity, module=module, title=title, pri=pri, steps=steps,
                                           assignedTo=assignedTo)
                raise msg

    @staticmethod
    def machaccnt_promotion_dispatch_assert(self, html, excepted, mach_pay_up_obj=None, mch_ant_bef=None,
                                            mch_ant_after=None, amt_info_after=None, settled_ant_bef=None,
                                            settled_ant_aft=None, part=Constants.RESULT.FALSE,
                                            put=Constants.RESULT.FALSE):
        if put.__eq__(Constants.RESULT.FALSE):
            HandleKeepingAccounts.public_assert(self, html, excepted)
            if part.__eq__(Constants.RESULT.TRUE):
                return
            HandleKeepingAccounts.mch_amt_assert(self, mch_ant_after, mch_ant_bef, mach_pay_up_obj)  # 校验子商户和准备金账户的余额
            HandleKeepingAccounts.mch_promotion_sttled_amt(self, settled_ant_aft, settled_ant_bef,
                                                           mach_pay_up_obj)  # 校验准备金商户的可结算金额
            HandleKeepingAccounts.has_amt_prepay(self, amt_info_after, mach_pay_up_obj)  # 校验准备金明细是否插入记录
        else:
            try:
                HandleKeepingAccounts.public_assert(self, html, excepted)
                if part.__eq__(Constants.RESULT.TRUE):
                    return
                HandleKeepingAccounts.mch_amt_assert(self, mch_ant_after, mch_ant_bef,
                                                     mach_pay_up_obj)  # 校验子商户和准备金账户的余额
                HandleKeepingAccounts.mch_promotion_sttled_amt(self, settled_ant_aft, settled_ant_bef,
                                                               mach_pay_up_obj)  # 校验准备金商户的可结算金额
                HandleKeepingAccounts.has_amt_prepay(self, amt_info_after, mach_pay_up_obj)  # 校验准备金明细是否插入记录
            except Exception as msg:
                severity, module, title, pri, steps, assignedTo = send_bug_cd.data_util(self.after_treatment_data, html,
                                                                                        msg)
                send_bug_cd.send_bug_to_cd(severity=severity, module=module, title=title, pri=pri, steps=steps,
                                           assignedTo=assignedTo)
                raise msg

    @staticmethod
    def machaccnt_promotion_refund_dispatch_assert(self, html, excepted, mach_pay_up_obj=None, mch_ant_bef=None,
                                                   mch_ant_after=None, amt_info_after=None, settled_ant_bef=None,
                                                   settled_ant_aft=None, part=Constants.RESULT.FALSE,
                                                   put=Constants.RESULT.FALSE):

        if put.__eq__(Constants.RESULT.FALSE):
            HandleKeepingAccounts.public_assert(self, html, excepted)
            if part.__eq__(Constants.RESULT.TRUE):
                return
            HandleKeepingAccounts.mch_amt_assert(self, mch_ant_after, mch_ant_bef, mach_pay_up_obj,
                                                 button='refund')  # 校验子商户和准备金账户的余额
            HandleKeepingAccounts.mch_promotion_sttled_amt(self, settled_ant_aft, settled_ant_bef, mach_pay_up_obj,
                                                           button='refund')  # 校验准备金商户的可结算金额
            HandleKeepingAccounts.has_amt_prepay(self, amt_info_after, mach_pay_up_obj,
                                                 button='refund')  # 校验准备金明细是否插入记录
        else:
            try:
                HandleKeepingAccounts.public_assert(self, html, excepted)
                if part.__eq__(Constants.RESULT.TRUE):
                    return
                HandleKeepingAccounts.mch_amt_assert(self, mch_ant_after, mch_ant_bef, mach_pay_up_obj,
                                                     button='refund')  # 校验子商户和准备金账户的余额
                HandleKeepingAccounts.mch_promotion_sttled_amt(self, settled_ant_aft, settled_ant_bef, mach_pay_up_obj,
                                                               button='refund')  # 校验准备金商户的可结算金额
                HandleKeepingAccounts.has_amt_prepay(self, amt_info_after, mach_pay_up_obj,
                                                     button='refund')  # 校验准备金明细是否插入记录
            except Exception as msg:
                severity, module, title, pri, steps, assignedTo = send_bug_cd.data_util(self.after_treatment_data, html,
                                                                                        msg)
                send_bug_cd.send_bug_to_cd(severity=severity, module=module, title=title, pri=pri, steps=steps,
                                           assignedTo=assignedTo)
                raise msg
