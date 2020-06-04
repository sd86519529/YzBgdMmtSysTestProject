import requests

from data_structure.sql_save import SqlSave


class PrecoditionSettle(object):
    """结算入账，预先处理"""

    @staticmethod
    def reconditionAccountInfo():
        """统计结算的定时器"""
        url = 'http://172.16.202.160:3054/handMovement/reconditionAccountInfo.htm?billDate=20200101'
        requests.get(url=url)

    @staticmethod
    def settle():
        """入账的定时器"""
        url = 'http://172.16.202.160:3054/handMovement/settle?today=2020-01-01'
        requests.get(url=url)

    @staticmethod
    def precondition_download_info():
        """生成对账单下载记录"""
        SqlSave.insert_download_info()

    @staticmethod
    def precondition_reconciliation_result():
        """生成对账结果记录"""
        SqlSave.insert_reconciliation_result()

    @staticmethod
    def precondition_settle():
        """生成结算前提条件"""
        PrecoditionSettle.precondition_download_info()
        PrecoditionSettle.precondition_reconciliation_result()