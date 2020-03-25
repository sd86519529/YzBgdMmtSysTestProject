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
    def select_amt_info(table_name, trans_no, event=None):
        """
        通过trans_no（订单号）从子商户，分润商户，在途商户表中查询其event_amt,accnt_amt_before,accnt_amt_after
        """
        if event is None:
            sql = "select event_amt,accnt_amt_before,accnt_amt_after,mch_accnt_no from %s where trans_no = '%s'" % (
                table_name, trans_no)
        else:
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
    def delete_amt_info_to_order_id(table_name, trans_no):
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
                Constants.Merchant.CS))
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def delete_amt_info_refund(table_name, trans_no):
        """
        退款记账需要清理的数据
        :return:
        """
        sql = "delete from %s where trans_no = '%s' and event='refund'" % (table_name, trans_no)
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def select_prepay_info(trans_no):
        """
        查询准备金明细
        """
        sql = "select event_amt from his_accnt_prepay where trans_no = '%s'" % trans_no
        result = ConnectionMysql().select_db(sql)
        return result

    @staticmethod
    def update_accnt_type(mch_no, button=Constants.RESULT.TRUE):
        """
        更改备用子账户为准备金账户
        如果 button为True 则把备用账户改为准备金类型，否则吧备用账户改为子账户类型
        :return:
        """
        if button:
            sql = "update mch_accnt set accnt_type = 'prepay' where mch_accnt_no = '%s'" % mch_no
        else:
            sql = "update mch_accnt set accnt_type = 'mchsub' where mch_accnt_no = '%s'" % mch_no
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def update_remain_amt(button=Constants.RESULT.TRUE):
        """
        更改准备金账户的余额为0，测试余额不足流程 button:控制准备金账户余额充足或不足
        :return:
        """
        if button:
            sql = "update mch_accnt set remain_amt = '0' where mch_accnt_no='T0020181229115338000001'"
        else:
            sql = "update mch_accnt set remain_amt = '10000' where mch_accnt_no='T0020181229115338000001'"
        ConnectionMysql().execute_db(sql)
