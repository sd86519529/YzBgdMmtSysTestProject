import ddt
import unittest
import json
from common.logger import Logger
from common.constants import Constants
from common.read_excle import ReadExl
from common.request_base import RequestBase
from data_structure.handle import Handle
from data_structure.clearing_all.clearing_withdrawal import ClearingWithdrawal
from data_structure.precodition_all.precondition_withdrawal import PreconditionWithdrawal

log = Logger('MachPayDispatch').get_log()

exa_and_approve_list = ReadExl(Constants.EXL.WITHDRAW, sheet=0).obtain_data()
flow_1 = ReadExl.screen_case('提现接口异常流程调用测试用例_1', exa_and_approve_list)  # 其他商户（非子商户，非分润商户）类型发起提现
flow_2 = ReadExl.screen_case('提现接口异常流程调用测试用例_2', exa_and_approve_list)  # 子商户修改银行卡姓名请求提现接口
flow_3 = ReadExl.screen_case('提现接口异常流程调用测试用例_3', exa_and_approve_list)  # 缓存中存在一条提现记录，在未过期的情况下发起提现
flow_4 = ReadExl.screen_case('提现接口异常流程调用测试用例_4', exa_and_approve_list)
flow_5 = ReadExl.screen_case('提现接口异常流程调用测试用例_5', exa_and_approve_list)
flow_6 = ReadExl.screen_case('提现接口异常流程调用测试用例_6', exa_and_approve_list)
flow_7 = ReadExl.screen_case('提现接口异常流程调用测试用例_7', exa_and_approve_list)
flow_8 = ReadExl.screen_case('提现接口异常流程调用测试用例_8', exa_and_approve_list)
flow_9 = ReadExl.screen_case('提现接口异常流程调用测试用例_9', exa_and_approve_list)
flow_9_1 = ReadExl.screen_case('提现接口异常流程调用测试用例_10', exa_and_approve_list)
flow_9_2 = ReadExl.screen_case('提现接口异常流程调用测试用例_11', exa_and_approve_list)
flow_9_3 = ReadExl.screen_case('提现接口异常流程调用测试用例_12', exa_and_approve_list)
flow_9_4 = ReadExl.screen_case('提现接口异常流程调用测试用例_13', exa_and_approve_list)
flow_9_5 = ReadExl.screen_case('提现接口异常流程调用测试用例_14', exa_and_approve_list)
flow_9_6 = ReadExl.screen_case('提现接口异常流程调用测试用例_15', exa_and_approve_list)


@ddt.ddt
class MachRefundError(unittest.TestCase):
    """
    提现测试用例: <br>
    1>>接口所有异常流程验证
    """

    def setUp(self):
        log.info('******************************** -- 测试开始 -- ********************************************')

    # @unittest.skip('测试')
    @ddt.data(*flow_1)
    def test_flow_1(self, flow_1):
        """
        1.其他商户（非子商户，非分润商户）类型发起提现
        2.子商户不绑定银行卡请求提现接口
        3.提现方式为超级网银大于100万发起提现操作
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_1)  # 补充测试商户的余额与可结算余额
        self.err_public(flow_1)

    # @unittest.skip('测试')
    @ddt.data(*flow_2)
    def test_flow_2(self, flow_2):
        """
        1.子商户修改银行卡姓名请求提现接口
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_2)  # 补充测试商户的余额与可结算余额
        PreconditionWithdrawal.update_card_name(button=Constants.RESULT.FALSE)  # 修改银行卡姓名为测试
        try:
            self.err_public(flow_2)
        except Exception as e:
            PreconditionWithdrawal.update_card_name(button=Constants.RESULT.TRUE)  # 修改银行卡姓名为测试
            raise e
        PreconditionWithdrawal.update_card_name(button=Constants.RESULT.TRUE)  # 修改银行卡姓名为测试

    # @unittest.skip('测试')
    @ddt.data(*flow_3)
    def test_flow_3(self, flow_3):
        """
        缓存中存在一条提现记录，在未过期的情况下发起提现
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_3)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_3)
        RequestBase.send_request(**self.after_treatment_data)
        self.err_public(flow_3)

    # @unittest.skip('测试')
    @ddt.data(*flow_4)
    def test_flow_4(self, flow_4):
        """
        缓存中不存在提现记录，在数据库中存在一条orderid为test1的数据，重新请求，金额不同。
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_4)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_4)
        self.after_treatment_data['data']['biz_content']['amount'] = '5000'
        RequestBase.send_request(**self.after_treatment_data)
        # 清理缓存的记录
        ClearingWithdrawal.redis_clear(self.after_treatment_data)
        self.after_treatment_data['data']['biz_content']['amount'] = '4000'
        self.err_public(flow_4)

    # @unittest.skip('测试')
    @ddt.data(*flow_5)
    def test_flow_5(self, flow_5):
        """
        缓存存在，但数据库不存在，发起提现请求
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_5)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_5)
        RequestBase.send_request(**self.after_treatment_data)
        # 清理数据库记录
        ClearingWithdrawal.withdrawal_clear(self.after_treatment_data)
        self.err_public(flow_5)

    # @unittest.skip('测试')
    @ddt.data(*flow_6)
    def test_flow_6(self, flow_6):
        """
        缓存中不存在提现记录，在数据库中存在一条orderid为test1的数据，重新请求，金额相同。
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_6)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_6)
        RequestBase.send_request(**self.after_treatment_data)
        # 清理缓存记录
        ClearingWithdrawal.redis_clear(self.after_treatment_data)
        self.err_public(flow_6)

    # @unittest.skip('测试')
    @ddt.data(*flow_7)
    def test_flow_7(self, flow_7):
        """
        缓存中不存在提现记录，在数据库中存在一条orderid为test1的数据，重新请求，金额相同，withdraw_status为1
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_7)  # 补充测试商户的余额与可结算余额
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(flow_7)
        RequestBase.send_request(**self.after_treatment_data)
        PreconditionWithdrawal.mch_update_withdraw_status('1')
        # 清理数据库记录
        ClearingWithdrawal.redis_clear(self.after_treatment_data)
        self.err_public(flow_7)

    # @unittest.skip('测试')
    @ddt.data(*flow_8)
    def test_flow_8(self, flow_8):
        """
        有提现手续费，但提现金额小于或等于手续费
        """
        PreconditionWithdrawal.mch_update_fixed_poundage()
        PreconditionWithdrawal.mct_update_amount_pre(flow_8)  # 补充测试商户的余额与可结算余额
        try:
            self.err_public(flow_8)
        except Exception as e:
            PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 清空提现手续费
            raise e
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 清空提现手续费

    # @unittest.skip('测试')
    @ddt.data(*flow_9)
    def test_flow_9(self, flow_9):
        """
        提现金额大于手续费，但是不存在分润商户
        """
        PreconditionWithdrawal.mch_update_fixed_poundage()
        PreconditionWithdrawal.mct_update_amount_pre(flow_9)  # 补充测试商户的余额与可结算余额
        PreconditionWithdrawal.mct_update_acct_type()  # 更改分润商户数量为空
        try:
            self.err_public(flow_9)
        except Exception as e:
            PreconditionWithdrawal.mct_update_acct_type(button=Constants.RESULT.FALSE)  # 还原分润商户
            PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 清空提现手续费
            raise e
        PreconditionWithdrawal.mct_update_acct_type(button=Constants.RESULT.FALSE)  # 还原分润商户
        PreconditionWithdrawal.mch_update_fixed_poundage(button=Constants.RESULT.FALSE)  # 清空提现手续费

    # @unittest.skip('测试')
    @ddt.data(*flow_9_1)
    def test_flow_9_1(self, flow_9_1):
        """
        提现金额大于商户的账面余额流程
        """
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_1)  # 补充测试商户的余额与可结算余额
        self.err_public(flow_9_1)

    # @unittest.skip('测试')
    @ddt.data(*flow_9_2)
    def test_flow_9_2(self, flow_9_2):
        """
        提现金额大于商户的可结算余额，小于商户的账面余额未开启超额提现
        """
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_2, set_amt='5000')  # 补充测试商户的余额与可结算余额
        self.err_public(flow_9_2)

    # @unittest.skip('测试')
    @ddt.data(*flow_9_3)
    def test_flow_9_3(self, flow_9_3):
        """
        提现金额大于商户的可结算余额，小于商户的账面余额，开启超额提现但没有准备金账户
        """
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 开启超额提现
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_3, set_amt='5000')  # 补充测试商户的余额与可结算余额
        PreconditionWithdrawal.mct_promotion_pre(button=Constants.RESULT.FALSE, all=Constants.RESULT.TRUE)  # 清空准备金类型商户
        try:
            self.err_public(flow_9_3)
        except Exception as e:
            PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 关闭超额提现
            PreconditionWithdrawal.mct_promotion_pre(button=Constants.RESULT.TRUE)  # 还原准备金类型商户
            raise e
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
        PreconditionWithdrawal.mct_promotion_pre(button=Constants.RESULT.TRUE)  # 还原准备金类型商户

    # @unittest.skip('测试')
    @ddt.data(*flow_9_4)
    def test_flow_9_4(self, flow_9_4):
        """
        提现金额大于商户的可结算余额，小于商户的账面余额，准备金账户余额不足
        """
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.TRUE)  # 开启超额提现
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_4, set_amt='5000')  # 补充测试商户的余额与可结算余额
        PreconditionWithdrawal.mch_update_prepay_amount()  # 设置准备金测试商户的余额和可结算余额
        try:
            self.err_public(flow_9_4)
        except Exception as e:
            PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现
            raise e
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 关闭超额提现

    @ddt.data(*flow_9_5)
    def test_flow_9_5(self, flow_9_5):
        """
        提现金额大于商户的可结算余额，小于商户的账面余额，准备金账户余额不足
        """
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 开启超额提现
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_5, set_amt='-1')  # 补充测试商户的余额与可结算余额
        PreconditionWithdrawal.mch_update_prepay_amount()  # 设置准备金测试商户的余额和可结算余额
        self.err_public(flow_9_5)

    @ddt.data(*flow_9_6)
    def test_flow_9_6(self, flow_9_6):
        """
        提现金额大于商户的可结算余额，小于商户的账面余额，准备金账户余额不足
        """
        PreconditionWithdrawal.mct_update_super_money_pre(is_change=Constants.RESULT.FALSE)  # 开启超额提现
        PreconditionWithdrawal.mct_update_amount_pre(flow_9_6, set_amt='0')  # 补充测试商户的余额与可结算余额
        PreconditionWithdrawal.mch_update_prepay_amount()  # 设置准备金测试商户的余额和可结算余额
        self.err_public(flow_9_6)

    def err_public(self, data):
        log.info('准备开始执行：^^^^^ %s ^^^^^ 编号的测试用例' % data['编号'])
        self.after_treatment_data = Handle.machaccnt_withdraw_handle(data)
        log.info('参数化处理后的测试数据为:--%s' % self.after_treatment_data)
        res, html = RequestBase.send_request(**self.after_treatment_data)  # 发送请求
        log.info('本次请求结果为%s' % html)
        excepted = json.loads(self.after_treatment_data['excepted_code'])
        Handle.machaccnt_promotion_dispatch_assert(self, html, excepted, part=Constants.RESULT.TRUE)

    def tearDown(self):
        ClearingWithdrawal.redis_clear(self.after_treatment_data)
        ClearingWithdrawal.withdrawal_clear(self.after_treatment_data)
        log.info('******************************** -- 测试结束 -- ********************************************')
        log.info('\r\n\r\n\r\n\r\n')


if __name__ == '__main__':
    unittest.main()
