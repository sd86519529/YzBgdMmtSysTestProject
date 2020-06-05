from common.config_manager import ConfigManager
from common.constants import Constants
from data_structure.sql_save import SqlSave

class HandleSettle(object):

    @staticmethod
    def public_handle(self):
        """进行存管户和在途账户的金额校验"""
        depository_mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.DEPOSITORY)
        depository_event_amt = SqlSave.select_his_mch_accnt_keep_event_amt(depository_mch_accnt_no)

        self.assertEqual(depository_event_amt,980)

        onway_mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.ONWAY)
        onway_event_amt = SqlSave.select_his_mch_accnt_keep_event_amt(onway_mch_accnt_no)

        self.assertEqual(onway_event_amt, 980)
        # 进行子商户的金额校验
        mch_accnt_no = ConfigManager.get_service(Constants.SubMerchant.MUCSUB['mucsub_1'])

        mch_accnt_no_event_amt = SqlSave.select_his_mch_accnt_keep_event_amt(mch_accnt_no)

        trans_amount_total =HandleSettle.get_trans_amount_total()

        self.assertEqual(trans_amount_total, mch_accnt_no_event_amt)


    @staticmethod

    def get_trans_amount_total():
        """统计结算入账的总金额"""
        # 获取支付记账的金额
        data_list = Constants.CREATE().get_creat_pay_true_list()
        trans_amount_no_transfer = 0
        for list in data_list:
            trans_amount_no_transfer = int(list[1])+trans_amount_no_transfer
        # 获取有转账的金额
        data_list2 = Constants.CREATE().get_creat_dispatch_true_list()
        trans_amount_transfer = 0
        for list2 in data_list2:
            trans_amount_transfer = trans_amount_transfer+int(list2[5])

        trans_amount_total = trans_amount_no_transfer+trans_amount_transfer
        return trans_amount_total


if __name__ == '__main__':
    HandleSettle.get_trans_amount_total()