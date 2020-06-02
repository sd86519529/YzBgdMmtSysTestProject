import requests
import datetime

from common.ftp_connect import FtpConnect
from data_structure.sql_save import SqlSave


class PreconditionDowStatement(object):
    """
    下载对账单数据准备类
    1.
    """

    @staticmethod
    def send_request(day='def'):
        """发起请求下载对账单,默认为昨天"""
        if day.__eq__('def'):
            yesterday = str(datetime.date.today() - datetime.timedelta(days=1)).replace('-', '')
        else:
            yesterday = day
        url = 'http://172.16.202.160:3054/handMovement/getDownLoad.htm?billDate=%s' % yesterday
        re = requests.get(url=url)
        print(re.text)

    @staticmethod
    def get_csv_name_from_db():
        """从数据库获取拉取对账单的数据"""
        csv_name_tuple = SqlSave.select_download_url()
        if len(csv_name_tuple) == 0:
            return [], [], 0
        csv_name_list = [i[0] for i in csv_name_tuple]
        csv_type_list = [i[1] for i in csv_name_tuple]
        return csv_name_list, csv_type_list, len(csv_name_tuple)

    @staticmethod
    def get_file_number_for_ftp():
        """获取ftp的数量"""
        file_list, file_number = FtpConnect().get_dir_list()
        return file_list, file_number

    @staticmethod
    def get_file_list_size(file_list):
        file_size_list = list()
        for file_name in file_list:
            size = FtpConnect().get_file_size(file_name)
            file_size_list.append(size)
        return file_size_list

    @staticmethod
    def creat_download_info(channel, download_url, bill_data, typ, id='99999'):
        """创建解析对账单的数据"""
        SqlSave.insert_download_info(channel, download_url, bill_data, typ, id=id)

    @staticmethod
    def select_count_mch_details():
        """查看解析对账单有多少条数据"""
        result = SqlSave.select_count_mch_details()
        return result

    @staticmethod
    def statement_analyze_send(day='20200519'):
        """解析对账单"""
        url = 'http://172.16.202.160:3054/handMovement/resolvingBills.htm?billDate=%s' % day
        re = requests.get(url=url)
        print(re.text)

    @staticmethod
    def get_csv_len(zfb_path):
        """获取csv除去表头的行数"""
        with open(zfb_path, 'r') as f:
            csv_len = len(f.readlines()) - 1
        return csv_len

    @staticmethod
    def select_into_data():
        """获取对账单是否解析标志 None为没有解析 1为已经解析"""
        result = SqlSave.select_into_data()
        return result

    @staticmethod
    def update_into_data():
        """更新对账单解析标识为已解析"""
        SqlSave.update_into_data()

    @staticmethod
    def recondition():
        """发起对账"""
        url = 'http://172.16.202.160:3054/handMovement/recondition.htm?billDate=20200519'
        requests.get(url=url)


if __name__ == '__main__':
    # yesterday = str(datetime.date.today() - datetime.timedelta(days=1)).replace('-', '')
    PreconditionDowStatement.statement_analyze_send('20200521')
    # url = 'http://172.16.202.160:3064/handMovement/getDownLoad.htm?billDate=%s' % '20200521'
    # re = requests.get(url=url)
    # print(re.text)
