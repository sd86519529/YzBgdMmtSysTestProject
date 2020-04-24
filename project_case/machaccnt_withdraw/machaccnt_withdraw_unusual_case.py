import ddt
import unittest
import json
from common.logger import Logger
from common.constants import Constants
from common.read_excle import ReadExl
from common.request_base import RequestBase
from data_structure.handle import Handle
from data_structure.clearing_all.clearing_withdrawal import ClearingWithdrawal

log = Logger('MachPayDispatch').get_log()

exa_and_approve_list = ReadExl(Constants.EXL.WITHDRAW, sheet=0).obtain_data()
unusual_parameter = ReadExl.screen_case('提现接口异常调用测试用例', exa_and_approve_list)  # 异常参数校验数据


@ddt.ddt
class MachRefundUnusual(unittest.TestCase):
    """
    提现测试用例: <br>
    1>>接口所有异常字段的验证 test_unusual_parameter
    """

    def setUp(self):
        log.info('******************************** -- 测试开始 -- ********************************************')

    @ddt.data(*unusual_parameter)
    def test_unusual_parameter(self, unusual_parameter):
        """异常参数校验方法"""
        log.info('准备开始执行：^^^^^ %s ^^^^^ 编号的测试用例' % unusual_parameter['编号'])
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(unusual_parameter)
        log.info('参数化处理后的测试数据为:--%s' % self.after_treatment_data)
        res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
        log.info('==============================本次请求结果为:::%s' % html)
        excepted = json.loads(self.after_treatment_data['excepted_code'])
        Handle.machaccnt_withdraw_assert(self, html, excepted, part=True)

    def tearDown(self):
        ClearingWithdrawal.redis_clear(self.after_treatment_data)
        ClearingWithdrawal.withdrawal_clear(self.after_treatment_data)
        log.info('******************************** -- 测试结束 -- ********************************************')
        log.info('\r\n\r\n\r\n\r\n')


if __name__ == '__main__':
    unittest.main()
