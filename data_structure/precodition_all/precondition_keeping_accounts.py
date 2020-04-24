from common.constants import Constants
from common.request_base import RequestBase
from model.machaccnt_pay_dispatch_model import MachPayDispatchDown
from data_structure.sql_save import SqlSave


class PreconditionKeepingAccounts(object):
    """
        本类用于前置条件构造
        对于不同的用例所需要的前置条件进行接口层面的构造准备或sql层面的构造准备
    """

    @staticmethod
    def mct_pay_dispatch_pre(c_obj):
        """
        通过事前准备的查询数据进行查询
        1.返回内容 不同子商户对应的金额{'子商户号':'子商户金额'}
        2.返回内容 不同子商户表中的三个金额 请求前的数值，以及对应的数量 {'表名':查询出来的数据}
        :return:
        """
        result = MachPayDispatchDown([Constants.TableName.HIS_ACCNT_PROFILE, Constants.TableName.HIS_ACCNT_ONWAY,
                                      Constants.TableName.HIS_ACCNT_MCH_SUB], c_obj.mch_act_no_list, c_obj.trans_no,
                                     event='pay')

        return result.amt_info, result.mch_ant

    @staticmethod
    def mct_pay_channel_rate_pre(is_change):
        """
        计算手续费时首先将测试商户改为子商户承担 扣除手续费
        :return:
        """
        SqlSave.update_change(is_change)

    @staticmethod
    def mct_refund_dispatch_pre(c_obj):
        """
        通过事前准备的查询数据进行查询
        1.返回内容 不同子商户对应的金额{'子商户号':'子商户金额'}
        2.返回内容 不同子商户表中的三个金额 请求前的数值，以及对应的数量 {'表名':查询出来的数据}
        3.返回内容 不同子商户对应的结算余额{'子商户号':'可结算余额'}
        :return:
        """
        result = MachPayDispatchDown([Constants.TableName.HIS_ACCNT_PROFILE, Constants.TableName.HIS_ACCNT_ONWAY,
                                      Constants.TableName.HIS_ACCNT_MCH_SUB], c_obj.mch_act_no_list, c_obj.trans_no,
                                     event='refund')

        return result.amt_info, result.mch_ant, result.settled_ant

    @staticmethod
    def mct_promotion_dispatch_pre(c_obj):
        """
        通过事前准备的查询数据进行查询
        1.返回内容 不同子商户对应的金额{'子商户号':'子商户金额'}
        2.返回内容 不同子商户表中的三个金额 请求前的数值，以及对应的数量 {'表名':查询出来的数据}
        3.返回内容 不同子商户对应的结算余额{'子商户号':'可结算余额'}
        4.返回内容 准备金明细
        :return:
        """
        result = MachPayDispatchDown([Constants.TableName.HIS_ACCNT_PROFILE, Constants.TableName.HIS_ACCNT_ONWAY,
                                      Constants.TableName.HIS_ACCNT_MCH_SUB, Constants.TableName.HIS_ACCNT_PREPAY],
                                     c_obj.mch_act_no_list, c_obj.trans_no, event=None)

        return result.amt_info, result.mch_ant, result.settled_ant

    @staticmethod
    def mct_promotion_pre(button, mch_no):
        """
        在活动金额记账时更改备用准备金账户类型为准备金
        :return:
        """
        SqlSave.update_accnt_type(mch_no, button=button)

    @staticmethod
    def mct_promotion_remain_amt_pre(button):
        """
        在活动金额记账时使准备金账户的余额充足或不足
        :param button:
        :return:
        """
        SqlSave.update_remain_amt(button)

    @staticmethod
    def mct_promotion_refund_pre():
        """
        活动退款记账时需要提前准备一条活动记账的准备数据
        :return:
        """
        RequestBase.send_request(**Constants.PRE_DATA.PRO_REFUND_DATA)

    @staticmethod
    def mct_promotion_set_channel(channel):
        """更改测试商户手续费费率"""
        SqlSave.mch_update_channel_rate_real(channel)


if __name__ == '__main__':
    pass
