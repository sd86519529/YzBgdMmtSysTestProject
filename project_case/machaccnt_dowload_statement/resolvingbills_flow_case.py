import ddt
import datetime
import unittest
from common.constants import Constants
from common.ftp_connect import FtpConnect
from common.logger import Logger
from data_structure.precodition_all.precondition_dowload_statement import PreconditionDowStatement
from data_structure.clearing_all.clearing_dowload_statement import ClearDownloadStatement

zfb_path = [
    (Constants.STATEMENT.dlb_path, 'dlb', Constants.CHANNEL.dlb),
    (Constants.STATEMENT.qq_path, 'qq', Constants.CHANNEL.qq),
    (Constants.STATEMENT.wx_path, 'wx', Constants.CHANNEL.wx),
    (Constants.STATEMENT.yl_path, 'yl', Constants.CHANNEL.yl),
    (Constants.STATEMENT.cib_path, 'cib', Constants.CHANNEL.cib)]
# ,
log = Logger('ResolvingBillFlow').get_log()


@ddt.ddt
class ResolvingBillFlow(unittest.TestCase):
    """解析对账单，test.csv文件"""

    def setUp(self):
        ClearDownloadStatement.clear_down_load_info()
        ClearDownloadStatement.clear_mch_account_details()

    def tearDown(self):
        FtpConnect().delete_file(self.path_name)
        ClearDownloadStatement.clear_down_load_info()
        ClearDownloadStatement.clear_mch_account_details()
        pass

    # @unittest.skip('测试')
    def test_analyze_statement(self):
        """FTP服务器上无对账单，数据库存在记录时，解析对账单（ftp误删）支付宝"""
        zfb_path = Constants.STATEMENT.none_zfb_path
        self.path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1)).replace('-', '')
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.zfb, self.path_name, yesterday, 'zfb')
        PreconditionDowStatement.statement_analyze_send(yesterday)
        befor_len = PreconditionDowStatement.get_csv_len(zfb_path)
        after_len = PreconditionDowStatement.select_count_mch_details()
        after_into_data = PreconditionDowStatement.select_into_data()
        self.assertEqual(befor_len, after_len, msg='对账单解析数据错误，CSV文件条目数为%s db查询出来的条目数为%s' % (befor_len, after_len))
        self.assertEqual(None, after_into_data, msg='对账单解析标志改变出现错误，预期应该为1,实际为%s' % after_into_data)

    # @unittest.skip('测试')
    @ddt.data(*zfb_path)
    def test_analyze_statement_flow_pass(self, zfb_path):
        """FTP服务器上有对账单，数据库dowloadinfo表中该条记录为0时，解析对账单（正常流程，测试解析数据时是否正确入库）"""
        log.info('开始执行解析%s对账单测试' % (zfb_path[1]))
        self.path_name = FtpConnect().push_file_csv_on_ftp(zfb_path[0])
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1)).replace('-', '')
        PreconditionDowStatement.creat_download_info(zfb_path[2], self.path_name, yesterday, zfb_path[1])
        PreconditionDowStatement.statement_analyze_send(yesterday)
        befor_len = PreconditionDowStatement.get_csv_len(zfb_path[0])
        after_len = PreconditionDowStatement.select_count_mch_details()
        after_into_data = PreconditionDowStatement.select_into_data()
        self.assertEqual(befor_len, after_len,
                         msg='%s对账单解析数据错误，CSV文件条目数为%s db查询出来的条目数为%s' % (zfb_path[1], befor_len, after_len))
        self.assertEqual('1', after_into_data, msg='对账单解析标志改变出现错误，预期应该为1,实际为%s' % after_into_data)

    # @unittest.skip('测试')
    def test_analyze_statement_info_data_true(self):
        """FTP服务器上有对账单，数据库dowloadinfo表中该条记录为1时，解析对账单（正常流程，测试解析完成后是否能重复解析）"""
        zfb_path = Constants.STATEMENT.zfb_path
        self.path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1)).replace('-', '')
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.zfb, self.path_name, yesterday, 'zfb')
        PreconditionDowStatement.update_into_data()
        PreconditionDowStatement.statement_analyze_send(yesterday)
        after_len = PreconditionDowStatement.select_count_mch_details()
        after_into_data = PreconditionDowStatement.select_into_data()
        self.assertEqual(0, after_len, msg='对账单解析数据错误，CSV文件条目数为%s db查询出来的条目数为%s' % (0, after_len))
        self.assertEqual('1', after_into_data, msg='对账单解析标志改变出现错误，预期应该为1,实际为%s' % after_into_data)

    # @unittest.skip('测试')
    def test_analyze_statement_two_channel_zfb(self):
        """FTP服务器上存在两条相同渠道的对账单（多个通道商户号同一渠道解析测试）# 每个渠道都要覆盖 验证解析完成后入库数据正确"""
        zfb_path = Constants.STATEMENT.zfb_path
        zfb2_path = Constants.STATEMENT.zfb2_path
        self.path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        self.path2_name = FtpConnect().push_file_csv_on_ftp(zfb2_path)
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1)).replace('-', '')
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.zfb, self.path_name, yesterday, 'zfb')
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.zfb2, self.path2_name, yesterday, 'zfb',
                                                     id='99998')
        PreconditionDowStatement.statement_analyze_send(yesterday)
        befor_len = PreconditionDowStatement.get_csv_len(zfb_path) + PreconditionDowStatement.get_csv_len(zfb2_path)
        after_len = PreconditionDowStatement.select_count_mch_details()
        after_into_data = PreconditionDowStatement.select_into_data()
        self.assertEqual(befor_len, after_len, msg='对账单解析数据错误，CSV文件条目数为%s db查询出来的条目数为%s' % (befor_len, after_len))
        self.assertEqual('1', after_into_data, msg='对账单解析标志改变出现错误，预期应该为1,实际为%s' % after_into_data)
        FtpConnect().delete_file(self.path2_name)


if __name__ == '__main__':
    unittest.main()
