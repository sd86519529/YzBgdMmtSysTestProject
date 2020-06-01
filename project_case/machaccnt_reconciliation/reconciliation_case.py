import requests
import unittest
import ddt
from common.logger import Logger
from common.read_excle import ReadExl
from common.constants import Constants
from common.ftp_connect import FtpConnect
from common.request_base import RequestBase
from data_structure.handle import Handle
from data_structure.precodition_all.precondition_dowload_statement import PreconditionDowStatement

log = Logger('MachPayDispatch').get_log()

exa_and_approve_list = ReadExl(Constants.EXL.RESOLIVINGBILL, sheet=0).obtain_data()
flow_not_change_pay = ReadExl.screen_case('对账数据准备', exa_and_approve_list)  # 不含手续费流程测试
print(flow_not_change_pay)


@ddt.ddt
class Reconciliation():
    """对账程序 1.mch_account_details 有解析的数据
               2.his_accnt_onway 有在途的数据

    """

    def setUp(self):
        self.send_jizhang()

    def tearDown(self):
        pass

    # @ddt.data(*flow_not_change_pay)
    # def test_send_request(self, flow_not_change_pay):
    #     self.after_treatment_data = Handle.machaccnt_pay_dispatch_handle(flow_not_change_pay)
    #     res, html = RequestBase.send_request(**flow_not_change_pay)  # 发送请求
    #     log.info('本次请求结果为%s' % html)

    def send_reconciliation(self):
        """发起对账"""
        url = 'http://172.16.202.160:3054/handMovement/recondition.htm?billDate=20200519'
        re = requests.get(url=url)
        print(re.text)

    def send_jizhang(self):
        zfb_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\reconciliation\zfb_20200519_6RygDDfSs87Ff7l0Q4xx.csv'
        path_name = FtpConnect().push_file_csv_on_ftp(zfb_path)
        PreconditionDowStatement.creat_download_info(Constants.CHANNEL.zfb, path_name, '20200519', 'zfb')
        PreconditionDowStatement.statement_analyze_send('20200519')


if __name__ == '__main__':
    Reconciliation().send_reconciliation()
