from data_structure.sql_save import SqlSave


class ClearingReconciliation(object):
    @staticmethod
    def clearing_download_info():
        """清理对账单下载表"""
        SqlSave.delete_download_info()

    @staticmethod
    def clearing_mch_account_details():
        """清理对账单解析数据表"""
        SqlSave.delete_mch_account_details()

    @staticmethod
    def clearing_reconciliation_result():
        """清理对账记录数据 制造的数据为5-19日 所以只清理5-19数据"""
        SqlSave.delete_reconciliation_result()

    @staticmethod
    def clearing_reconciliation_result_info():
        """清理对账明细数据"""
        SqlSave.delete_reconciliation_result_info()

    @staticmethod
    def clearing_pay_refund():
        """清理记账数据"""
        SqlSave.delete_pay_refund()

    @staticmethod
    def clearing_all():
        """全部清理"""
        ClearingReconciliation.clearing_download_info()
        ClearingReconciliation.clearing_mch_account_details()
        ClearingReconciliation.clearing_pay_refund()
        ClearingReconciliation.clearing_reconciliation_result()
        ClearingReconciliation.clearing_reconciliation_result_info()
