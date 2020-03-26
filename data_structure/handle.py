from data_structure.handle_all.handlekeepingaccounts import HandleKeepingAccounts
from common.constants import Constants
from common.config_manager import ConfigManager


class Handle(object):
    """
    管理所有的数据处理和预期结果
    keeping_accounts: 记账handle管理
    """

    put = ConfigManager.get_basic(Constants.PutBug.BUTTON)  # 是否提交禅道bug

    @staticmethod
    def machaccnt_pay_dispatch_handle(exc_data):
        # 处理excle参数
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
