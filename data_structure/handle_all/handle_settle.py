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
        data_list = Constants.CREATE.creat_pay_true_list
        trans_amount_total = 0
        for list in data_list:
            trans_amount_total = int(list[1])+trans_amount_total
        return trans_amount_total


if __name__ == '__main__':
    HandleSettle.get_trans_amount_total()