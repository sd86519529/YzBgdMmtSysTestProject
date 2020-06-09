import requests

from common.config_manager import ConfigManager
from common.constants import Constants
from data_structure.sql_save import SqlSave
from model.creat_reconciliation import CreatReconciliation


class PrecoditionSettle(object):
    """结算入账，预先处理"""

    @staticmethod
    def reconditionAccountInfo():
        """统计结算的定时器"""
        url = 'http://172.16.202.160:3054/handMovement/reconditionAccountInfo.htm?billDate=20200519'
        requests.get(url=url)

    @staticmethod
    def settle():
        """入账的定时器"""
        url = 'http://172.16.202.160:3054/handMovement/settle?today=2020-05-19'
        requests.get(url=url)
    # 已废除
    # @staticmethod
    # def precondition_download_info():
    #     """生成对账单下载记录"""
    #     SqlSave.insert_download_info_settle()
    #
    # @staticmethod
    # def precondition_reconciliation_result():
    #     """生成对账结果记录"""
    #     SqlSave.insert_reconciliation_result()

    @staticmethod
    def precondition_fee_undertaker(is_change):
        """生成对账结果记录"""
        SqlSave.update_change(is_change)

    @staticmethod
    def precondition_settle(channel,is_change):
        """生成结算前提条件"""

        PrecoditionSettle.precondition_fee_undertaker(is_change)

        CreatReconciliation().creat_settle_data(channel=channel)

        SqlSave.insert_transaction_details(channel)



    @staticmethod
    def get_remian_amt():
        """查询各账户的账户余额"""
        # 查询存管户余额
        depository_mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.DEPOSITORY)
        depository_remain_amt = SqlSave.select_remain_amt(depository_mch_accnt_no)[0][0]
        # 查询在途账户余额
        onway_mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.ONWAY)
        onway_mch_remain_amt =SqlSave.select_remain_amt(onway_mch_accnt_no)[0][0]
        # 查询子商户余额
        mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.MUCSUB['mucsub_1'])
        mch_accnt_no_remain_amt =SqlSave.select_remain_amt(mch_accnt_no)[0][0]
        # 查询子商户可结算余额
        mch_accnt_no_settled_amt = SqlSave.select_settled_amt(mch_accnt_no)[0][0]

        remian_amt = [depository_remain_amt,onway_mch_remain_amt,mch_accnt_no_remain_amt,mch_accnt_no_settled_amt]
        return remian_amt

if __name__ == '__main__':

    # PrecoditionSettle.settle()
    PrecoditionSettle.get_remian_amt()

