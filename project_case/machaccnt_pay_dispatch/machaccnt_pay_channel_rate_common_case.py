import ddt
import unittest
import json
from common.logger import Logger
from common.constants import Constants
from common.read_excle import ReadExl
from common.request_base import RequestBase
from data_structure.precodition_all.precondition_keeping_accounts import PreconditionKeepingAccounts
from data_structure.handle import Handle
from data_structure.clearing_all.clearing_keeping_accounts import ClearingKeepingAccounts
from model.machaccnt_pay_dispatch_model import MachPayDispatchUp

log = Logger('MachPayDispatch').get_log()

exa_and_approve_list = ReadExl(Constants.EXL.PAY, sheet=0).obtain_data()
# flow_have_change_pay = ReadExl.screen_case('支付分账正常调用测试用例(包含手续费)', exa_and_approve_list)  # 含手续费流程测试
flow_change_rate_pay = ReadExl.screen_case('支付分账正常调用费率调整流程测试1', exa_and_approve_list)  # 费率为0.8传入1流程测试
flow_change_rate_pay_2 = ReadExl.screen_case('支付分账正常调用费率调整流程测试2', exa_and_approve_list)  # 费率为0.1传入1流程测试
flow_change_rate_pay_3 = ReadExl.screen_case('支付分账正常调用费率调整流程测试3', exa_and_approve_list)  # 费率为0.1传入1流程测试


@ddt.ddt
class MachPayChannel(unittest.TestCase):
    """
    支付记账测试用例: <br>
    1>>子商户承担手续费的流程组合 test_flow_not_change_pay
    """

    @classmethod
    def setUpClass(cls):
        """更改商户承担手续费"""
        PreconditionKeepingAccounts.mct_pay_channel_rate_pre(is_change=Constants.CHARGE.TRUE)

    def setUp(self):
        log.info('******************************** -- 测试开始 -- ********************************************')

    # @ddt.data(*flow_have_change_pay)
    def low(self, flow_have_change_pay):
        log.info('准备开始执行：^^^^^ %s ^^^^^ 编号的测试用例' % flow_have_change_pay['编号'])
        self.after_treatment_data = Handle.machaccnt_pay_dispatch_handle(flow_have_change_pay)
        log.info('参数化处理后的测试数据为:--%s' % self.after_treatment_data)
        # 数据初次处理，将数据data中的变量进行替换
        copy_exc_data = Handle.machaccnt_pay_channel_rate_common(self.after_treatment_data)
        # model模块中的事前调用预处理，主要是返回出数据库查询所使用的条件，和数据库层面的预期结果构造，对象MachPayDispatchUp
        self.mach_pay_up_obj = MachPayDispatchUp(copy_exc_data)
        log.info('预处理返回的内容 mach_pay_up_obj:: %s' % self.mach_pay_up_obj)
        # 通过precondition事前处理器拿到数据库在请求前所需要记录的数据，为了验证请求后的数据变化,去不同的子表中查询出 金额 事前 时候等数据 该子商户现有金额
        amt_info_bef, mch_ant_bef = PreconditionKeepingAccounts.mct_pay_dispatch_pre(self.mach_pay_up_obj)
        res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
        log.info('本次请求结果为%s' % html)
        # 请求后查询数据变化
        excepted = json.loads(self.after_treatment_data['excepted_code'])
        self.amt_info_after, mch_ant_after = PreconditionKeepingAccounts.mct_pay_dispatch_pre(self.mach_pay_up_obj)
        log.info('本次数据库查询实际结果返回为 amt_info_after:%s \n mch_ant_after:%s' % (self.amt_info_after, mch_ant_after))
        # 进行结果校验对比，对比内容为excl中的验证点
        Handle.machaccnt_pay_dispatch_assert(self, html, excepted, self.mach_pay_up_obj, mch_ant_bef,
                                             mch_ant_after,
                                             self.amt_info_after)

    @ddt.data(*flow_change_rate_pay)
    def test_flow_change_rate(self, flow_change_rate_pay):
        # 费率为0.8流程
        PreconditionKeepingAccounts.mct_promotion_set_channel(channel='0.8')
        self.low(flow_change_rate_pay)

    @ddt.data(*flow_change_rate_pay_2)
    def test_flow_change_rate_2(self, flow_change_rate_pay_2):
        # 费率为0.1流程
        PreconditionKeepingAccounts.mct_promotion_set_channel(channel='0.1')
        self.low(flow_change_rate_pay_2)

    @ddt.data(*flow_change_rate_pay_3)
    def test_flow_change_rate_3(self, flow_change_rate_pay_3):
        PreconditionKeepingAccounts.mct_promotion_set_channel(channel='0.0063')
        self.low(flow_change_rate_pay_3)

    def tearDown(self):
        ClearingKeepingAccounts.machaccnt_pay_dispatch_clear(self.amt_info_after, self.mach_pay_up_obj)
        log.info('********************************测试结束 -- 数据清理完成 --********************************************')
        log.info('******************************** -- 测试结束 -- ********************************************')
        log.info('\r\n\r\n\r\n\r\n')

    @classmethod
    def tearDownClass(cls):
        """关闭子商户承担手续费"""
        PreconditionKeepingAccounts.mct_promotion_set_channel(channel='0.001')
        PreconditionKeepingAccounts.mct_pay_channel_rate_pre(is_change=Constants.CHARGE.FALSE)


if __name__ == '__main__':
    unittest.main()
