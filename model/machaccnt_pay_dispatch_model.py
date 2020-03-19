from data_structure.sql_save import SqlSave
from common.base import Base
import json


class MachPayDispatchDown(SqlSave):
    def __init__(self, table_name, mch_ant_no, trans_no, event):
        """
        事后调用，查询到需要对比的数据库字段  Down请求后的数据库实际结果准备
        1.若表名有多张则传入 list形式
        2.会通过 select_amt_info 去不同的子表中查询出 金额 事前 时候等数据
        3.会通过 select_remain_amt 表中查询出该子商户现有金额
        :param table_name: 表名
        :param mch_ant_no: 子商户号
        :param trans_no: 交易流水号
        settled_ant: 可结算金额{'mch_ant_no[mc_number]':'settled_ant'}
        mch_ant: 账面金额{'mch_ant_no[mc_number]':'mch_ant'}
        """
        if isinstance(table_name, list):
            self.amt_info = dict()
            for tb_number in range(len(table_name)):
                info = self.select_amt_info(table_name[tb_number], trans_no, event)
                self.amt_info[table_name[tb_number]] = info
        else:
            self.amt_info = self.select_amt_info(table_name, trans_no, event)

        if isinstance(mch_ant_no, list):
            self.mch_ant = dict()
            self.settled_ant = dict()
            for mc_number in range(len(mch_ant_no)):
                info = self.select_remain_amt(mch_ant_no[mc_number])
                set_info = self.select_settled_amt(mch_ant_no[mc_number])
                self.mch_ant[mch_ant_no[mc_number]] = info
                self.settled_ant[mch_ant_no[mc_number]] = set_info
        else:
            self.mch_ant = self.select_remain_amt(mch_ant_no)
            self.settled_ant = self.select_settled_amt(mch_ant_no)
        # 以上是构造所需要比对的金额

    def __str__(self) -> str:
        return '%s\t%s\t%s' % (self.amt_info, self.mch_ant, self.settled_ant)


class MachPayDispatchUp(object):
    """
    事前调用，查询到需要用到的字段和需要计算的字段 Up请求前的需要字段准备和预期结果准备
    return：trans_no 交易流水号，用来查询对应子商户表的不同金额变化
    return：mch_accnt_no_list list形式 包含不同子商户表的商户号
    return self.trans_amt_dict 和 self.amt_dict 是数据库数据验证所需要的数据
    """

    def __init__(self, exc_data):
        self.mch_act_no_list = []
        self.amt_list = []
        self.oder_no_list = []
        data = exc_data['data']
        if not isinstance(data, dict):
            data = json.loads(exc_data['data'])
        self.trans_no = data.get('biz_content').get('trans_no')  # 获取支付对账请求中的trans_no
        for i in data.get('biz_content').get('split_accnt_detail'):
            self.mch_act_no_list.append(i.get('mch_accnt_no'))
            self.amt_list.append(i.get('amount'))
            self.oder_no_list.append(i.get('order_no'))
        self.trans_amt_dict = Base.add_amt(self.mch_act_no_list, self.amt_list)
        self.amt_dict = Base.merchant_type(self.mch_act_no_list, self.amt_list)

    def __str__(self) -> str:
        return '商户号:%s\t 子商户号：%s\t 子商户总金额预期：%s\t 单个子商户表预期:%s \t 子商户oder_no:%s' % (
            self.trans_no, self.mch_act_no_list, self.trans_amt_dict, self.amt_dict, self.oder_no_list)


if __name__ == '__main__':
    pass
