import time

import ddt
import unittest
import json
from common.logger import Logger
from common.constants import Constants
from common.read_excle import ReadExl
from common.request_base import RequestBase
from data_structure.handle import Handle
from model.machaccnt_withdraw_model import MachAntWithdrawUp
from data_structure.clearing_all.clearing_withdrawal import ClearingWithdrawal
from data_structure.precodition_all.precondition_withdrawal import PreconditionWithdrawal

log = Logger('MachPayDispatch').get_log()

exa_and_approve_list = ReadExl(Constants.EXL.WITHDRAW, sheet=0).obtain_data()
flow_1 = ReadExl.screen_case('提现接口正常流程调用测试用例_1', exa_and_approve_list)
flow_2 = ReadExl.screen_case('提现接口正常流程调用测试用例_2', exa_and_approve_list)
flow_3 = ReadExl.screen_case('提现接口正常流程调用测试用例_3', exa_and_approve_list)
flow_4 = ReadExl.screen_case('提现接口正常流程调用测试用例_4', exa_and_approve_list)
flow_5 = ReadExl.screen_case('提现接口正常流程调用测试用例_5', exa_and_approve_list)
flow_6 = ReadExl.screen_case('提现接口正常流程调用测试用例_6', exa_and_approve_list)
flow_7 = ReadExl.screen_case('提现接口正常流程调用测试用例_7', exa_and_approve_list)
flow_8 = ReadExl.screen_case('提现接口正常流程调用测试用例_8', exa_and_approve_list)
flow_9 = ReadExl.screen_case('提现接口正常流程调用测试用例_9', exa_and_approve_list)
flow_9_1 = ReadExl.screen_case('提现接口正常流程调用测试用例_10', exa_and_approve_list)
flow_9_2 = ReadExl.screen_case('提现接口正常流程调用测试用例_11', exa_and_approve_list)
flow_9_3 = ReadExl.screen_case('提现接口正常流程调用测试用例_12', exa_and_approve_list)
flow_9_4 = ReadExl.screen_case('提现接口正常流程调用测试用例_13', exa_and_approve_list)
flow_9_5 = ReadExl.screen_case('提现接口正常流程调用测试用例_14', exa_and_approve_list)
flow_9_6 = ReadExl.screen_case('提现接口正常流程调用测试用例_15', exa_and_approve_list)
flow_9_7 = ReadExl.screen_case('提现接口正常流程调用测试用例_16', exa_and_approve_list)
flow_9_8 = ReadExl.screen_case('提现接口正常流程调用测试用例_17', exa_and_approve_list)
flow_9_9 = ReadExl.screen_case('提现接口正常流程调用测试用例_18', exa_and_approve_list)


@ddt.ddt
class MachRefundPass(unittest.TestCase):
    """
    提现测试用例: <br>
    1>>接口所有正常流程验证
    """

    @classmethod
    def setUpClass(cls):
        # 增加准备金的金额为10000 为本次测试套件的初始工作
        PreconditionWithdrawal.mct_update_amount_for_prepay_pre()

    def setUp(self):
        log.info('******************************** -- 测试开始 -- ********************************************')

    @staticmethod
    def creat_except_data(with_draw_info_index=0, mch_accnt_info_index=0, his_settled_amount_index=0,
                          profit_index=0, propay_index=0):
        dic = MachAntWithdrawUp.info_assert_kwargs()
        dic['with_draw_info_index'] = with_draw_info_index
        dic['mch_accnt_info_index'] = mch_accnt_info_index
        dic['his_settled_amount_index'] = his_settled_amount_index
        dic['profit_index'] = profit_index
        dic['propay_index'] = propay_index
        return dic

    def flow_pass_public(self, data, is_borrow_money, is_service_charge, type_befor, type_after, **kwargs):
        """流程公用"""
        log.info('准备开始执行：^^^^^ %s ^^^^^ 编号的测试用例' % data['编号'])
        befor_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money,
                                                                                      is_service_charge, type_befor,
                                                                                      **kwargs)
        res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
        log.info('本次请求结果为%s' % html)
        aft_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money, is_service_charge,
                                                                                    type_after, **kwargs)
        excepted = json.loads(self.after_treatment_data['excepted_code'])
        Handle.machaccnt_withdraw_assert(self, html, excepted, befor_dic, aft_dic)

    @unittest.skip('测试')
    @ddt.data(*flow_1)
    def test_flow_1(self, flow_1):
        """缓存中不存在提现记录，在数据库中存在一条orderid为test1的数据,重新请求,金额相同,状态为3。 """
        PreconditionWithdrawal.mct_update_amount_pre(flow_1)  # 补充测试商户的余额与可结算余额
        # 创造一个提现数据
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_1)
        RequestBase.send_request(**self.after_treatment_data)
        PreconditionWithdrawal.mch_update_request_num('6')  # 将request_num置为6
        PreconditionWithdrawal.update_pay_url(pay_type='time_out')
        PreconditionWithdrawal.send_deal_withdraw()  # 触发提现定时器
        ClearingWithdrawal.redis_clear(self.after_treatment_data)  # 清理缓存记录
        # 构造预期结果
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=3,
                                                  his_settled_amount_index=3)
        try:
            self.flow_pass_public(data=flow_1, is_borrow_money=False, is_service_charge=False, type_befor=True,
                                  type_after=False, **kwargs)
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    @unittest.skip('测试')
    @ddt.data(*flow_2)
    def test_flow_2(self, flow_2):
        """商户类型为分润商户的无手续费正常提现测试"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_2)  # 补充测试商户的余额与可结算余额
        # 创造一个提现数据
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 清空提现手续费
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_2)
        # 构造预期结果
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, profit_index=1,
                                                  his_settled_amount_index=1)
        self.flow_pass_public(data=flow_2, is_borrow_money=False, is_service_charge=False, type_befor=True,
                              type_after=False, **kwargs)

    @unittest.skip('测试')
    @ddt.data(*flow_3)
    def test_flow_3(self, flow_3):
        """商户类型为分润商户有手续费正常提现测试"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_3)  # 补充测试商户的余额与可结算余额
        # 创造一个提现数据
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.TRUE)  # 开启提现手续费
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_3)
        # 构造预期结果
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, profit_index=1,
                                                  his_settled_amount_index=1)
        try:
            self.flow_pass_public(data=flow_3, is_borrow_money=False, is_service_charge=False, type_befor=True,
                                  type_after=False, **kwargs)
        except Exception as e:
            PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费
            raise e
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费

    @unittest.skip('测试')
    @ddt.data(*flow_4)
    def test_flow_4(self, flow_4):
        """
        商户类型为子商户，银行卡姓名相同，提现方式为超级网银金额小于100万进行提现测试(启用定时器)
        商户类型为子商户，银行卡姓名相同，提现方式为普通网银进行测试(启用定时器)
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_4)  # 补充测试商户的余额与可结算余额
        # 创造一个提现数据
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_4)
        # 构造预期结果
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=1,
                                                  his_settled_amount_index=1)
        self.flow_pass_public(data=flow_4, is_borrow_money=False, is_service_charge=False, type_befor=True,
                              type_after=False, **kwargs)
        PreconditionWithdrawal.send_deal_withdraw()  # 触发提现定时器 检查提现是否有返回
        result = PreconditionWithdrawal.with_draw_info()
        self.assertEqual(result, '交易成功')

    @unittest.skip('测试')
    @ddt.data(*flow_5)
    def test_flow_5(self, flow_5):
        """商户类型为子商户，无提现手续费，提现金额等于商户可结算余额流程测试"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_5, set_amt='1000')  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_5)
        # 构造预期结果
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=1,
                                                  his_settled_amount_index=1)
        self.flow_pass_public(data=flow_5, is_borrow_money=False, is_service_charge=False, type_befor=True,
                              type_after=False, **kwargs)

    @unittest.skip('测试')
    @ddt.data(*flow_6)
    def test_flow_6(self, flow_6):
        """商户类型为子商户，无提现手续费，提现金额小于商户可结算余额流程测试"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_6)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_6)
        # 构造预期结果
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=1,
                                                  his_settled_amount_index=1)
        self.flow_pass_public(data=flow_6, is_borrow_money=False, is_service_charge=False, type_befor=True,
                              type_after=False, **kwargs)

    # @unittest.skip('测试')
    @ddt.data(*flow_7)
    def test_flow_7(self, flow_7):
        """
        商户类型为子商户，有提现手续费，提现金额大于商户可结算余额，小于商户账面余额，开启超额提现，从准备金账户借款流程测试
        提现金额>手续费+结算金额
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_7, set_amt='1000')
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_7)
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.TRUE)  # 开启提现手续费
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 开启超额提现
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=2,
                                                  his_settled_amount_index=3, profit_index=1, propay_index=1)
        try:
            self.flow_pass_public(data=flow_7, is_borrow_money=True, is_service_charge=True, type_befor=True,
                                  type_after=False, **kwargs)
        except Exception as e:
            PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费
            PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
            raise e
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费

    @unittest.skip('测试')
    @ddt.data(*flow_8)
    def test_flow_8(self, flow_8):
        """
        商户类型为子商户，有提现手续费，提现金额大于商户可结算余额，小于商户账面余额，开启超额提现，从准备金账户借款流程测试
        提现金额=手续费+结算金额
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_8, set_amt='1000')
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_8)
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.TRUE)  # 开启提现手续费
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 开启超额提现
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=2,
                                                  his_settled_amount_index=3, profit_index=1, propay_index=1)
        try:
            self.flow_pass_public(data=flow_8, is_borrow_money=True, is_service_charge=True, type_befor=True,
                                  type_after=False, **kwargs)
        except Exception as e:
            PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费
            PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
            raise e
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费

    @unittest.skip('测试')
    @ddt.data(*flow_9)
    def test_flow_9(self, flow_9):
        """
        商户类型为子商户，有提现手续费，提现金额大于商户可结算余额，小于商户账面余额，开启超额提现，从准备金账户借款流程测试
        手续费为0
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_9, set_amt='1000')
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_9)
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.TRUE, number=0)  # 开启提现手续费
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 开启超额提现
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=1,
                                                  his_settled_amount_index=1, profit_index=0, propay_index=1)
        try:
            self.flow_pass_public(data=flow_9, is_borrow_money=True, is_service_charge=True, type_befor=True,
                                  type_after=False, **kwargs)
        except Exception as e:
            PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费
            PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
            raise e
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费

    @unittest.skip('测试')
    @ddt.data(*flow_9_1)
    def test_flow_10(self, flow_9_1):
        """
        商户类型为子商户，有提现手续费，提现金额大于商户可结算余额，小于商户账面余额，开启超额提现，从准备金账户借款流程测试
        结算金额为负数
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_1, set_amt='-200')
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_9_1)
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.TRUE)  # 开启提现手续费
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 开启超额提现
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=2,
                                                  his_settled_amount_index=3, profit_index=1, propay_index=1)
        try:
            self.flow_pass_public(data=flow_9_1, is_borrow_money=True, is_service_charge=True, type_befor=True,
                                  type_after=False, **kwargs)
        except Exception as e:
            PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费
            PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
            raise e
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费

    @unittest.skip('测试')
    @ddt.data(*flow_9_2)
    def test_flow_11(self, flow_9_2):
        """
        商户类型为子商户，无提现手续费，需要借用准备金流程测试
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_2, set_amt='1000')
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_9_2)
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 开启超额提现
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=1,
                                                  his_settled_amount_index=1, propay_index=1)
        try:
            self.flow_pass_public(data=flow_9_2, is_borrow_money=True, is_service_charge=True, type_befor=True,
                                  type_after=False, **kwargs)
        except Exception as e:
            PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
            raise e
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现

    @unittest.skip('测试')
    @ddt.data(*flow_9_3)
    def test_flow_12(self, flow_9_3):
        """
        子商户结算余额为负数，无提现手续费，提现金额小于准备金，但大于准备金+结算余额进行测试
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_3, set_amt='-200')
        PreconditionWithdrawal.mch_update_prepay_amount(amt='10000', set_amt='10000')
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_9_3)
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 开启超额提现
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=1,
                                                  his_settled_amount_index=1, propay_index=1)
        try:
            self.flow_pass_public(data=flow_9_3, is_borrow_money=True, is_service_charge=True, type_befor=True,
                                  type_after=False, **kwargs)
        except Exception as e:
            PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
            raise e
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现

    @unittest.skip('测试')
    @ddt.data(*flow_9_4)
    def test_flow_13(self, flow_9_4):
        """
        商户类型为子商户，有提现手续费，提现金额大于商户可结算余额，小于商户账面余额，开启超额提现，存在多个准备金账户借款流程测试
        测试结果：只会扣减第一个准备金账户
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_4, set_amt='1000')
        PreconditionWithdrawal.mct_promotion_pre(button=Constants.RESULT.TRUE,
                                                 all=Constants.RESULT.TRUE)  # 将准备金数量更改至大于1
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_9_4)
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 开启超额提现
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=1,
                                                  his_settled_amount_index=1, propay_index=1)
        try:
            self.flow_pass_public(data=flow_9_4, is_borrow_money=True, is_service_charge=False, type_befor=True,
                                  type_after=False, **kwargs)
        except Exception as e:
            PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
            PreconditionWithdrawal.mct_promotion_pre(button=Constants.RESULT.TRUE,
                                                     all=Constants.RESULT.TRUE)  # 还原准备金数量
            raise e
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
        PreconditionWithdrawal.mct_promotion_pre(button=Constants.RESULT.TRUE, all=Constants.RESULT.TRUE)  # 还原准备金数量

    @unittest.skip('测试')
    @ddt.data(*flow_9_5)
    def test_flow_14(self, flow_9_5):
        """缓存中不存在提现记录，在数据库中存在一条orderid为test1的数据，重新请求，金额相同。 withdraw_status2。提现完成订单返回 分为status为成功"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_5)  # 补充测试商户的余额与可结算余额
        # 创造一个提现数据
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_9_5)
        kwargs = MachRefundPass.creat_except_data(with_draw_info_index=1, mch_accnt_info_index=1,
                                                  his_settled_amount_index=1)
        befor_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money=False,
                                                                                      is_service_charge=False,
                                                                                      type=True, **kwargs)
        RequestBase.send_request(**self.after_treatment_data)
        PreconditionWithdrawal.update_pay_url(pay_type='success')
        PreconditionWithdrawal.send_deal_withdraw()  # 触发提现定时器
        ClearingWithdrawal.redis_clear(self.after_treatment_data)  # 清理缓存记录
        try:
            res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
            log.info('本次请求结果为%s' % html)
            self.assertNotEqual(len(html.get('biz_content').get('status')), '1',
                                msg='没有返回数据库以存在的T0020181229204406000002订单信息')
            aft_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money=False,
                                                                                        is_service_charge=False,
                                                                                        type=False, **kwargs)
            excepted = json.loads(self.after_treatment_data['excepted_code'])
            Handle.machaccnt_withdraw_assert(self, html, excepted, befor_dic, aft_dic)
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    @unittest.skip('测试')
    @ddt.data(*flow_9_6)
    def test_flow_15(self, flow_9_6):
        """缓存中不存在提现记录，在数据库中存在一条orderid为test1的数据，重新请求，金额相同。 withdraw_status2。提现完成订单返回 分为status为失败"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_6)  # 补充测试商户的余额与可结算余额
        # 创造一个提现数据
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_9_6)
        befor_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money=False,
                                                                                      is_service_charge=False,
                                                                                      type=False)
        befor_dic['info_index']['with_draw_info_index'] = 1
        befor_dic['info_index']['mch_accnt_info_index'] = 2
        befor_dic['info_index']['his_settled_amount_index'] = 2
        RequestBase.send_request(**self.after_treatment_data)
        PreconditionWithdrawal.update_pay_url(pay_type='fail')
        PreconditionWithdrawal.send_deal_withdraw()  # 触发提现定时器
        ClearingWithdrawal.redis_clear(self.after_treatment_data)  # 清理缓存记录
        try:
            res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
            self.assertNotEqual(len(html.get('biz_content').get('errmsg')), '交易失败',
                                msg='没有返回数据库以存在的T0020181229204406000002交易失败的信息')
            log.info('本次请求结果为%s' % html)
            aft_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money=False,
                                                                                        is_service_charge=False,
                                                                                        type=False)
            excepted = json.loads(self.after_treatment_data['excepted_code'])
            Handle.machaccnt_withdraw_assert(self, html, excepted, befor_dic, aft_dic)
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    @unittest.skip('测试')
    @ddt.data(*flow_9_7)
    def test_flow_16(self, flow_9_7):
        """缓存中不存在提现记录，在数据库中存在一条orderid为test1的数据，
        有提现手续费，无准备金借取，重新请求，金额相同。 withdraw_status2。提现完成订单返回 分为status为失败"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_7)
        # 创造一个提现数据
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_9_7)
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.TRUE)  # 开启提现手续费
        befor_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money=False,
                                                                                      is_service_charge=True,
                                                                                      type=False)
        befor_dic['info_index']['with_draw_info_index'] = 1
        befor_dic['info_index']['mch_accnt_info_index'] = 4  # 提现扣减 手续费扣减 提现退还 手续费退还
        befor_dic['info_index']['his_settled_amount_index'] = 6  # 三条正向操作提现记录 三条退还提现记录
        befor_dic['info_index']['profit_index'] = 2  # 提现增加手续费 退还减少手续费
        RequestBase.send_request(**self.after_treatment_data)
        PreconditionWithdrawal.update_pay_url(pay_type='fail')
        PreconditionWithdrawal.send_deal_withdraw()  # 触发提现定时器
        ClearingWithdrawal.redis_clear(self.after_treatment_data)  # 清理缓存记录
        try:
            res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
            self.assertNotEqual(len(html.get('biz_content').get('errmsg')), '交易失败',
                                msg='没有返回数据库以存在的T0020181229204406000002交易失败的信息')
            log.info('本次请求结果为%s' % html)
            aft_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money=False,
                                                                                        is_service_charge=True,
                                                                                        type=False)
            excepted = json.loads(self.after_treatment_data['excepted_code'])
            Handle.machaccnt_withdraw_assert(self, html, excepted, befor_dic, aft_dic)
        except Exception as e:
            PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    @unittest.skip('测试')
    @ddt.data(*flow_9_8)
    def test_flow_17(self, flow_9_8):
        """缓存中不存在提现记录，在数据库中存在一条orderid为test1的数据，
        有提现手续费，有准备金借取，重新请求，金额相同。 withdraw_status2。提现完成订单返回 分为status为失败"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_8, set_amt='1000')  # 补充测试商户的余额与可结算余额
        # 创造一个提现数据
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_9_8)
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.TRUE)  # 开启提现手续费
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 开启超额提现
        befor_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money=True,
                                                                                      is_service_charge=True,
                                                                                      type=False)
        befor_dic['info_index']['with_draw_info_index'] = 1
        befor_dic['info_index']['mch_accnt_info_index'] = 4  # 提现扣减 手续费扣减 提现退还 手续费退还
        befor_dic['info_index']['his_settled_amount_index'] = 6  # 三条正向操作提现记录 三条退还提现记录
        befor_dic['info_index']['profit_index'] = 2  # 提现增加手续费 退还减少手续费
        befor_dic['info_index']['propay_index'] = 2  # 借准备金记录 还准备金记录
        RequestBase.send_request(**self.after_treatment_data)
        PreconditionWithdrawal.update_pay_url(pay_type='fail')
        PreconditionWithdrawal.send_deal_withdraw()  # 触发提现定时器
        ClearingWithdrawal.redis_clear(self.after_treatment_data)  # 清理缓存记录
        try:
            res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
            self.assertNotEqual(len(html.get('biz_content').get('errmsg')), '交易失败',
                                msg='没有返回数据库以存在的T0020181229204406000002交易失败的信息')
            log.info('本次请求结果为%s' % html)
            aft_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money=True,
                                                                                        is_service_charge=True,
                                                                                        type=False)
            excepted = json.loads(self.after_treatment_data['excepted_code'])
            Handle.machaccnt_withdraw_assert(self, html, excepted, befor_dic, aft_dic)
        except Exception as e:
            PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费
            PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 关闭超额提现
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 关闭提现手续费
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 关闭超额提现
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    @unittest.skip('测试')
    @ddt.data(*flow_9_9)
    def test_flow_18(self, flow_9_9):
        """超时时数据回滚流程测试"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_9)  # 补充测试商户的余额与可结算余额
        # 创造一个提现数据
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_9_9)
        befor_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money=False,
                                                                                      is_service_charge=False,
                                                                                      type=False)
        befor_dic['info_index']['with_draw_info_index'] = 1
        befor_dic['info_index']['mch_accnt_info_index'] = 2
        befor_dic['info_index']['his_settled_amount_index'] = 2
        try:
            res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
            PreconditionWithdrawal.update_pay_url(pay_type='time_out')
            PreconditionWithdrawal.mch_update_request_num('5')
            PreconditionWithdrawal.send_deal_withdraw()  # 触发提现定时器
            log.info('本次请求结果为%s' % html)
            aft_dic = MachAntWithdrawUp(self.after_treatment_data).amt_expected_results(is_borrow_money=False,
                                                                                        is_service_charge=False,
                                                                                        type=False)
            excepted = json.loads(self.after_treatment_data['excepted_code'])
            Handle.machaccnt_withdraw_assert(self, html, excepted, befor_dic, aft_dic)
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    def tearDown(self):
        ClearingWithdrawal.redis_clear(self.after_treatment_data)
        ClearingWithdrawal.withdrawal_clear(self.after_treatment_data)
        log.info('******************************** -- 测试结束 -- ********************************************')
        log.info('\r\n\r\n\r\n\r\n')


if __name__ == '__main__':
    unittest.main()
