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

exa_and_approve_list = ReadExl(Constants.EXL.PROMOTION_REFUND, sheet=0).obtain_data()
flow_not_change_Promotion = ReadExl.screen_case('活动记退款账正常流程调用测试用例', exa_and_approve_list)


@ddt.ddt
class MachPromotionRefundDispatch(unittest.TestCase):
    """
    活动退款测试用例: <br>
    1>>活动金额退款正常流程测试 test_flow_promotion
    """

    def setUp(self):
        log.info('******************************** -- 测试开始 -- ********************************************')
        PreconditionKeepingAccounts.mct_promotion_remain_amt_pre(Constants.RESULT.FALSE)
        PreconditionKeepingAccounts.mct_promotion_refund_pre(Constants.PRE_DATA.PRO_REFUND_DATA)  # 准备活动记账数据

    @ddt.data(*flow_not_change_Promotion)
    def test_flow_promotion(self, flow_not_change_Promotion):
        log.info('准备开始执行：^^^^^ %s ^^^^^ 编号的测试用例' % flow_not_change_Promotion['编号'])
        # 数据初次处理，将数据data中的变量进行替换
        self.after_treatment_data = Handle.machaccnt_pay_dispatch_handle(flow_not_change_Promotion)
        log.info('参数化处理后的测试数据为:--%s' % self.after_treatment_data)
        # model模块中的事前调用预处理，主要是返回出数据库查询所使用的条件，和数据库层面的预期结果构造，对象MachPayDispatchUp
        self.mach_pay_up_obj = MachPayDispatchUp(self.after_treatment_data, is_promotion=Constants.RESULT.TRUE)
        log.info('预处理返回的内容 mach_pay_up_obj:: %s' % self.mach_pay_up_obj)
        # 通过precondition事前处理器拿到数据库在请求前所需要记录的数据，为了验证请求后的数据变化,去不同的子表中查询出 金额 事前 事后等数据 该子商户现有金额
        amt_info_bef, mch_ant_bef, settled_ant_bef = PreconditionKeepingAccounts.mct_promotion_dispatch_pre(
            self.mach_pay_up_obj)
        res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
        log.info('本次请求结果为%s' % html)
        # 请求后查询数据变化
        excepted = json.loads(self.after_treatment_data['excepted_code'])
        self.amt_info_after, mch_ant_after, settled_ant_aft = PreconditionKeepingAccounts.mct_promotion_dispatch_pre(
            self.mach_pay_up_obj)
        log.info('本次数据库查询实际结果返回为 amt_info_after:%s \n mch_ant_after:%s' % (self.amt_info_after, mch_ant_after))
        # 进行结果校验对比，对比内容为excl中的验证点
        Handle.machaccnt_promotion_refund_dispatch_assert(self, html, excepted, self.mach_pay_up_obj, mch_ant_bef,
                                                          mch_ant_after,
                                                          self.amt_info_after, settled_ant_bef, settled_ant_aft)

    def tearDown(self):
        ClearingKeepingAccounts.machaccnt_promotion_refund_dispatch_clear(self.after_treatment_data)
        log.info('********************************测试结束 -- 数据清理完成 --********************************************')
        log.info('******************************** -- 测试结束 -- ********************************************')
        log.info('\r\n\r\n\r\n\r\n')


if __name__ == '__main__':
    unittest.main()
