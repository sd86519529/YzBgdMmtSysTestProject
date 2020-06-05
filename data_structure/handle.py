from data_structure.handle_all.handle_keeping_accounts import HandleKeepingAccounts
from data_structure.handle_all.handle_settle import HandleSettle
from data_structure.handle_all.handle_withdrawal import HandleWithdrawal
from data_structure.handle_all.handle_reconciliation import HandleReconciliation
from common.constants import Constants
from common.config_manager import ConfigManager


class Handle(object):
    """
    管理所有的数据处理和预期结果
    keeping_accounts: 记账handle管理
    Handle_Withdrawal: 提现handle管理
    """

    put = ConfigManager.get_basic(Constants.PutBug.BUTTON)  # 是否提交禅道bug

    @staticmethod
    def machaccnt_pay_dispatch_handle(exc_data):
        # 处理记账excle参数
        exc_data = HandleKeepingAccounts.machaccnt_pay_dispatch_handle(exc_data)
        return exc_data

    @staticmethod
    def machaccnt_pay_channel_rate_common(exc_data):
        # 含手续费的记账 excle处理
        copy_exc_data = HandleKeepingAccounts.machaccnt_pay_channel_rate_common(exc_data)
        return copy_exc_data

    @staticmethod
    def machaccnt_pay_dispatch_assert(self, html, excepted, mach_pay_up_obj=None, mch_ant_bef=None, mch_ant_after=None,
                                      amt_info_after=None, part=Constants.RESULT.FALSE):
        # 支付记账断言
        HandleKeepingAccounts.machaccnt_pay_dispatch_assert(self, html, excepted, mach_pay_up_obj, mch_ant_bef,
                                                            mch_ant_after, amt_info_after, part, Handle.put)

    @staticmethod
    def machaccnt_refund_dispatch_assert(self, html, excepted, mach_pay_up_obj=None, mch_ant_bef=None,
                                         mch_ant_after=None, amt_info_after=None, settled_ant_bef=None,
                                         settled_ant_aft=None, part=Constants.RESULT.FALSE):
        # 退款记账断言
        HandleKeepingAccounts.machaccnt_refund_dispatch_assert(self, html, excepted, mach_pay_up_obj, mch_ant_bef,
                                                               mch_ant_after, amt_info_after, settled_ant_bef,
                                                               settled_ant_aft, part, Handle.put)

    @staticmethod
    def machaccnt_promotion_dispatch_assert(self, html, excepted, mach_pay_up_obj=None, mch_ant_bef=None,
                                            mch_ant_after=None, amt_info_after=None, settled_ant_bef=None,
                                            settled_ant_aft=None, part=Constants.RESULT.FALSE):
        # 活动记账断言
        HandleKeepingAccounts.machaccnt_promotion_dispatch_assert(self, html, excepted, mach_pay_up_obj, mch_ant_bef,
                                                                  mch_ant_after, amt_info_after, settled_ant_bef,
                                                                  settled_ant_aft, part, Handle.put)

    @staticmethod
    def machaccnt_promotion_refund_dispatch_assert(self, html, excepted, mach_pay_up_obj=None, mch_ant_bef=None,
                                                   mch_ant_after=None, amt_info_after=None, settled_ant_bef=None,
                                                   settled_ant_aft=None, part=Constants.RESULT.FALSE):
        # 活动退款记账断言
        HandleKeepingAccounts.machaccnt_promotion_refund_dispatch_assert(self, html, excepted, mach_pay_up_obj,
                                                                         mch_ant_bef, mch_ant_after, amt_info_after,
                                                                         settled_ant_bef, settled_ant_aft, part,
                                                                         Handle.put)

    @staticmethod
    def machaccnt_withdraw_handle(exc_data):
        # 处理记账excle参数
        exc_data = HandleWithdrawal.machaccnt_withdraw_handle(exc_data)
        return exc_data

    @staticmethod
    def machaccnt_withdraw_assert(self, html, excepted, befor_dic=None, after_dic=None, part=Constants.RESULT.FALSE):
        # 提现断言
        HandleWithdrawal.machaccnt_withdraw_assert(self, html, excepted, befor_dic, after_dic, part, Handle.put)

    @staticmethod
    def machaccnt_timer_assert(self, html, excepted, befor_tuple=None, after_tuple=None, part=Constants.RESULT.FALSE):
        # 提现定时器断言
        HandleWithdrawal.timer_withdraw_assert(self, html, excepted, befor_tuple, after_tuple, part, Handle.put)

    @staticmethod
    def machaccnt_handle_assert(self, expect, actual):
        # 对账断言
        HandleReconciliation.handle_assert(self, expect, actual)

    @staticmethod
    def machaccnt_settle_handle_assert(self):
        # 结算入账断言
        HandleSettle.public_handle(self)

