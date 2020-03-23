import ddt
import unittest
import json
from common.logger import Logger
from common.constants import Constants
from common.read_excle import ReadExl
from common.request_base import RequestBase
from common.config_manager import ConfigManager
from data_structure.precodition_all.precondition import Precondition
from data_structure.handle import Handle
from data_structure.clearing import Clearing
from model.machaccnt_pay_dispatch_model import MachPayDispatchUp

log = Logger('MachPayDispatch').get_log()

exa_and_approve_list = ReadExl(Constants.EXL.PROMOTION, sheet=0).obtain_data()
flow_not_change_Promotion = ReadExl.screen_case('活动记账正常流程测试用例', exa_and_approve_list)
flow_error_Promotion = ReadExl.screen_case('活动记账异常流程测试用例', exa_and_approve_list)
flow_error_has_Promotion = ReadExl.screen_case('活动记账异常流程测试有多个准备金账户', exa_and_approve_list)
flow_error_none_Promotion = ReadExl.screen_case('活动记账异常流程测试没有准备金账户', exa_and_approve_list)
flow_error_remain_amt_Promotion = ReadExl.screen_case('活动记账异常流程测试备用金账户余额不足', exa_and_approve_list)

unusual_parameter = ReadExl.screen_case('活动记账异常调用测试用例', exa_and_approve_list)  # 异常参数校验数据
print(unusual_parameter)


@ddt.ddt
class MachPromotionDispatch(unittest.TestCase):
    """
    活动记账测试用例: <br>
    """

    def setUp(self):
        log.info('******************************** -- 测试开始 -- ********************************************')

    @ddt.data(*flow_not_change_Promotion)
    def test_flow_promotion(self, flow_not_change_Promotion):
        log.info('准备开始执行：^^^^^ %s ^^^^^ 编号的测试用例' % flow_not_change_Promotion['编号'])
        # 数据初次处理，将数据data中的变量进行替换
        after_treatment_data = Handle.machaccnt_pay_dispatch_handle(flow_not_change_Promotion)
        log.info('参数化处理后的测试数据为:--%s' % after_treatment_data)
        # model模块中的事前调用预处理，主要是返回出数据库查询所使用的条件，和数据库层面的预期结果构造，对象MachPayDispatchUp
        self.mach_pay_up_obj = MachPayDispatchUp(after_treatment_data)
        log.info('预处理返回的内容 mach_pay_up_obj:: %s' % self.mach_pay_up_obj)
        # 通过precondition事前处理器拿到数据库在请求前所需要记录的数据，为了验证请求后的数据变化,去不同的子表中查询出 金额 事前 事后等数据 该子商户现有金额
        amt_info_bef, mch_ant_bef, settled_ant_bef = Precondition.mct_promotion_dispatch_pre(
            self.mach_pay_up_obj)
        res, html = RequestBase.send_request(**after_treatment_data)  # 发送请求
        log.info('本次请求结果为%s' % html)
        # 请求后查询数据变化
        excepted = json.loads(after_treatment_data['excepted_code'])
        self.amt_info_after, mch_ant_after, settled_ant_aft = Precondition.mct_promotion_dispatch_pre(
            self.mach_pay_up_obj)
        log.info('本次数据库查询实际结果返回为 amt_info_after:%s \n mch_ant_after:%s' % (self.amt_info_after, mch_ant_after))
        # 进行结果校验对比，对比内容为excl中的验证点
        Handle.machaccnt_promotion_dispatch_assert(self, html, excepted, self.mach_pay_up_obj, mch_ant_bef,
                                                   mch_ant_after,
                                                   self.amt_info_after, settled_ant_bef, settled_ant_aft)
        Clearing.machaccnt_pay_dispatch_clear(self.amt_info_after, self.mach_pay_up_obj)
        log.info('********************************测试结束 -- 数据清理完成 --********************************************')

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
        after_treatment_data = Handle.machaccnt_pay_dispatch_handle(data)
        log.info('参数化处理后的测试数据为:--%s' % after_treatment_data)
        res, html = RequestBase.send_request(**after_treatment_data)  # 发送请求
        log.info('本次请求结果为%s' % html)
        excepted = json.loads(after_treatment_data['excepted_code'])
        Handle.machaccnt_promotion_dispatch_assert(self, html, excepted, part=Constants.RESULT.TRUE)

    def tearDown(self):
        log.info('******************************** -- 测试结束 -- ********************************************')
        log.info('\r\n\r\n\r\n\r\n')


if __name__ == '__main__':
    unittest.main()
