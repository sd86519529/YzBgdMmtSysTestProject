import json
import requests
from common.config_manager import ConfigManager
from common.constants import Constants
from model.machaccnt_pay_dispatch_model import MachPayDispatchDown
from data_structure.sql_save import SqlSave


class PreconditionWithdrawal(object):
    """
        本类用于前置条件构造
        对于不同的用例所需要的前置条件进行接口层面的构造准备或sql层面的构造准备
    """

    @staticmethod
    def mct_pay_dispatch_pre(c_obj):
        """
        通过事前准备的查询数据进行查询
        1.返回内容 不同子商户对应的金额{'子商户号':'子商户金额'}
        2.返回内容 不同子商户表中的三个金额 请求前的数值，以及对应的数量 {'表名':查询出来的数据}
        :return:
        """
        result = MachPayDispatchDown([Constants.TableName.HIS_ACCNT_PROFILE, Constants.TableName.HIS_ACCNT_ONWAY,
                                      Constants.TableName.HIS_ACCNT_MCH_SUB], c_obj.mch_act_no_list, c_obj.trans_no,
                                     event='pay')

        return result.amt_info, result.mch_ant

    @staticmethod
    def update_card_name(button):
        """修改银行卡姓名"""
        SqlSave.update_card_name(button)

    @staticmethod
    def mct_update_super_money_pre(is_change):
        """
        是否开启超额提现开关 True为开启
                          False为关闭
        :return:
        """
        SqlSave.update_super_money(is_change)

    @staticmethod
    def mch_update_prepay_amount(amt='1000', set_amt='1000'):
        """
        设置提现准备金账户余额和可结算余额
        :return:
        """
        mch = ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_1'])
        SqlSave.update_amount(amt, set_amt, mch)

    @staticmethod
    def mct_update_amount_pre(unusual_parameter, amt='10000', set_amt='10000',
                              ):
        """
        设置提现专用子商户的余额和可结算余额amt, set_amt
        :return:
        """
        data = unusual_parameter['data']
        if not isinstance(data, dict):
            data = json.loads(data)
        data = data['biz_content']
        if data.get('mch_accnt_no') in Constants.SubMerchant.MUCSUB.keys():
            mch = ConfigManager.get_service(Constants.SubMerchant.MUCSUB[data.get('mch_accnt_no')])
        elif data.get('mch_accnt_no') in Constants.SubMerchant.PROFIT.keys():
            mch = ConfigManager.get_service(Constants.SubMerchant.PROFIT[data.get('mch_accnt_no')])
        else:
            mch = ConfigManager.get_service(Constants.SubMerchant.PREPAY[data.get('mch_accnt_no')])
        SqlSave.update_amount(amt, set_amt, mch)

    @staticmethod
    def mct_promotion_pre(button, all=False):
        """
        在提现时更改备用准备金账户类型为准备金
        :return:
        """
        # 多个准备金账户暂时不管
        if all:
            mch_no_list = [ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_1']),
                           ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_2'])]
        else:
            mch_no_list = [ConfigManager.get_service(Constants.SubMerchant.PREPAY['prepay_1'])]
        for i in mch_no_list:
            SqlSave.update_accnt_type(i, button=button)

    @staticmethod
    def mct_update_amount_for_prepay_pre(amt='10000', set_amt='10000'):
        """
        在提现时更改准备金账户金额，默认为10000
        :return:
        """
        SqlSave.update_amount_for_prepay(amt, set_amt)

    @staticmethod
    def mct_update_acct_type(button=True):
        """
        更改测试商户下分润商户的数量
        button为True   分润商户设置为0
        button为False  分润商户还原
        操作的商户分别为 PROFIT_1   PREPAY_2
        :return:
        """
        SqlSave.mct_update_acct_type(button)

    @staticmethod
    def mch_update_fixed_poundage(number=100, button=True):
        """
        清空fixed_poundage
        或设置费率为100
        :return:
        """
        SqlSave.mch_update_fixed_poundage(button, number)

    @staticmethod
    def mch_update_withdraw_status(number):
        """更改withdraw_status为number"""
        SqlSave.mch_update_withdraw_status(number)

    @staticmethod
    def mch_update_request_num(number):
        """更改request_num"""
        SqlSave.mch_update_request_num(number)

    @staticmethod
    def mch_update_status(number):
        """修改返回成功，失败，或进行中"""
        SqlSave.mch_update_status(number)

    @staticmethod
    def send_deal_withdraw():
        """触发提现"""
        res = requests.post(url=ConfigManager.get_service(Constants.HOST.TIMER_TEST))
        print(res)

    @staticmethod
    def with_draw_info():
        """查看提现结果表的返回"""
        info = SqlSave.mch_select_info('with_draw_info')
        return info[0][13]

    @staticmethod
    def update_pay_url(pay_type):
        """更新提现真实请求的接口，模拟返回"""
        SqlSave.update_pay_url(pay_type)
    # @staticmethod
    # def select_fix_poundage():
    #     """获取提现手续费"""
    #     info = SqlSave.select_fix_poundage()
    #     return info[0][0]


if __name__ == '__main__':
    PreconditionWithdrawal.send_deal_withdraw()
