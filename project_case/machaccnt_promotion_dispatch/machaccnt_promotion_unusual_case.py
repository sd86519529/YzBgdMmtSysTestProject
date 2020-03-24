import ddt
import unittest
import json
from common.logger import Logger
from common.constants import Constants
from common.read_excle import ReadExl
from common.request_base import RequestBase
from common.config_manager import ConfigManager
from data_structure.clearing import Clearing
from data_structure.precodition_all.precondition import Precondition
from data_structure.handle import Handle

log = Logger('MachPayDispatch').get_log()

exa_and_approve_list = ReadExl(Constants.EXL.PROMOTION, sheet=0).obtain_data()
flow_error_Promotion = ReadExl.screen_case('活动记账异常流程测试用例', exa_and_approve_list)
flow_error_has_Promotion = ReadExl.screen_case('活动记账异常流程测试有多个准备金账户', exa_and_approve_list)
flow_error_none_Promotion = ReadExl.screen_case('活动记账异常流程测试没有准备金账户', exa_and_approve_list)
flow_error_remain_amt_Promotion = ReadExl.screen_case('活动记账异常流程测试备用金账户余额不足', exa_and_approve_list)
unusual_parameter = ReadExl.screen_case('活动记账异常调用测试用例', exa_and_approve_list)  # 异常参数校验数据


@ddt.ddt
class MachPromotionDispatch(unittest.TestCase):
    """
    活动记账测试用例: <br>
    1>>活动金额记账字段异常测试 test_unusual_parameter <br>
    2>>活动金额记账异常流程测试 test_error_flow*
    """

    def setUp(self):
        log.info('******************************** -- 测试开始 -- ********************************************')

    @ddt.data(*flow_error_has_Promotion)
    def test_error_flow_has_promotion(self, flow_error_has_Promotion):
        """
        异常活动金额支付流程，准备金账户有多个
        """
        Precondition.mct_promotion_pre(button=Constants.RESULT.TRUE,
                                       mch_no=ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_1']))
        Precondition.mct_promotion_pre(button=Constants.RESULT.TRUE,
                                       mch_no=ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_2']))
        self.err_public(flow_error_has_Promotion)
        Precondition.mct_promotion_pre(button=Constants.RESULT.FALSE,
                                       mch_no=ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_2']))

    @ddt.data(*flow_error_none_Promotion)
    def test_error_flow_none_promotion(self, flow_error_none_Promotion):
        """
        异常活动金额支付流程，没有准备金账户
        """
        Precondition.mct_promotion_pre(button=Constants.RESULT.FALSE,
                                       mch_no=ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_2']))
        Precondition.mct_promotion_pre(button=Constants.RESULT.FALSE,
                                       mch_no=ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_1']))
        self.err_public(flow_error_none_Promotion)
        Precondition.mct_promotion_pre(button=Constants.RESULT.TRUE,
                                       mch_no=ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_1']))

    @ddt.data(*flow_error_remain_amt_Promotion)
    def test_error_flow_none_promotion(self, flow_error_remain_amt_Promotion):
        """
        异常活动金额支付流程，没有准备金账户
        """
        Precondition.mct_promotion_remain_amt_pre(Constants.RESULT.TRUE)
        self.err_public(flow_error_remain_amt_Promotion)
        Precondition.mct_promotion_remain_amt_pre(Constants.RESULT.FALSE)

    @ddt.data(*unusual_parameter)
    def test_unusual_parameter(self, unusual_parameter):
        """
        异常活动金额支付流程，没有准备金账户
        """
        self.err_public(unusual_parameter)

    def err_public(self, data):
        log.info('准备开始执行：^^^^^ %s ^^^^^ 编号的测试用例' % data['编号'])
        self.after_treatment_data = Handle.machaccnt_pay_dispatch_handle(data)
        log.info('参数化处理后的测试数据为:--%s' % self.after_treatment_data)
        res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
        log.info('本次请求结果为%s' % html)
        excepted = json.loads(self.after_treatment_data['excepted_code'])
        Handle.machaccnt_promotion_dispatch_assert(self, html, excepted, part=Constants.RESULT.TRUE)

    def tearDown(self):
        Clearing.err_data_clear(self.after_treatment_data)
        log.info('******************************** -- 测试结束 -- ********************************************')
        log.info('\r\n\r\n\r\n\r\n')


if __name__ == '__main__':
    unittest.main()
