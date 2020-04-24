class Constants(object):
    """静态资源管理类"""

    class MockUrl:
        SUCCESS = 'http://172.16.202.160:10008/s'
        FAIL = 'http://172.16.202.160:10008/f'
        WAIT = 'http://172.16.202.160:10008/w'
        TIME_OUT = 'http://47.98.144.54:800'
        DEFAULT = 'http://47.98.144.54:8007'
        SELECT_SUCCESS = 'http://172.16.202.160:10008/ss'
        SELECT_NONE = 'http://172.16.202.160:10008/sn'
        SELECT_WAIT = 'http://172.16.202.160:10008/sw'
        SELECT_FAIL = 'http://172.16.202.160:10008/sf'
        SELECT_LONG = 'http://172.16.202.160:10008/fl'

    class PutBug:
        BUTTON = 'CD_PUTBUG.BUTTON'  # 是否提交bug到禅道

    class CdAdmin:
        JW = {'username': 'CD_CONFIG.jw_username', 'password': 'CD_CONFIG.jw_password'}

    class UserAgent:
        CHROME = "USER_AGENT.CHROME_USER_AGENT"

    class MD5Token:
        SW = 'MD5TOKEN.JI0'  # 顺网
        CS = 'MD5TOKEN.BUu'  # 测试

    class Merchant:
        CS = 'MERCHANT.MCHNO'  # 测试商户

    class SubMerchant:
        MUCSUB = {'mucsub_1': 'SUBMERCHANTS.MUCSUB_1', 'mucsub_2': 'SUBMERCHANTS.MUCSUB_2',
                  'mucsub_3': 'SUBMERCHANTS.MUCSUB_3', 'mucsub_4': 'SUBMERCHANTS.MUCSUB_4'}  # 商户子商户

        PROFIT = {'profit_1': 'SUBMERCHANTS.PROFIT_1', 'profit_2': 'SUBMERCHANTS.PROFIT_2'}  # 商户分润商户

        PREPAY = {'prepay_1': 'SUBMERCHANTS.PREPAY_1', 'prepay_2': 'SUBMERCHANTS.PREPAY_2'}  # 准备金账户

        DEPOSITORY = 'SUBMERCHANTS.DEPOSITORY'

    class HOST:
        TEST = 'HOST.TEST'  # 测试环境
        TIMER_TEST = 'HOST.TIMER_TEST' # 提现定时器触发

    class EXL:
        PAY = 'MCHACCNT_PAY_DISPATCH'  # 记账用例储存管理
        REFUND = 'MCHACCNT_REFUND_DISPATCH'  # 退款用例储存管理
        PROMOTION = 'MCHACCNT_PROMOTION_DISPATCH'  # 活动记账用例储存管理
        PROMOTION_REFUND = 'MCHACCNT_PROMOTION_REFUND_DISPATCH'  # 活动退款记账用例储存管理
        WITHDRAW = 'MCHACCNT_WITHDRAW'  # 提现用例储存管理

    class TableName:
        HIS_ACCNT_MCH_SUB = 'his_accnt_mch_sub'  # 子商户表
        HIS_ACCNT_PROFILE = 'his_accnt_profile'  # 分润账户表
        HIS_ACCNT_ONWAY = 'his_accnt_onway'  # 在途账户表
        HIS_ACCNT_PREPAY = 'his_accnt_prepay'  # 准备金明细表
        WITH_DRAW_INFO = 'with_draw_info'  # 提现明细表
        HIS_SETTLED_AMOUNT = 'his_settled_amount'  # 结算金额明细记录表
        BANK_CARD = 'bank_card'  # 商户银行卡信息表

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
                                                    "mch_accnt_no": "T0020181229115338000002"}]},
                               "biz_type": "mchaccnt.promotion.pay.dispatch",
                               "out_trans_no": "225295c2068ae5405cada7edf1670749a6", "sign_type": "MD5",
                               "timestamp": "20191028022240", "mch_no": "MH20181229115220NBUu"}}
