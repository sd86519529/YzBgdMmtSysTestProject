from data_structure.precodition_all.precondition_dowload_statement import PreconditionDowStatement
from common.ftp_connect import FtpConnect
from data_structure.sql_save import SqlSave


class ClearDownloadStatement(object):
    """清理对账单拉去的数据"""

    @staticmethod
    def clear_ftp_file():
        """清理ftp的文件"""
        f = FtpConnect()
        csv_name_list, csv_type_list, index = PreconditionDowStatement.get_csv_name_from_db()
        if len(csv_name_list) == 0:
            return
        for name in csv_name_list:
            f.delete_file(name)

    @staticmethod
    def clear_down_load_info():
        """清理download_info的数据"""
        SqlSave.delete_download_info()

    @staticmethod
    def clear_mch_account_details():
        """清理解析表里的测试数据"""
        SqlSave.delete_mch_account_details()
