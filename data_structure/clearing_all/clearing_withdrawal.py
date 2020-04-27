from common.config_manager import ConfigManager
from data_structure.sql_save import SqlSave
from common.constants import Constants
from common import redis_connect


class ClearingWithdrawal(object):
    """
    本类用于数据清理
    根据不同接口测试条件来进行sql清理或接口层清理
    提现
    """

    @staticmethod
    def withdrawal_clear(data):
        """提现记录数据清理"""
        order_no = data['data']['biz_content']['order_no']
        table_name = [Constants.TableName.WITH_DRAW_INFO, Constants.TableName.HIS_ACCNT_PROFILE,
                      Constants.TableName.HIS_ACCNT_MCH_SUB, Constants.TableName.HIS_SETTLED_AMOUNT,
                      Constants.TableName.HIS_ACCNT_PREPAY]
        for tb in table_name:
            SqlSave.delete_withdrawal_info(table_name=tb, order_no=order_no)

    @staticmethod
    def redis_clear(data):
        order_no = data['data']['biz_content']['order_no']
        mch_no = ConfigManager.get_service(Constants.Merchant.CS)
        redis_connect.remove_withdrawal_info(mch_no, order_no)
