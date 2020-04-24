import json
from common.config_manager import ConfigManager
from common.constants import Constants
from data_structure.sql_save import SqlSave


class MachAntWithdrawUp(object):
    """构造预期结果"""

    def __init__(self, after_treatment_data):
        self.after_treatment_data = after_treatment_data

    def amt_expected_results(self, is_borrow_money, is_service_charge, type, **kwargs):
        """
        需要：1.商户类型 mch_sub_4  PROFIT_1
             2.提现金额 self.get_for_after_treatment_data('amount')
             3.预期or实际 type 为True 预期 为False 实际
             4.是否借准备金 is_borrow_money
             5.是否有手续费 is_service_charge
             子商户提现扣减余额，可结算余额，  存管户扣减余额
             非回退的情况下 查询出的子商户余额和可结算余额-amount为预期结果
                          存管户的账面余额 - amount为预期结果

        """
        result_dict = dict()
        amount = self.get_for_after_treatment_data('amount')  # 拿取提现金额
        self.mch_accnt = self.get_for_after_treatment_data('mch_accnt_no')  # 拿取商户号
        # 构造查询商户
        if is_borrow_money.__eq__(Constants.RESULT.FALSE) and is_service_charge.__eq__(Constants.RESULT.FALSE):
            """不借准备金，无手续费构造预期结果"""
            # 金额构造
            result_dict['depository_amt'] = MachAntWithdrawUp.amt_depository_and_prepay(
                ConfigManager.get_service(Constants.SubMerchant.DEPOSITORY), amount, type)
            result_dict['mch_amt'] = MachAntWithdrawUp.amt_mch_accnt(self.mch_accnt, amount, type)
            result_dict['info_index'] = self.info_assert_amt_mch_accnt(type, **kwargs)
            return result_dict
            # 明细构造
        elif is_borrow_money.__eq__(Constants.RESULT.FALSE) and is_service_charge.__eq__(Constants.RESULT.TRUE):
            """不借准备金,有手续费构造预期结果"""
            result_dict['depository_amt'] = MachAntWithdrawUp.amt_depository_and_prepay(
                ConfigManager.get_service(Constants.SubMerchant.DEPOSITORY), amount, type, is_service_charge)
            result_dict['mch_amt'] = MachAntWithdrawUp.amt_mch_accnt(self.mch_accnt, amount, type)
            result_dict['info_index'] = self.info_assert_amt_mch_accnt(type, **kwargs)
            if self.mch_accnt == ConfigManager.get_service(Constants.SubMerchant.MUCSUB['mucsub_4']):
                result_dict['profit_amt'] = MachAntWithdrawUp.amt_mch_profit(
                    ConfigManager.get_service(Constants.SubMerchant.PROFIT['profit_1']), amount, type)
                return result_dict
            return result_dict

        elif is_borrow_money.__eq__(Constants.RESULT.TRUE) and is_service_charge.__eq__(Constants.RESULT.TRUE):
            """借准备金，有手续费构造预期结果"""
            result_dict['depository_amt'] = MachAntWithdrawUp.amt_depository_and_prepay(
                ConfigManager.get_service(Constants.SubMerchant.DEPOSITORY), amount, type, is_service_charge)
            result_dict['prepay_amt'] = MachAntWithdrawUp.amt_prepay(
                ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_1']), self.mch_accnt, amount, type)
            result_dict['mch_amt'] = MachAntWithdrawUp.amt_mch_accnt(self.mch_accnt, amount, type)
            result_dict['info_index'] = self.info_assert_amt_mch_accnt(type, **kwargs)
            if self.mch_accnt == ConfigManager.get_service(Constants.SubMerchant.MUCSUB['mucsub_4']):
                result_dict['profit_amt'] = MachAntWithdrawUp.amt_mch_profit(
                    ConfigManager.get_service(Constants.SubMerchant.PROFIT['profit_1']), amount, type)
                return result_dict
            return result_dict
        else:
            """借准备金，无手续费构造预期结果"""
            result_dict['depository_amt'] = MachAntWithdrawUp.amt_depository_and_prepay(
                ConfigManager.get_service(Constants.SubMerchant.DEPOSITORY), amount, type)
            result_dict['prepay_amt'] = MachAntWithdrawUp.amt_prepay(
                ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_1']), self.mch_accnt, amount, type)
            result_dict['mch_amt'] = MachAntWithdrawUp.amt_mch_accnt(self.mch_accnt, amount, type)
            result_dict['info_index'] = self.info_assert_amt_mch_accnt(type, **kwargs)
            return result_dict

    @staticmethod
    def timer_expected_results(type, *args):
        """校验定时器处理提现数据 type 为true 为预期， flase为实际 结构为 withdraw_status,status,remark"""
        if type:
            result_tuple = args
        else:
            result_tuple = SqlSave.select_withdraw_and_status()
        print(result_tuple)
        return result_tuple

    def get_for_after_treatment_data(self, key):
        data = self.after_treatment_data['data']['biz_content']
        if not isinstance(data, dict):
            data = json.loads(data)
        return data[key]

    @staticmethod
    def amt_depository_and_prepay(mch, amount, Type, fix=False):
        """存管户计算"""
        amt = SqlSave.select_remain_amt(mch)  # 根据商户号查询余额
        fix_amount = SqlSave.select_fix_poundage()  # 查询手续费
        if Type:
            if fix:
                result_amt = int(amt[0][0]) - int(amount) + int(fix_amount)
            else:
                result_amt = int(amt[0][0]) - int(amount)
            return result_amt
        return amt[0][0]

    @staticmethod
    def amt_prepay(mch_prepay, mch_accnt, amount, Type):
        """准备金计算"""
        amt = SqlSave.select_remain_amt(mch_prepay)  # 根据商户号查询余额
        set = SqlSave.select_settled_amt(mch_accnt)  # 查询结算余额
        set_amt = ((0,),) if int(set[0][0]) <= 0 else set
        fix_amount = SqlSave.select_fix_poundage()  # 查询手续费
        if Type:
            result_amt = int(amt[0][0]) - (int(amount) - int(set_amt[0][0]) - int(fix_amount))
            return result_amt
        return amt[0][0]

    @staticmethod
    def amt_mch_accnt(mch, amount, Type):
        """子商户或分润计算  fix 是否有手续费，type是否为预期结果"""
        amt = SqlSave.select_remain_amt(mch)
        set_amt = SqlSave.select_settled_amt(mch)
        if Type:
            result_amt = int(amt[0][0]) - int(amount)
            result_set_amt = int(set_amt[0][0]) - int(amount)
            if int(set_amt[0][0]) <= 0:
                return result_amt, set_amt[0][0]
            if int(result_set_amt) < 0:
                return result_amt, 0
            return result_amt, result_set_amt
        return amt[0][0], set_amt[0][0]

    @staticmethod
    def amt_mch_profit(mch, amount, Type):
        """分润商户增加手续费计算"""
        amt = SqlSave.select_remain_amt(mch)
        set_amt = SqlSave.select_settled_amt(mch)
        fix_amount = SqlSave.select_fix_poundage()  # 查询手续费
        if Type:
            result_amt = int(amt[0][0]) + int(fix_amount)
            result_set_amt = int(set_amt[0][0]) + int(fix_amount)
            print('查询出来的amt::%s' % amt)
            print('查询出来的可结算余额::%s' % set_amt)
            print('传入的提现金额::%s' % amount)
            print('子商户或分润计算 amt+amount%s' % result_amt)
            return result_amt, result_set_amt
        return amt[0][0], set_amt[0][0]

    def info_assert_amt_mch_accnt(self, Type, **kwargs):
        """
        子商户或分润明细预期结果生成
        with_draw_info_index  提现明细数量
        mch_accnt_info_index  提现账户明细数量
        his_settled_amount_index 结算金额明细数量
        profit_index 分润账户明细数量
        propay_index 准备金账户明细数量
        """
        if Type:
            dic = MachAntWithdrawUp.info_assert_kwargs()
            dic['with_draw_info_index'] = kwargs['with_draw_info_index']  # 提现明细数量
            dic['mch_accnt_info_index'] = kwargs['mch_accnt_info_index']  # 提现账户明细数量
            dic['his_settled_amount_index'] = kwargs['his_settled_amount_index']  # 结算金额记录明细数量
            dic['profit_index'] = kwargs['profit_index']  # 分润账户明细数量
            dic['propay_index'] = kwargs['propay_index']  # 准备金账户明细数量
            return dic
        table_name_list = [Constants.TableName.WITH_DRAW_INFO, Constants.TableName.HIS_ACCNT_MCH_SUB,
                           Constants.TableName.HIS_SETTLED_AMOUNT, Constants.TableName.HIS_ACCNT_PROFILE,
                           Constants.TableName.HIS_ACCNT_PREPAY]
        dic_key_list = ['with_draw_info_index', 'mch_accnt_info_index', 'his_settled_amount_index', 'profit_index',
                        'propay_index']
        dic = MachAntWithdrawUp.info_assert_kwargs()
        for index in range(len(table_name_list)):
            result = SqlSave.mch_select_info(table_name_list[index])
            if len(result) == 0:
                dic[dic_key_list[index]] = ''
            dic[dic_key_list[index]] = len(result)
        return dic

    @staticmethod
    def info_assert_kwargs():
        """生成明细比对kwargs"""
        dic = {'with_draw_info_index': '', 'mch_accnt_info_index': '', 'his_settled_amount_index': '',
               'profit_index': '', 'propay_index': ''}
        return dic
