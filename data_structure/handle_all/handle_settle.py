from common.config_manager import ConfigManager
from common.constants import Constants
from data_structure.precodition_all.precodition_settle import PrecoditionSettle
from data_structure.sql_save import SqlSave

class HandleSettle(object):

    @staticmethod
    def get_amount():
        '''获取待结算表各账户的余额'''
        # 存管户
        depository_mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.DEPOSITORY)
        depository_event_amt = SqlSave.select_his_mch_accnt_keep_event_amt(depository_mch_accnt_no, 'depository')
        # 在途商户
        onway_mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.ONWAY)
        onway_event_amt = SqlSave.select_his_mch_accnt_keep_event_amt(onway_mch_accnt_no, 'onway')
        # 分润商户的损益金额
        profit_mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.PROFIT['profit_1'])
        profit_event_amt = SqlSave.select_his_mch_accnt_keep_event_amt(profit_mch_accnt_no, 'profit')
        # 子商户的金额
        mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.MUCSUB['mucsub_1'])
        mch_accnt_no_event_amt = SqlSave.select_his_mch_accnt_keep_event_amt(mch_accnt_no, 'pay')

        amount_list = [depository_event_amt,onway_event_amt,profit_event_amt,mch_accnt_no_event_amt]

        return amount_list

    @staticmethod
    def public_handle(self,channel,is_change):
        """进行存管户和在途账户的金额校验"""
        result = SqlSave.select_reconciliation_result_settle(channel)
        recon_amt = result[2]
        profit_loss_amt = result[3]
        depository_mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.DEPOSITORY)
        depository_event_amt = SqlSave.select_his_mch_accnt_keep_event_amt(depository_mch_accnt_no,'depository')

        self.assertEqual(depository_event_amt,recon_amt)

        onway_mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.ONWAY)
        onway_event_amt = SqlSave.select_his_mch_accnt_keep_event_amt(onway_mch_accnt_no,'onway')

        self.assertEqual(onway_event_amt, recon_amt)

        profit_mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.PROFIT['profit_1'])
        profit_event_amt = SqlSave.select_his_mch_accnt_keep_event_amt(profit_mch_accnt_no,'profit')

        self.assertEqual(profit_event_amt, profit_loss_amt)


        # 进行子商户的金额校验
        mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.MUCSUB['mucsub_1'])

        mch_accnt_no_event_amt = SqlSave.select_his_mch_accnt_keep_event_amt(mch_accnt_no,'pay')

        trans_amount_total =HandleSettle.get_trans_amount_total(channel,is_change)

        self.assertEqual(trans_amount_total, mch_accnt_no_event_amt)


    @staticmethod
    def get_trans_amount_total(channel,is_change):
        """统计结算入账的总金额"""
        # 获取支付记账的金额
        data_list = Constants.CREATE().get_creat_pay_true_list()
        # 获取有转账的金额
        data_list2 = Constants.CREATE().get_creat_dispatch_true_list()
        trans_amount_no_transfer = 0
        if is_change == 1:
            for list in data_list:
                trans_amount_no_transfer = int(list[1]) + trans_amount_no_transfer
            trans_amount_transfer = 0
            for list2 in data_list2:
                trans_amount_transfer = trans_amount_transfer + int(list2[5])

            trans_amount_total = trans_amount_no_transfer + trans_amount_transfer
            return trans_amount_total
        elif is_change == 2:
            for list in data_list:
                trans_amount_no_transfer = int(list[1]) + trans_amount_no_transfer
            trans_amount_transfer = 0
            for list2 in data_list2:
                trans_amount_transfer = trans_amount_transfer + int(list2[5])

            acc_mch_id = ''
            if hasattr(Constants.CHANNEL,channel):
                acc_mch_id = getattr(Constants.CHANNEL,channel)

            channel_rate = float(SqlSave.select_settle_change(acc_mch_id))

            # 支付记账手续费
            trans_amount_no_transfer_rate = 0
            for list in data_list:
                trans_amount_no_transfer_rate = round(int(list[1])*channel_rate,0)+trans_amount_no_transfer_rate
            # 获取转账的手续费
            trans_amount_transfer_rate = 0
            for list2 in data_list2:
                trans_amount_transfer_rate = round(int(list2[4][0][0])*channel_rate,0)+trans_amount_transfer_rate

            # 计算应扣的手续费
            rate_amount = int(trans_amount_no_transfer_rate+trans_amount_transfer_rate)

            trans_amount_total = trans_amount_no_transfer + trans_amount_transfer -rate_amount

            return trans_amount_total

    @staticmethod
    def remain_ant_assert(self,amount_befour):
        amount = HandleSettle.get_amount()
        amount_after = PrecoditionSettle.get_remian_amt()

        depository_remain_amt = amount_befour[0]
        onway_mch_remain_amt = amount_befour[1]
        mch_accnt_no_remain_amt = amount_befour[2]
        mch_accnt_no_settled_amt = amount_befour[3]

        depository_remain_amt_after = depository_remain_amt+amount[0]
        onway_mch_remain_amt_after = onway_mch_remain_amt+amount[1]-amount[2]
        mch_accnt_no_settled_amt_after = mch_accnt_no_settled_amt+amount[3]

        self.assertEqual(depository_remain_amt_after, amount_after[0])
        self.assertEqual(onway_mch_remain_amt_after, amount_after[1])
        self.assertEqual(mch_accnt_no_remain_amt, amount_after[2])
        self.assertEqual(mch_accnt_no_settled_amt_after, amount_after[3])


if __name__ == '__main__':
    HandleSettle.get_trans_amount_total('zfb','2')