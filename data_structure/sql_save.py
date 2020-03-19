from common.connection_mysql import ConnectionMysql
from common.constants import Constants
from common.config_manager import ConfigManager


class SqlSave(object):
    @staticmethod
    def select_remain_amt(mch_ant_no):
        """
        通过mch_accnt_no（子商户的商户号）查询出该商户现有金额
        """
        sql = "select remain_amt from mch_accnt where mch_accnt_no = '%s'" % mch_ant_no
        result = ConnectionMysql().select_db(sql)
        return result

    @staticmethod
    def select_settled_amt(mch_ant_no):
        """
        通过mch_accnt_no（子商户的商户号）查询出该商户可结算余额
        """
        sql = "select settled_amount from mch_accnt where mch_accnt_no = '%s'" % mch_ant_no
        result = ConnectionMysql().select_db(sql)
        return result

    @staticmethod
    def select_amt_info(table_name, trans_no, event):
        """
        通过trans_no（订单号）从子商户，分润商户，在途商户表中查询其event_amt,accnt_amt_before,accnt_amt_after
        """
        sql = "select event_amt,accnt_amt_before,accnt_amt_after,mch_accnt_no from %s where trans_no = '%s' and event='%s'" % (
            table_name, trans_no, event)
        result = ConnectionMysql().select_db(sql)
        return result

    @staticmethod
    def delete_amt_info(table_name, trans_no):
        """
        通过trans_no（订单号）清理已经插入的测试数据
        :param table_name:
        :param trans_no:
        :return:
        """
        sql = "delete from %s where trans_no = '%s'" % (table_name, trans_no)
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def delete_mch_accnt_balance_record(oder_id):
        """
        清理事前余额记录表
        :return:
        """
        sql = "delete from mch_accnt_balance_record where id_mch_balance_record = '%s'" % oder_id
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def update_change(is_change):
        """
        更改手续费为29999支付方式，费率为0.01
        :return:
        """
        sql = "update mch_other_config set fee_undertaker='%s',is_charge='Y' where mch_no = '%s'" % (
            is_change, ConfigManager.get_service(
                Constants.Merchant.SW))
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def delete_amt_info_refund(table_name, trans_no):
        """
        退款记账需要清理的数据
        :return:
        """
        sql = "delete from %s where trans_no = '%s' and event='refund'" % (table_name, trans_no)
        ConnectionMysql().execute_db(sql)
