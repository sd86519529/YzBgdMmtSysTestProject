from data_structure.sql_save import SqlSave


class Clearing(object):
    """
    本类用于数据清理
    根据不同接口测试条件来进行sql清理或接口层清理
    """

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
