import unittest
import ddt
from common.logger import Logger
from common.constants import Constants
from common.ftp_connect import FtpConnect
from model.creat_reconciliation import CreatReconciliation
from data_structure.precodition_all.precondition_dowload_statement import PreconditionDowStatement
from data_structure.precodition_all.precondition_reconciliation import PreconditionReconciliation
from data_structure.clearing_all.clearing_reconciliation import ClearingReconciliation
from data_structure.handle import Handle

log = Logger('MachPayDispatch').get_log()


@ddt.ddt
class Reconciliation(unittest.TestCase):
    """对账程序 1.mch_account_details 有解析的数据
               2.his_accnt_onway 有在途的数据

    """

    def setUp(self):
        pass

    def tearDown(self):
        ClearingReconciliation.clearing_all()


    def test_zfb_reconciliation_false(self):
        """支付宝，对不平测试用例集合"""
        CreatReconciliation().zfb_in_transit_data()  # 制造记账退款在途数据
        zfb_path = Constants.RECONCILIATION.false_zfb_path  # 获取对账单数据
        path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.zfb, path_name, '20200519', 'zfb')
        PreconditionDowStatement.statement_analyze_send()
        PreconditionDowStatement.recondition()
        expect = CreatReconciliation.info_assert_kwargs(trans_fee='283', recon_amt=86367, account_type='N',
                                                        info_len=8,
                                                        info_list=['2', '0', '0', '1', '1', '1', '1', '1'])
        actual = PreconditionReconciliation.info_assert_kwargs_actual()
        Handle.machaccnt_handle_assert(self, expect, actual)

    @unittest.skip('测试')
    def test_zfb_reconciliation_true(self):
        """支付宝对平测试用例集合"""
        CreatReconciliation().zfb_in_transit_true_data()  # 制造对平的在途数据
        zfb_path = Constants.RECONCILIATION.true_zfb_path  # 获取对账单数据
        path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.zfb, path_name, '20200519', 'zfb')
        PreconditionDowStatement.statement_analyze_send()
        PreconditionDowStatement.recondition()


if __name__ == '__main__':
    unittest.main()
