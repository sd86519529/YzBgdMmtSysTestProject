from common.constants import Constants
from model.machaccnt_pay_dispatch_model import MachPayDispatchDown
from data_structure.sql_save import SqlSave


class Precondition(object):
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


if __name__ == '__main__':
    pass
