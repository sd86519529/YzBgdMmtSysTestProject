import ddt
import unittest
import time
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
flow_1 = ReadExl.screen_case('提现接口定时器流程调用测试用例_1', exa_and_approve_list)
flow_2 = ReadExl.screen_case('提现接口定时器流程调用测试用例_2', exa_and_approve_list)
flow_3 = ReadExl.screen_case('提现接口定时器流程调用测试用例_3', exa_and_approve_list)
flow_4 = ReadExl.screen_case('提现接口定时器流程调用测试用例_4', exa_and_approve_list)
flow_5 = ReadExl.screen_case('提现接口定时器流程调用测试用例_5', exa_and_approve_list)
flow_6 = ReadExl.screen_case('提现接口定时器流程调用测试用例_6', exa_and_approve_list)
flow_7 = ReadExl.screen_case('提现接口定时器流程调用测试用例_7', exa_and_approve_list)
flow_8 = ReadExl.screen_case('提现接口定时器流程调用测试用例_8', exa_and_approve_list)
flow_9 = ReadExl.screen_case('提现接口定时器流程调用测试用例_9', exa_and_approve_list)
flow_10 = ReadExl.screen_case('提现接口定时器流程调用测试用例_10', exa_and_approve_list)
flow_11 = ReadExl.screen_case('提现接口定时器流程调用测试用例_11', exa_and_approve_list)
flow_12 = ReadExl.screen_case('提现接口定时器流程调用测试用例_12', exa_and_approve_list)
flow_13 = ReadExl.screen_case('提现接口定时器流程调用测试用例_13', exa_and_approve_list)
flow_14 = ReadExl.screen_case('提现接口定时器流程调用测试用例_14', exa_and_approve_list)
flow_15 = ReadExl.screen_case('提现接口定时器流程调用测试用例_15', exa_and_approve_list)
flow_16 = ReadExl.screen_case('提现接口定时器流程调用测试用例_16', exa_and_approve_list)
flow_17 = ReadExl.screen_case('提现接口定时器流程调用测试用例_17', exa_and_approve_list)

@ddt.ddt
class MachRefundTimer(unittest.TestCase):
    """
    提现定时器测试用例: <br>
    1>>定时器所有流程校验
    """

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        log.info('******************************** -- 测试开始 -- ********************************************')

    def tearDown(self):
        ClearingWithdrawal.redis_clear(self.after_treatment_data)
        ClearingWithdrawal.withdrawal_clear(self.after_treatment_data)
        log.info('******************************** -- 测试结束 -- ********************************************')
        log.info('\r\n\r\n\r\n\r\n')

    def flow_pass_public(self, data, pay_type, *args, **kwargs):
        """流程公用 pay_type 为 模拟返回结果"""
        log.info('准备开始执行：^^^^^ %s ^^^^^ 编号的测试用例' % data['编号'])
        befor_tuple = MachAntWithdrawUp(self.after_treatment_data).timer_expected_results(True, *args)
        res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
        if kwargs.get('update_withdraw') is not None:
            PreconditionWithdrawal.mch_update_withdraw_status(kwargs['update_withdraw'])
        if kwargs.get('request_num') is not None:
            PreconditionWithdrawal.mch_update_request_num(kwargs['request_num'])
        PreconditionWithdrawal.update_pay_url(pay_type=pay_type)
        PreconditionWithdrawal.send_deal_withdraw()  # 触发提现定时器
        time.sleep(2)
        log.info('本次请求结果为%s' % html)
        after_tuple = MachAntWithdrawUp(self.after_treatment_data).timer_expected_results(False, *args)
        excepted = json.loads(self.after_treatment_data['excepted_code'])
        Handle.machaccnt_timer_assert(self, html, excepted, befor_tuple, after_tuple)

    # @unittest.skip('测试')
    @ddt.data(*flow_1)
    def test_flow_1(self, flow_1):
        """创造一条withdraw_status=0，status=3的测试数据，调用定时器，模拟提现接口返回为成功 预期status=1，withdraw_status=2提现成功"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_1)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_1)
        try:
            self.flow_pass_public(flow_1, 'success', *('2', '1', '交易成功', 0))
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_2)
    def test_flow_2(self, flow_2):
        """创造一条withdraw_status=0，status=3的测试数据，调用定时器，模拟提现接口返回为失败 预期status=1，withdraw_status=2提现失败"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_2)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_2)
        try:
            self.flow_pass_public(flow_2, 'fail', *('2', '2', '交易失败', 0))
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_3)
    def test_flow_3(self, flow_3):
        """创造一条withdraw_status=0，status=3的测试数据，调用定时器，模拟提现接口返回为未决 预期status=1，withdraw_status=2"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_3)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_3)
        try:
            self.flow_pass_public(flow_3, 'wait', *('1', '3', '未决', 0))
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_4)
    def test_flow_4(self, flow_4):
        """创造一条withdraw_status=0，status=3的测试数据，调用定时器，模拟提现接口返回为超时 预期withdraw_status=0，status=3 num=1 """
        PreconditionWithdrawal.mct_update_amount_pre(flow_4)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_4)
        try:
            self.flow_pass_public(flow_4, 'time_out', *('0', '3', None, 1))
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_5)
    def test_flow_5(self, flow_5):
        """创造一条withdraw_status为4，status=3的测试数据，调用定时器，模拟查询接口返回成功，预期status=1，withdraw_status=2提现成功"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_5)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_5)
        try:
            self.flow_pass_public(flow_5, 'select_success', *('2', '1', '交易成功', 0), **{'update_withdraw': '4'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_6)
    def test_flow_6(self, flow_6):
        """创造一条withdraw_status为4，status=3的测试数据，调用定时器，模拟查询接口返回不存在 预期withdraw_status更新为0"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_6)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_6)
        try:
            self.flow_pass_public(flow_6, 'select_none', *('0', '3', None, 0), **{'update_withdraw': '4'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_7)
    def test_flow_7(self, flow_7):
        """创造一条withdraw_status为4，status=3的测试数据，调用定时器，模拟查询接口超时"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_7)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_7)
        try:
            self.flow_pass_public(flow_7, 'time_out', *('4', '3', None, 0), **{'update_withdraw': '4'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_8)
    def test_flow_8(self, flow_8):
        """创造一条withdraw_status为4，status=3的测试数据，调用定时器，模拟查询接口暂时未处理"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_8)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_8)
        try:
            self.flow_pass_public(flow_8, 'select_wait', *('4', '3', None, 0),
                                  **{'update_withdraw': '4'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_9)
    def test_flow_9(self, flow_9):
        """创造一条withdraw_status为4，status=3的测试数据，调用定时器，模拟查询接口失败"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_9)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_9)
        try:
            self.flow_pass_public(flow_9, 'select_fail', *('2', '2', '查询结果为提现失败', 0),
                                  **{'update_withdraw': '4'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_10)
    def test_flow_9_1(self, flow_10):
        """创造一条withdraw_status为0，status=3的测试数据，调用定时器，模拟提现接口失败，过长的remark测试是否能正常储存"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_10)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_10)
        try:
            self.flow_pass_public(flow_10, 'select_long',
                                  *('2', '2', '交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易', 0))
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_11)
    def test_flow_9_2(self, flow_11):
        """创造一条withdraw_status为1，status=3的测试数据，调用定时器，模拟查询接口返回成功，预期status=1，withdraw_status=2提现成功"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_11)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_11)
        try:
            self.flow_pass_public(flow_11, 'select_success', *('2', '1', '交易成功', 0), **{'update_withdraw': '1'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_12)
    def test_flow_9_3(self, flow_12):
        """创造一条withdraw_status为1，status=3的测试数据，调用定时器，模拟查询接口返回不存在 预期withdraw_status更新为0"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_12)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_12)
        try:
            self.flow_pass_public(flow_12, 'select_none', *('0', '3', None, 0), **{'update_withdraw': '1'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_13)
    def test_flow_9_4(self, flow_13):
        """创造一条withdraw_status为1，status=3的测试数据，调用定时器，模拟查询接口超时"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_13)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_13)
        try:
            self.flow_pass_public(flow_13, 'time_out', *('4', '3', None, 0), **{'update_withdraw': '4'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_14)
    def test_flow_9_5(self, flow_14):
        """创造一条withdraw_status为1，status=3的测试数据，调用定时器，模拟查询接口暂时未处理"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_14)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_14)
        try:
            self.flow_pass_public(flow_14, 'select_wait', *('4', '3', None, 0),
                                  **{'update_withdraw': '4'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_15)
    def test_flow_9_6(self, flow_15):
        """创造一条withdraw_status为1，status=3的测试数据，调用定时器，模拟查询接口失败"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_15)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_15)
        try:
            self.flow_pass_public(flow_15, 'select_fail', *('2', '2', '查询结果为提现失败', 0),
                                  **{'update_withdraw': '4'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    # @unittest.skip('测试')
    @ddt.data(*flow_16)
    def test_flow_9_6(self, flow_16):
        """创造一条withdraw_status为0，status=3，number=5 的测试数据，调用定时器，模拟提现接口超时 预期withdraw_status为3  status=2  number=0"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_16)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_16)
        try:
            self.flow_pass_public(flow_16, 'time_out', *('3', '2', '网银代付超时，请重试', 0),
                                  **{'request_num': '5'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址

    @ddt.data(*flow_17)
    def test_flow_9_6(self, flow_17):
        """创造一条withdraw_status为0，status=3，number=5 的测试数据，调用定时器，模拟提现接口超时 预期withdraw_status为3  status=2  number=0"""
        PreconditionWithdrawal.mct_update_amount_pre(flow_17)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_17)
        try:
            self.flow_pass_public(flow_17, 'time_out', *('0', '3', None, 3),
                                  **{'request_num': '2'})
        except Exception as e:
            PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址
            raise e
        PreconditionWithdrawal.update_pay_url(pay_type='default')  # 回复默认url地址


if __name__ == '__main__':
    unittest.main()
