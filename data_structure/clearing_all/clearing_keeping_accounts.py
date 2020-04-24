from common.base import Base
from data_structure.sql_save import SqlSave
from common.constants import Constants


class ClearingKeepingAccounts(object):
    """
    本类用于数据清理
    根据不同接口测试条件来进行sql清理或接口层清理
    """

    @staticmethod
    def machaccnt_promotion_dispatch_clear(mch_ant_bef, mach_pay_up_obj):
        """活动记账数据清理"""
        for table_name in mch_ant_bef.keys():
            SqlSave.delete_amt_info(table_name=table_name, trans_no=mach_pay_up_obj.trans_no)

    @staticmethod
    def machaccnt_pay_dispatch_clear(mch_ant_bef, mach_pay_up_obj):
        """支付记账数据清理"""
        for table_name in mch_ant_bef.keys():
            SqlSave.delete_amt_info(table_name=table_name, trans_no=mach_pay_up_obj.trans_no)
        for oder_id in mach_pay_up_obj.oder_no_list:
            SqlSave.delete_mch_accnt_balance_record(oder_id=oder_id)

    @staticmethod
    def machaccnt_refund_dispatch_clear(mch_ant_bef, mach_pay_up_obj):
        """退款记账数据清理"""
        for table_name in mch_ant_bef.keys():
            SqlSave.delete_amt_info_refund(table_name=table_name, trans_no=mach_pay_up_obj.trans_no)
        for oder_id in mach_pay_up_obj.oder_no_list:
            SqlSave.delete_mch_accnt_balance_record(oder_id=oder_id)

    @staticmethod
    def err_data_clear(exe_data):
        """特殊清理方法"""
        trans_no = Base.get_trans_no(exe_data)
        table_name = [Constants.TableName.HIS_ACCNT_PREPAY, Constants.TableName.HIS_ACCNT_ONWAY,
                      Constants.TableName.HIS_ACCNT_PROFILE, Constants.TableName.HIS_ACCNT_MCH_SUB]
        oder_id = ['test1', 'test2', 'test3', 'test4', 'test5', 'test6']
        for table_name in table_name:
            SqlSave.delete_amt_info(table_name=table_name, trans_no=trans_no)
        for id in oder_id:
            SqlSave.delete_mch_accnt_balance_record(oder_id=id)

    @staticmethod
    def machaccnt_promotion_refund_dispatch_clear(exe_data):
        """活动退款记账数据清理"""
        trans_no = Base.get_trans_no(exe_data)
        table_name = [Constants.TableName.HIS_ACCNT_PREPAY, Constants.TableName.HIS_ACCNT_PROFILE,
                      Constants.TableName.HIS_ACCNT_MCH_SUB]
        for t_n in table_name:
            SqlSave.delete_amt_info(table_name=t_n, trans_no=trans_no)
