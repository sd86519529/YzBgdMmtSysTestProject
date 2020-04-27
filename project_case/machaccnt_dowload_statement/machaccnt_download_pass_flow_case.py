import unittest
import datetime
from data_structure.precodition_all.precondition_dowload_statement import PreconditionDowStatement
from data_structure.clearing_all.clearing_dowload_statement import ClearDownloadStatement
from data_structure.handle_all.handle_dowload_statement import HandleDowStatement
from model.download_statement_model import DownloadStatement


class MachDownStatement(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        ClearDownloadStatement.clear_ftp_file()
        ClearDownloadStatement.clear_down_load_info()

    # @unittest.skip('测试')
    def test_dow_load_statement(self):
        """拉取对账单校验"""
        file_list, file_number = PreconditionDowStatement.get_file_number_for_ftp()  # 请求前获取对账单的数量和名称
        PreconditionDowStatement.send_request()  # 发起下载对账单请求，拉取6种不同渠道的对账单  day默认为前一天
        file_list_af, file_number_af = PreconditionDowStatement.get_file_number_for_ftp()  # 请求后获取对账单的数量和名称
        end_list = [i for i in file_list_af if i not in file_list]  # 去重后的名称
        befor_data = DownloadStatement.info_assert_kwargs(ftp_name=end_list, ftp_number=6, db_number=6,
                                                          db_type=['cib', 'yl', 'zfb', 'wx', 'qq', 'dlb'])
        end_file_number = int(file_number_af) - int(file_number)  # 增加对账单的数量
        csv_name_list_af, csv_type_list_af, file_number_after = PreconditionDowStatement.get_csv_name_from_db()  # 请求后的名称列表和类型列表
        file_size_list = PreconditionDowStatement.get_file_list_size(csv_name_list_af)
        after_data = DownloadStatement.info_assert_kwargs(ftp_name=csv_name_list_af, ftp_number=end_file_number,
                                                          db_number=file_number_after, db_type=csv_type_list_af,
                                                          file_size=file_size_list)
        HandleDowStatement.assert_dow_statement(self, **{'befor_data': befor_data, 'after_data': after_data})

    # @unittest.skip('测试')
    def test_dow_load_statement_tomorrow(self):
        """拉取对账单校验  日期为明天"""
        file_list, file_number = PreconditionDowStatement.get_file_number_for_ftp()  # 请求前获取对账单的数量和名称
        tomorrow = str(datetime.date.today() + datetime.timedelta(days=1)).replace('-', '')
        PreconditionDowStatement.send_request(day=tomorrow)  # 发起下载对账单请求，拉取6种不同渠道的对账单  day为明天
        file_list_af, file_number_af = PreconditionDowStatement.get_file_number_for_ftp()  # 请求后获取对账单的数量和名称
        end_list = [i for i in file_list_af if i not in file_list]  # 去重后的名称
        befor_data = DownloadStatement.info_assert_kwargs(ftp_name=end_list, ftp_number=0, db_number=0, db_type=[])
        end_file_number = int(file_number_af) - int(file_number)  # 增加对账单的数量
        csv_name_list_af, csv_type_list_af, file_number_after = PreconditionDowStatement.get_csv_name_from_db()  # 请求后的名称列表和类型列表
        file_size_list = PreconditionDowStatement.get_file_list_size(csv_name_list_af)
        after_data = DownloadStatement.info_assert_kwargs(ftp_name=csv_name_list_af, ftp_number=end_file_number,
                                                          db_number=file_number_after, db_type=csv_type_list_af,
                                                          file_size=file_size_list)
        HandleDowStatement.assert_dow_statement(self, **{'befor_data': befor_data, 'after_data': after_data})

    # @unittest.skip('测试')
    def test_dow_load_statement_repeat(self):
        """重复拉取对账单校验"""
        file_list, file_number = PreconditionDowStatement.get_file_number_for_ftp()  # 请求前获取对账单的数量和名称
        PreconditionDowStatement.send_request()  # 发起下载对账单请求，拉取6种不同渠道的对账单  day默认为前一天
        PreconditionDowStatement.send_request()  # 第二次发起下载对账单请求，拉取6种不同渠道的对账单  day默认为前一天
        file_list_af, file_number_af = PreconditionDowStatement.get_file_number_for_ftp()  # 请求后获取对账单的数量和名称
        end_list = [i for i in file_list_af if i not in file_list]  # 去重后的名称
        befor_data = DownloadStatement.info_assert_kwargs(ftp_name=end_list, ftp_number=6, db_number=6,
                                                          db_type=['cib', 'yl', 'zfb', 'wx', 'qq', 'dlb'])
        end_file_number = int(file_number_af) - int(file_number)  # 增加对账单的数量
        csv_name_list_af, csv_type_list_af, file_number_after = PreconditionDowStatement.get_csv_name_from_db()  # 请求后的名称列表和类型列表
        file_size_list = PreconditionDowStatement.get_file_list_size(csv_name_list_af)
        after_data = DownloadStatement.info_assert_kwargs(ftp_name=csv_name_list_af, ftp_number=end_file_number,
                                                          db_number=file_number_after, db_type=csv_type_list_af,
                                                          file_size=file_size_list)
        HandleDowStatement.assert_dow_statement(self, **{'befor_data': befor_data, 'after_data': after_data})

    def test_dow_load_statement_mouth(self):
        """拉取一个月之前的对账单校验"""
        file_list, file_number = PreconditionDowStatement.get_file_number_for_ftp()  # 请求前获取对账单的数量和名称
        mouth = str(datetime.date.today() - datetime.timedelta(days=30)).replace('-', '')
        PreconditionDowStatement.send_request(day=mouth)  # 发起下载对账单请求，拉取6种不同渠道的对账单  day默认为前一天
        file_list_af, file_number_af = PreconditionDowStatement.get_file_number_for_ftp()  # 请求后获取对账单的数量和名称
        end_list = [i for i in file_list_af if i not in file_list]  # 去重后的名称
        befor_data = DownloadStatement.info_assert_kwargs(ftp_name=end_list, ftp_number=6, db_number=6,
                                                          db_type=['cib', 'yl', 'zfb', 'wx', 'qq', 'dlb'])
        end_file_number = int(file_number_af) - int(file_number)  # 增加对账单的数量
        csv_name_list_af, csv_type_list_af, file_number_after = PreconditionDowStatement.get_csv_name_from_db()  # 请求后的名称列表和类型列表
        file_size_list = PreconditionDowStatement.get_file_list_size(csv_name_list_af)
        after_data = DownloadStatement.info_assert_kwargs(ftp_name=csv_name_list_af, ftp_number=end_file_number,
                                                          db_number=file_number_after, db_type=csv_type_list_af,
                                                          file_size=file_size_list)
        HandleDowStatement.assert_dow_statement(self, **{'befor_data': befor_data, 'after_data': after_data})


if __name__ == '__main__':
    unittest.main()
