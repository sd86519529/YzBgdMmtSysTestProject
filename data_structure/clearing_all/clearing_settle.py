from common.redis_connect import remove_mch_accnt_no_settle_key
from data_structure.clearing_all.clearing_reconciliation import ClearingReconciliation
from data_structure.sql_save import SqlSave


class ClearingSettle():

    @staticmethod
    def his_mch_accnt_keep_clear():
        """待结算数据清理"""
        SqlSave.delect_his_mch_accnt_keep()

    @staticmethod
    def transaction_details_clear():
        """流水数据清理"""
        SqlSave.delete_transaction_details()

    @staticmethod
    def his_settled_amount_clear():
        """结算明细清理"""
        SqlSave.his_settled_amount()

    @staticmethod
    def settle_all_clear():
        """待结算数据清理"""
        ClearingSettle.transaction_details_clear()
        ClearingSettle.his_settled_amount_clear()
        ClearingSettle.his_mch_accnt_keep_clear()
        # 清除记账数据
        ClearingReconciliation.clearing_all()
        # 清除redis缓存
        remove_mch_accnt_no_settle_key()

        print('1111')


if __name__ == '__main__':
    ClearingSettle.settle_all_clear()