import ddt
import unittest
import json
from common.logger import Logger
from common.constants import Constants
from common.read_excle import ReadExl
from common.request_base import RequestBase
from data_structure.clearing_all.clearing_keeping_accounts import ClearingKeepingAccounts
from data_structure.precodition_all.precondition_keeping_accounts import PreconditionKeepingAccounts
from data_structure.handle import Handle

log = Logger('MachPayDispatch').get_log()

exa_and_approve_list = ReadExl(Constants.EXL.PAY, sheet=0).obtain_data()
unusual_parameter3 = ReadExl.screen_case('支付分账异常调用测试用例3', exa_and_approve_list)  # 异常参数校验数据
unusual_parameter2 = ReadExl.screen_case('支付分账异常调用测试用例2', exa_and_approve_list)  # 异常参数校验数据
unusual_parameter = ReadExl.screen_case('支付分账异常调用测试用例', exa_and_approve_list)  # 异常参数校验数据


@ddt.ddt
class MachPayUnusual(unittest.TestCase):
    """
    支付记账测试用例: <br>
    1>>接口所有异常字段的验证 test_unusual_parameter
    """

    @classmethod
    def setUpClass(cls):
        """关闭子商户承担手续费"""
        PreconditionKeepingAccounts.mct_pay_channel_rate_pre(is_change=Constants.CHARGE.FALSE)

    def setUp(self):
        log.info('******************************** -- 测试开始 -- ********************************************')

    @ddt.data(*unusual_parameter)
    def test_unusual_parameter(self, unusual_parameter):
        log.info('准备开始执行：^^^^^ %s ^^^^^ 编号的测试用例' % unusual_parameter['编号'])
        self.after_treatment_data = Handle.machaccnt_pay_dispatch_handle(unusual_parameter)
        log.info('参数化处理后的测试数据为:--%s' % self.after_treatment_data)
        res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
        log.info('本次请求结果为%s' % html)
        excepted = json.loads(self.after_treatment_data['excepted_code'])
        Handle.machaccnt_pay_dispatch_assert(self, html, excepted, part=True)

    # @unittest.skip('测试')
    @ddt.data(*unusual_parameter2)
    def test_unusual_parameter2(self, unusual_parameter):
        # 提前准备一条数据
        PreconditionKeepingAccounts.mct_promotion_refund_pre(Constants.PRE_DATA.PAY_DATA)
        self.after_treatment_data = Handle.machaccnt_pay_dispatch_handle(unusual_parameter)
        log.info('参数化处理后的测试数据为:--%s' % self.after_treatment_data)
        res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
        log.info('本次请求结果为%s' % html)
        excepted = json.loads(self.after_treatment_data['excepted_code'])
        Handle.machaccnt_pay_dispatch_assert(self, html, excepted, part=True)

    # @unittest.skip('测试')
    @ddt.data(*unusual_parameter3)
    def test_unusual_parameter3(self, unusual_parameter):
        # 提前准备一条数据
        PreconditionKeepingAccounts.mct_promotion_refund_pre(Constants.PRE_DATA.PAY_DATA)
        self.after_treatment_data = Handle.machaccnt_pay_dispatch_handle(unusual_parameter)
        log.info('参数化处理后的测试数据为:--%s' % self.after_treatment_data)
        res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
        log.info('本次请求结果为%s' % html)
        excepted = json.loads(self.after_treatment_data['excepted_code'])
        try:
            Handle.machaccnt_pay_dispatch_assert(self, html, excepted, part=True)
        except Exception as e:
            ClearingKeepingAccounts.err_data_clear(self.after_treatment_data, trans_no='MH20181229115220NBUu')
            raise e
        ClearingKeepingAccounts.err_data_clear(self.after_treatment_data, trans_no='MH20181229115220NBUu')

    def tearDown(self):
        ClearingKeepingAccounts.err_data_clear(self.after_treatment_data)
        log.info('******************************** -- 测试结束 -- ********************************************')
        log.info('\r\n\r\n\r\n\r\n')


if __name__ == '__main__':
    unittest.main()
