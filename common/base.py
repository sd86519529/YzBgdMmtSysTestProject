import json
import time
from common.constants import Constants
from common.config_manager import ConfigManager
from data_structure.sql_save import SqlSave


class Base(object):
    """该类为一些项目公共方法封装类"""

    @staticmethod
    def creat_time_stamp():
        """
        创建时间戳
        :return: 格式:20200310102135
        """
        tm_sp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).replace('-', '').replace(' ', '').replace(':', '')
        return tm_sp

    @staticmethod
    def add_amt(mch_accnt_no_list, amt_list):
        """传入两个列表，找到第一个列表中重复的元素，将第二个列表对应的金额相加"""
        re_list = []
        result_dict = {}
        amt = 0
        for z in range(len(mch_accnt_no_list)):
            if mch_accnt_no_list[z] in re_list:
                continue
            result_list = [i for i, x in enumerate(mch_accnt_no_list) if x == mch_accnt_no_list[z]]
            if len(result_list) > 1:
                for i in result_list:
                    re_list.append(mch_accnt_no_list[i])
                    amt += int(amt_list[i])
                result_dict[mch_accnt_no_list[z]] = amt
            else:
                result_dict[mch_accnt_no_list[z]] = amt_list[z]
        return result_dict

    @staticmethod
    def merchant_type(mch_accnt_no_list, amt_list):
        """
        将两个list分类成不同的商户类型以key value返回
        制造预期结果，支付记账时返回格式{‘表名’：（mch_accnt_no，金额）}
        """
        result_dict = {}
        mucsub_list = []
        profit_list = []
        comparison_muc_sub_list = []
        comparison_profit_list = []
        for key, value in Constants.SubMerchant.MUCSUB.items():
            comparison_muc_sub_list.append(ConfigManager.get_service(value))
        for key, value in Constants.SubMerchant.PROFIT.items():
            comparison_profit_list.append(ConfigManager.get_service(value))
        for mch_number in range(len(mch_accnt_no_list)):
            if mch_accnt_no_list[mch_number] in comparison_muc_sub_list:
                mucsub_list.append((mch_accnt_no_list[mch_number], amt_list[mch_number]))
            if mch_accnt_no_list[mch_number] in comparison_profit_list:
                profit_list.append((mch_accnt_no_list[mch_number], amt_list[mch_number]))
        result_dict[Constants.TableName.HIS_ACCNT_MCH_SUB] = mucsub_list
        result_dict[Constants.TableName.HIS_ACCNT_PROFILE] = profit_list
        return result_dict

    @staticmethod
    def count_charge(trans_amt, amount):
        # todo:费率的方案暂时没定，到时候需要修改
        """计算手续费   trans_amt订单总金额  amount子商户金额 默认支付渠道29999 费率百分之1"""
        a = SqlSave.select_change()[0][0]
        charge = round(int(trans_amt) * float(a))  # 计算手续费
        print('计算手续费后的金额为', charge)
        return amount - charge

    @staticmethod
    def promotion_count(amt_list, trans_amt_dict, mch_act_no_list):
        amt = 0
        for am in amt_list:
            amt -= int(am)
        trans_amt_dict['T0020181229115338000001'] = amt
        mch_act_no_list.append('T0020181229115338000001')
        return trans_amt_dict, mch_act_no_list

    @staticmethod
    def get_trans_no(exc_data):
        """获取trans_no"""
        data = exc_data['data']
        if not isinstance(data, dict):
            data = json.loads(exc_data['data'])
        trans_no = data.get('biz_content').get('trans_no')  # 获取支付对账请求中的trans_no
        return trans_no


if __name__ == '__main__':
    a = {'123':123}
    print(a.get('222'))
