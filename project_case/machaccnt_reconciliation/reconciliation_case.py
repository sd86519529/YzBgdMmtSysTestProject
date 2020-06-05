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
        # ClearingReconciliation.clearing_all()
        pass

    def tearDown(self):
        # ClearingReconciliation.clearing_all()
        pass

    @unittest.skip('测试')
    def test_zfb_reconciliation_false(self):
        """支付宝，对不平测试用例集合"""
        CreatReconciliation().zfb_in_transit_data()  # 制造记账退款在途数据
        zfb_path = Constants.RECONCILIATION.false_zfb_path  # 获取对账单数据
        path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.zfb, path_name, '20200519', 'zfb')
        PreconditionDowStatement.statement_analyze_send()
        PreconditionDowStatement.recondition()
        expect = CreatReconciliation.info_assert_kwargs(trans_fee='280', recon_amt=85820, account_type='N',
                                                        info_len=10,
                                                        info_list=['2', '0', '0', '2', '1', '1', '1', '1', '1', '1'])
        actual = PreconditionReconciliation.info_assert_kwargs_actual()
        Handle.machaccnt_handle_assert(self, expect, actual)

    # @unittest.skip('测试')
    def test_zfb_reconciliation_true(self):
        """支付宝对平测试用例集合"""
        CreatReconciliation().zfb_in_transit_true_data()  # 制造对平的在途数据
        zfb_path = Constants.RECONCILIATION.true_zfb_path  # 获取对账单数据
        path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.zfb, path_name, '20200519', 'zfb')
        PreconditionDowStatement.statement_analyze_send()
        PreconditionDowStatement.recondition()

    @unittest.skip('测试')
    def test_cib_reconciliation_false(self):
        """cib对不平测试用例"""
        CreatReconciliation().cib_in_transit_data()  # 制造记账退款在途数据
        zfb_path = Constants.RECONCILIATION.false_cib_path  # 获取对账单数据
        path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.cib, path_name, '20200519', 'cib')
        PreconditionDowStatement.statement_analyze_send()
        PreconditionDowStatement.recondition()
        expect = CreatReconciliation.info_assert_kwargs(trans_fee='280', recon_amt=85820, account_type='N',
                                                        info_len=10,
                                                        info_list=['2', '0', '0', '2', '1', '1', '1', '1', '1', '1'])
        actual = PreconditionReconciliation.info_assert_kwargs_actual()
        Handle.machaccnt_handle_assert(self, expect, actual)

    @unittest.skip('测试')
    def test_dlb_reconciliation_false(self):
        """dlb对不平测试用例"""
        CreatReconciliation().dlb_in_transit_data()  # 制造记账退款在途数据
        zfb_path = Constants.RECONCILIATION.false_dlb_path  # 获取对账单数据
        path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.dlb, path_name, '20200519', 'dlb')
        PreconditionDowStatement.statement_analyze_send()
        PreconditionDowStatement.recondition()
        expect = CreatReconciliation.info_assert_kwargs(trans_fee='280', recon_amt=85820, account_type='N',
                                                        info_len=10,
                                                        info_list=['2', '0', '0', '2', '1', '1', '1', '1', '1', '1'])
        actual = PreconditionReconciliation.info_assert_kwargs_actual()
        Handle.machaccnt_handle_assert(self, expect, actual)

    @unittest.skip('测试')
    def test_yl_reconciliation_false(self):
        """yl对不平测试用例"""
        CreatReconciliation().yl_in_transit_data()  # 制造记账退款在途数据
        zfb_path = Constants.RECONCILIATION.false_yl_path  # 获取对账单数据
        path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.yl, path_name, '20200519', 'yl')
        PreconditionDowStatement.statement_analyze_send()
        PreconditionDowStatement.recondition()
        expect = CreatReconciliation.info_assert_kwargs(trans_fee='280', recon_amt=85820, account_type='N',
                                                        info_len=10,
                                                        info_list=['2', '0', '0', '2', '1', '1', '1', '1', '1', '1'])
        actual = PreconditionReconciliation.info_assert_kwargs_actual()
        Handle.machaccnt_handle_assert(self, expect, actual)

    @unittest.skip('测试')
    def test_qq_reconciliation_false(self):
        """qq对不平测试用例"""
        CreatReconciliation().qq_in_transit_data()  # 制造记账退款在途数据
        zfb_path = Constants.RECONCILIATION.false_qq_path  # 获取对账单数据
        path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.qq, path_name, '20200519', 'qq')
        PreconditionDowStatement.statement_analyze_send()
        PreconditionDowStatement.recondition()
        expect = CreatReconciliation.info_assert_kwargs(trans_fee='174', recon_amt=85926, account_type='N',
                                                        info_len=10,
                                                        info_list=['2', '0', '0', '2', '1', '1', '1', '1', '1', '1'])
        actual = PreconditionReconciliation.info_assert_kwargs_actual()
        Handle.machaccnt_handle_assert(self, expect, actual)


if __name__ == '__main__':
    unittest.main()
