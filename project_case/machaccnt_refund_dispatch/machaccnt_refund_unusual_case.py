import ddt
import unittest
import json
from common.logger import Logger
from common.constants import Constants
from common.read_excle import ReadExl
from common.request_base import RequestBase
from data_structure.precodition_all.precondition import Precondition
from data_structure.handle import Handle
from data_structure.clearing import Clearing
from model.machaccnt_pay_dispatch_model import MachPayDispatchUp

log = Logger('MachPayDispatch').get_log()

exa_and_approve_list = ReadExl(Constants.EXL.REFUND, sheet=0).obtain_data()
unusual_parameter = ReadExl.screen_case('退款记账异常校验测试用例', exa_and_approve_list)  # 异常参数校验数据


@ddt.ddt
class MachRefundUnusual(unittest.TestCase):
    """
    退款记账测试用例: <br>
    1>>接口所有异常字段的验证 test_unusual_parameter
    """

    @classmethod
    def setUpClass(cls):
        """关闭子商户承担手续费"""
        Precondition.mct_pay_channel_rate_pre(is_change=Constants.CHARGE.FALSE)

    def setUp(self):
        log.info('******************************** -- 测试开始 -- ********************************************')

    @ddt.data(*unusual_parameter)
    def test_unusual_parameter(self, unusual_parameter):
        """异常参数校验方法"""
        log.info('准备开始执行：^^^^^ %s ^^^^^ 编号的测试用例' % unusual_parameter['编号'])
        after_treatment_data = Handle.machaccnt_pay_dispatch_handle(unusual_parameter)
        mach_pay_up_obj = MachPayDispatchUp(after_treatment_data)
        log.info('参数化处理后的测试数据为:--%s' % after_treatment_data)
        res, html = RequestBase.send_request(**after_treatment_data)  # 发送请求
        log.info('==============================本次请求结果为:::%s' % html)
        amt_info_after, mch_ant_after, settled_ant_aft = Precondition.mct_refund_dispatch_pre(mach_pay_up_obj)
        Clearing.machaccnt_refund_dispatch_clear(amt_info_after, mach_pay_up_obj)
        excepted = json.loads(after_treatment_data['excepted_code'])
        Handle.machaccnt_refund_dispatch_assert(self, html, excepted, part=True)

    def tearDown(self):
        log.info('******************************** -- 测试结束 -- ********************************************')
        log.info('\r\n\r\n\r\n\r\n')


if __name__ == '__main__':
    unittest.main()
