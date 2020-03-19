class Constants(object):
    """静态资源管理类"""

    class UserAgent:
        CHROME = "USER_AGENT.CHROME_USER_AGENT"

    class MD5Token:
        SW = 'MD5TOKEN.JI0'  # 顺网
        CS = 'MD5TOKEN.BUu'  # 测试

    class Merchant:
        SW = 'MERCHANT.MCHNO'  # 顺网

    class SubMerchant:
        MUCSUB = {'mucsub_1': 'SUBMERCHANTS.MUCSUB_1', 'mucsub_2': 'SUBMERCHANTS.MUCSUB_2',
                  'mucsub_3': 'SUBMERCHANTS.MUCSUB_3'}  # 商户子商户

        PROFIT = {'profit_1': 'SUBMERCHANTS.PROFIT_1', 'profit_2': 'SUBMERCHANTS.PROFIT_2'}  # 商户分润商户

    class HOST:
        TEST = 'HOST.TEST'  # 测试环境

    class EXL:
        PAY = 'MCHACCNT_PAY_DISPATCH'  # 记账用例储存管理
        REFUND = 'MCHACCNT_REFUND_DISPATCH'

    class TableName:
        HIS_ACCNT_MCH_SUB = 'his_accnt_mch_sub'  # 子商户表
        HIS_ACCNT_PROFILE = 'his_accnt_profile'  # 分润账户表
        HIS_ACCNT_ONWAY = 'his_accnt_onway'  # 在途账户表

    class RESULT:
        TRUE = True
        FALSE = False

    class CHARGE:  # 是否开启子商户承担手续费
        TRUE = '2'
        FALSE = '1'
