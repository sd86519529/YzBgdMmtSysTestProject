"""
1.添加对账记录、下载对账单记录、子商户记账数据
2.记录固定存管户和在途账户金额
3.执行结算定时器
http://172.16.202.160:3054/handMovement/reconditionAccountInfo.htm?billDate=20200101
4.查看his_mch_accnt_keep表的数据是否正确
5.执行入账定时器
http://172.16.202.160:3054/handMovement/settle?today=2020-06-01
6.对比存管户和在途账户的金额变动是否正确
7.查看子商户的可结算余额是否正确添加
8.清除数据
"""
import unittest
from data_structure.clearing_all.clearing_reconciliation import ClearingReconciliation
from data_structure.clearing_all.clearing_settle import ClearingSettle
from data_structure.handle import Handle
from data_structure.precodition_all.precodition_settle import PrecoditionSettle
from model.creat_reconciliation import CreatReconciliation


class MachSettle(unittest.TestCase):

    def setUp(self):
        CreatReconciliation().zfb_in_transit_true_data()
        PrecoditionSettle.precondition_settle()

    def test_settle(self):
        PrecoditionSettle().reconditionAccountInfo()
        Handle().machaccnt_settle_handle_assert(self)

    def tearDown(self):
        ClearingReconciliation.clearing_pay_refund()
        ClearingSettle.settle_all_clear()


if __name__ == '__main__':
    unittest.main()