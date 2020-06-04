from data_structure.sql_save import SqlSave


class ClearingSettle():

    @staticmethod
    def download_info_clear():
        """下载对账单数据清理"""
        SqlSave.delect_download_info()

    @staticmethod
    def reconciliation_result_clear():
        """对账结果数据清理"""
        SqlSave.delect_reconciliation_result()

    @staticmethod
    def his_mch_accnt_keep_clear():
        """待结算数据清理"""
        SqlSave.delect_his_mch_accnt_keep()

    @staticmethod
    def settle_all_clear():
        """待结算数据清理"""
        ClearingSettle.download_info_clear()
        ClearingSettle.his_mch_accnt_keep_clear()
        ClearingSettle.reconciliation_result_clear()