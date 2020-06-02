from common.connection_mysql import ConnectionMysql
from common.constants import Constants
from common.config_manager import ConfigManager
import datetime


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
        sql = "delete from %s where trans_no = '%s' and mch_no='MH20181229115220NBUu'" % (table_name, trans_no)
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
    def select_change():
        """查询手续费费率"""
        sql = "select channel_rate_real from pay_code_config where pay_code='29999'"
        result = ConnectionMysql().select_db(sql)
        return result

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

    @staticmethod
    def update_card_name(button):
        """修改绑定银行卡姓名进行提现测试sql"""
        if button is False:
            sql = "update %s set cardholder_name='提现银行卡姓名修改' where mch_accnt_no='%s'" % (
                Constants.TableName.BANK_CARD, ConfigManager.get_service(Constants.SubMerchant.MUCSUB['mucsub_4']))
        else:
            sql = "update %s set cardholder_name='靳伟' where mch_accnt_no='%s'" % (
                Constants.TableName.BANK_CARD, ConfigManager.get_service(Constants.SubMerchant.MUCSUB['mucsub_4']))
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def update_super_money(button):
        """
        是否开启超额提现开关 True为开启
                          False为关闭
        """
        if button:
            sql = "update mch_other_config set spuer_money = '1' where mch_no = '%s'" % (
                ConfigManager.get_service(Constants.Merchant.CS))
        else:
            sql = "update mch_other_config set spuer_money = '0' where mch_no = '%s'" % (
                ConfigManager.get_service(Constants.Merchant.CS))
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def update_amount(amt, settled_amt, mch):
        """设置测试提现的专用子商户的余额为94999926，可结算余额为44999926"""
        sql = "update mch_accnt set remain_amt = '%s',settled_amount='%s' where mch_accnt_no = '%s'" % (
            amt, settled_amt, mch)
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def update_amount_for_prepay(amt, settled_amt):
        """更新准备金账户余额为10000"""
        sql = "update mch_accnt set remain_amt = '%s',settled_amount='%s' where mch_accnt_no = '%s'" % (
            amt, settled_amt, ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_1']))
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def mct_update_acct_type(button):
        if button is True:
            sql_1 = "update mch_accnt set accnt_type='%s' where mch_accnt_no='%s'" % (
                'mch_sub', ConfigManager.get_service(Constants.SubMerchant.PROFIT['profit_1']))
            sql_2 = "update mch_accnt set accnt_type='%s' where mch_accnt_no='%s'" % (
                'mch_sub', ConfigManager.get_service(Constants.SubMerchant.PROFIT['profit_2']))
        else:
            sql_1 = "update mch_accnt set accnt_type='%s' where mch_accnt_no='%s'" % (
                'profit', ConfigManager.get_service(Constants.SubMerchant.PROFIT['profit_1']))
            sql_2 = "update mch_accnt set accnt_type='%s' where mch_accnt_no='%s'" % (
                'profit', ConfigManager.get_service(Constants.SubMerchant.PROFIT['profit_2']))
        ConnectionMysql().execute_db(sql_1)
        ConnectionMysql().execute_db(sql_2)

    #
    # @staticmethod
    # def mch_update_fixed_poundage(button):
    #     if button is True:
    #         sql = "update mch set fixed_poundage = '100' where mch_no = '%s'" % ConfigManager.get_service(
    #             Constants.Merchant.CS)
    #     else:
    #         sql = "update mch set fixed_poundage = null where mch_no = '%s'" % ConfigManager.get_service(
    #             Constants.Merchant.CS)
    #     ConnectionMysql().execute_db(sql)

    @staticmethod
    def mch_update_fixed_poundage(button, number):
        if button is True:
            sql = "update mch_other_config set fixed_poundage = '%s' where mch_no = '%s'" % (
                number, ConfigManager.get_service(Constants.Merchant.CS))
        else:
            sql = "update mch_other_config set fixed_poundage = null where mch_no = '%s'" % ConfigManager.get_service(
                Constants.Merchant.CS)
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def mch_update_channel_rate_real(channel):
        sql = "update pay_code_config set channel_rate_real = '%s',channel_rate_common = '%s' where pay_code = '29999'" % (
            channel, channel)
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def delete_withdrawal_info(table_name, order_no):
        """提现数据清理"""
        sql = "delete from %s where order_no='%s'" % (table_name, order_no)
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def mch_update_withdraw_status(number):
        """修改withdrawstatus为number"""
        times = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
        sql = "update with_draw_info set withdraw_status = '%s',withdraw_status_time='%s' where order_no='test1' " % (
            number, times)
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def mch_update_request_num(number):
        """修改提现记录表中的requests_num"""
        sql = "update with_draw_info set request_num = '%s' where order_no='test1' " % number
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def mch_update_status(number):
        """1:成功,2:失败,3:其他"""
        sql = "update with_draw_info set status = '%s' where order_no='test1' " % number
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def mch_select_info(table_name):
        """提现明细结果生成"""
        sql = "select * from %s where order_no='test1'" % table_name
        result = ConnectionMysql().select_db(sql)
        return result

    @staticmethod
    def select_fix_poundage():
        """获取数据库的手续费"""
        sql = "select fixed_poundage from mch_other_config where mch_no='%s'" % ConfigManager.get_service(
            Constants.Merchant.CS)
        result = ConnectionMysql().select_db(sql)
        if result[0][0] == None:
            return 0
        return result[0][0]

    @staticmethod
    def update_pay_url(pay_type):
        """更新提现真实请求的url"""
        success_url = Constants.MockUrl.SUCCESS
        fail_url = Constants.MockUrl.FAIL
        wait_url = Constants.MockUrl.WAIT
        time_out_url = Constants.MockUrl.TIME_OUT
        default = Constants.MockUrl.DEFAULT
        select_success_url = Constants.MockUrl.SELECT_SUCCESS
        select_none_url = Constants.MockUrl.SELECT_NONE
        select_wait_url = Constants.MockUrl.SELECT_WAIT
        select_fail_url = Constants.MockUrl.SELECT_FAIL
        select_long_url = Constants.MockUrl.SELECT_LONG

        if pay_type == 'success':
            sql = "update mch_config set pay_url = '%s' where mch_no = '%s'" % (
                success_url, ConfigManager.get_service(Constants.Merchant.CS))
        elif pay_type == 'fail':
            sql = "update mch_config set pay_url = '%s' where mch_no = '%s'" % (
                fail_url, ConfigManager.get_service(Constants.Merchant.CS))
        elif pay_type == 'wait':
            sql = "update mch_config set pay_url = '%s' where mch_no = '%s'" % (
                wait_url, ConfigManager.get_service(Constants.Merchant.CS))
        elif pay_type == 'time_out':
            sql = "update mch_config set pay_url = '%s' where mch_no = '%s'" % (
                time_out_url, ConfigManager.get_service(Constants.Merchant.CS))
        elif pay_type == 'select_success':
            sql = "update mch_config set pay_url = '%s' where mch_no = '%s'" % (
                select_success_url, ConfigManager.get_service(Constants.Merchant.CS))
        elif pay_type == 'select_none':
            sql = "update mch_config set pay_url = '%s' where mch_no = '%s'" % (
                select_none_url, ConfigManager.get_service(Constants.Merchant.CS))
        elif pay_type == 'select_wait':
            sql = "update mch_config set pay_url = '%s' where mch_no = '%s'" % (
                select_wait_url, ConfigManager.get_service(Constants.Merchant.CS))
        elif pay_type == 'select_fail':
            sql = "update mch_config set pay_url = '%s' where mch_no = '%s'" % (
                select_fail_url, ConfigManager.get_service(Constants.Merchant.CS))
        elif pay_type == 'select_long':
            sql = "update mch_config set pay_url = '%s' where mch_no = '%s'" % (
                select_long_url, ConfigManager.get_service(Constants.Merchant.CS))
        else:
            sql = "update mch_config set pay_url = '%s' where mch_no = '%s'" % (
                default, ConfigManager.get_service(Constants.Merchant.CS))
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def select_withdraw_and_status():
        """查询withdraw 和 status 与 remark"""
        sql = "select withdraw_status,status,remark,request_num from with_draw_info where order_no='test1'"
        result = ConnectionMysql().select_db(sql)
        return result

    @staticmethod
    def select_download_url():
        """获取对账单的名称"""
        sql = "select download_url,type from download_info where mch_no = '%s'" % ConfigManager.get_service(
            Constants.Merchant.CS)
        result = ConnectionMysql().select_db(sql)
        return result

    @staticmethod
    def delete_download_info():
        sql = "delete from download_info where mch_no = '%s'" % ConfigManager.get_service(
            Constants.Merchant.CS)
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def insert_download_info(channel, download_url, bill_data, typ, id):
        """制造解析对账单数据"""
        sql = "insert into download_info(id,mch_no,channel,download_url,bill_date,create_time,update_time,type,is_his_data,into_data) " \
              "values ('%s','MH20181229115220NBUu','%s','%s','%s','2019-06-28 06:00:51','2019-06-28 06:00:51','%s',null,null)" % (
                  id, channel, download_url, bill_data, typ)
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def delete_mch_account_details():
        sql = "delete from mch_account_details where mch_no = '%s'" % ConfigManager.get_service(
            Constants.Merchant.CS)
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def select_count_mch_details():
        """获取解析对账单表中共存在多少条数据"""
        sql = "select count(id) from mch_account_details where mch_no = '%s'" % ConfigManager.get_service(
            Constants.Merchant.CS)
        result = ConnectionMysql().select_db(sql)
        return result[0][0]

    @staticmethod
    def select_into_data():
        """获取对账单是否插入明细标志  None为没有插入 1为已经插入"""
        sql = "select into_data from download_info where id = '99999'"
        result = ConnectionMysql().select_db(sql)
        return result[0][0]

    @staticmethod
    def update_into_data():
        """修改对账单解析标识"""
        sql = "update download_info set into_data = '1' where id = '99999'"
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def delete_reconciliation_result():
        sql = "delete from reconciliation_result where mchNo='%s' and beginTime='%s'" % (
            Constants.Merchant.CS, '2020-05-19')
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def delete_reconciliation_result_info():
        sql = "delete from reconciliation_result_info where transNo like 'jinweiceshi%'"
        ConnectionMysql().execute_db(sql)

    @staticmethod
    def delete_pay_refund():
        sql_1 = "delete from his_accnt_mch_sub where trans_no like 'jinweiceshi%'"
        sql_2 = "delete from his_accnt_onway where trans_no like 'jinweiceshi%'"
        sql_3 = "delete from his_accnt_profile where trans_no like 'jinweiceshi%'"
        sql_4 = "delete from mch_accnt_balance_record where id_mch_balance_record like 'test%'"
        ConnectionMysql().execute_db(sql_1)
        ConnectionMysql().execute_db(sql_2)
        ConnectionMysql().execute_db(sql_3)
        ConnectionMysql().execute_db(sql_4)

    @staticmethod
    def select_reconciliation_result():
        sql = "select trans_fee,recon_amt,account_type from reconciliation_result where mchNo='MH20181229115220NBUu' and beginTime='2020-05-19'"
        result = ConnectionMysql().select_db(sql)
        return result[0]

    @staticmethod
    def select_reconciliation_result_info():
        """查询问题件明细"""
        sql = "select type from reconciliation_result_info where transNo like 'jinweiceshi%'"
        result = ConnectionMysql().select_db(sql)
        return result


if __name__ == '__main__':
    a = SqlSave.insert_download_info('2017112800223321', 'zfb_20200519_6RygDDfSs87Ff7l0Q4xx.csv', '20200426', 'zfb')
    print(a)
