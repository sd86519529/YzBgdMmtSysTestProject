class Constants(object):
    """静态资源管理类"""

    class UserAgent:
        CHROME = "USER_AGENT.CHROME_USER_AGENT"

    class MD5Token:
        SW = 'MD5TOKEN.JI0'  # 顺网
        CS = 'MD5TOKEN.BUu'  # 测试

    class Merchant:
        CS = 'MERCHANT.MCHNO'  # 测试商户

    class SubMerchant:
        MUCSUB = {'mucsub_1': 'SUBMERCHANTS.MUCSUB_1', 'mucsub_2': 'SUBMERCHANTS.MUCSUB_2',
                  'mucsub_3': 'SUBMERCHANTS.MUCSUB_3'}  # 商户子商户

        PROFIT = {'profit_1': 'SUBMERCHANTS.PROFIT_1', 'profit_2': 'SUBMERCHANTS.PROFIT_2'}  # 商户分润商户

        PREPAY = {'prepay_1': 'SUBMERCHANTS.PREPAY_1', 'prepay_2': 'SUBMERCHANTS.PREPAY_2'}  # 准备金账户

    class HOST:
        TEST = 'HOST.TEST'  # 测试环境

    class EXL:
        PAY = 'MCHACCNT_PAY_DISPATCH'  # 记账用例储存管理
        REFUND = 'MCHACCNT_REFUND_DISPATCH'  # 退款用例储存管理
        PROMOTION = 'MCHACCNT_PROMOTION_DISPATCH'  # 活动记账用例储存管理
        PROMOTION_REFUND = 'MCHACCNT_PROMOTION_REFUND_DISPATCH'  # 活动退款记账用例储存管理

    class TableName:
        HIS_ACCNT_MCH_SUB = 'his_accnt_mch_sub'  # 子商户表
        HIS_ACCNT_PROFILE = 'his_accnt_profile'  # 分润账户表
        HIS_ACCNT_ONWAY = 'his_accnt_onway'  # 在途账户表
        HIS_ACCNT_PREPAY = 'his_accnt_prepay'  # 准备金明细表

    class RESULT:
        TRUE = True
        FALSE = False

    class CHARGE:  # 是否开启子商户承担手续费
        TRUE = '2'
        FALSE = '1'

    class PRE_DATA:
        PRO_REFUND_DATA = {"请求类型": '',
                           "data": {
                               "biz_content": {"trans_no": "MH20181229115220NBUu", "trans_time": "2020-01-11 14:35:41",
                                               "split_accnt_detail": [
                                                   {"order_no": "test10", "amount": 1000, "dispatch_event": "coupon",
                                                    "mch_accnt_no": "T0020200303191941000000"},
                                                   {"order_no": "test11", "amount": 1000, "dispatch_event": "coupon",
                                                    "mch_accnt_no": "T0020181229184441000000"}]},
                               "biz_type": "mchaccnt.promotion.pay.dispatch",
                               "out_trans_no": "225295c2068ae5405cada7edf1670749a6", "sign_type": "MD5",
                               "timestamp": "20191028022240", "mch_no": "MH20181229115220NBUu"}}
