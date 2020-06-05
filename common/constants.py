class Constants(object):
    """静态资源管理类"""

    class STATEMENT:
        """对账单"""
        big_zfb_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\resolvingbill\zfb_20200426_vuQs6pRk5GFhOfo6Lpzz.csv'  # 过大的对账单(zfb)
        none_zfb_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\resolvingbill\zfb_20200417_6RygDDfSs87Ff7l0Q4xt.csv'  # 空csv文件
        zfb_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\resolvingbill\zfb_20200422_iyUiAEjyWnw4031iDwmp.csv'  # 正常的支付宝对账单文件
        zfb2_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\resolvingbill\zfb_20200422_iyUiAEjyWnw4031iDwml.csv'  # 正常的支付宝对账单文件2
        cib_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\resolvingbill\cib_20200427_7EGLKChvMMQh1tRy3egg.csv'  # 正常的cib对账单文件
        dlb_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\resolvingbill\dlb_20200427_3v8u4AtdJFYp1BoPRZdg.csv'  # 正常的cib对账单文件
        qq_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\resolvingbill\qq_20200427_gez41EKSpWo4zecIhnKf.csv'  # 正常的cib对账单文件
        wx_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\resolvingbill\wx_20200427_DVqfMez6kyIiHHoopdkh.csv'  # 正常的cib对账单文件
        yl_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\resolvingbill\yl_20200427_f7Og5pzCK3DDZ73hFaUa.csv'  # 正常的cib对账单文件

    class RECONCILIATION:
        """对账需要的对账单"""
        false_zfb_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\reconciliation\zfb_20200519_6RygDDfSs87Ff7l0Q4xx.csv'  # 出现问题件的对账单
        true_zfb_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\reconciliation\zfb_20200519_6RygDDfSs87Ff7l0Q4true.csv'  # 支付宝对平的对账单
        false_cib_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\reconciliation\cib_20200427_7EGLKChvMMQh1tRy3exx.csv'
        false_dlb_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\reconciliation\dlb_20200427_3v8u4AtdJFYp1BoPRZdg.csv'
        false_yl_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\reconciliation\yl_20200427_f7Og5pzCK3DDZ73hFaUa.csv'
        false_qq_path = 'G:\YzaoutTestProject\YzAutoTestProject\project_data\\reconciliation\qq_20200427_gez41EKSpWo4zecIhnKf.csv'

    class CREATE:
        """制造对账数据生成列表"""
        # 问题列表生成
        zfb_pay = [['jinweiceshi_zfb_002', '300', 'test01', '300', '2020-05-19 11:33:44', '20251'],
                   ['jinweiceshi_zfb_003', '28000', 'test02', '28000', '2020-05-19 11:33:44', '20251'],
                   ['jinweiceshi_zfb_004', '320', 'test03', '320', '2020-05-19 11:33:44', '20251'],
                   ['jinweiceshi_zfb_005', '30000', 'test04', '30000', '2020-05-19 11:33:44', '20251'],
                   ['jinweiceshi_zfb_009', '300', 'test09', '300', '2020-05-20 11:33:44', '20251'],
                   ['jinweiceshi_zfb_015', '300', 'test15', '300', '2020-05-19 11:33:44', '29999'],
                   ['jinweiceshi_zfb_010', '300', 'test10', '270', '2020-05-19 11:33:44', '20251', 'test14',
                    '30']]

        zfb_refund = [['jinweiceshi_zfb_007', '850', 'test07', '850', '2020-05-19 11:33:44', '20251'],
                      ['jinweiceshi_zfb_008', '650', 'test08', '650', '2020-05-19 11:33:44', '20251'],
                      ['jinweiceshi_zfb_011', '650', 'test11', '650', '2020-05-19 11:33:44', '20251'],
                      ['jinweiceshi_zfb_012', '850', 'test12', '850', '2020-05-20 11:33:44', '20251'],
                      ['jinweiceshi_zfb_016', '850', 'test16', '850', '2020-05-19 11:33:44', '29999'],
                      ['jinweiceshi_zfb_013', '850', 'test13', '750', '2020-05-19 11:33:44', '20251', 'test17',
                       '100']]

        # 对平列表生成
        creat_pay_true_list = ['jinweiceshi_zfb_001', '300', 'test01', '300', '2020-05-19 11:33:44', '20251']

    class CHANNEL:
        zfb = '2017112800223321'
        zfb2 = '2017112800223322'
        cib = '86570015'
        dlb = '10001115631585874067678'
        qq = '1298241301'
        wx = '1520262791'
        yl = '46570003'

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
        TIMER_TEST = 'HOST.TIMER_TEST'  # 提现定时器触发
        TIMER_WITH = 'HOST.TIMER_WITH'  # 还准备金定时器触发

    class EXL:
        PAY = 'MCHACCNT_PAY_DISPATCH'  # 记账用例储存管理
        REFUND = 'MCHACCNT_REFUND_DISPATCH'  # 退款用例储存管理
        PROMOTION = 'MCHACCNT_PROMOTION_DISPATCH'  # 活动记账用例储存管理
        PROMOTION_REFUND = 'MCHACCNT_PROMOTION_REFUND_DISPATCH'  # 活动退款记账用例储存管理
        WITHDRAW = 'MCHACCNT_WITHDRAW'  # 提现用例储存管理
        RESOLIVINGBILL = 'MCHACCNT_RESOLIVINGBILL'

    class TableName:
        HIS_ACCNT_MCH_SUB = 'his_accnt_mch_sub'  # 子商户表
        HIS_ACCNT_PROFILE = 'his_accnt_profile'  # 分润账户表
        HIS_ACCNT_ONWAY = 'his_accnt_onway'  # 在途账户表
        HIS_ACCNT_PREPAY = 'his_accnt_prepay'  # 准备金明细表
        WITH_DRAW_INFO = 'with_draw_info'  # 提现明细表
        HIS_SETTLED_AMOUNT = 'his_settled_amount'  # 结算金额明细记录表
        BANK_CARD = 'bank_card'  # 商户银行卡信息表
        MCH_CHARGE_UP = 'mch_accnt_charge_up'  # 提现还准备金记录表

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
        PAY_DATA = {"请求类型": '',
                    "data": {
                        "biz_content": {"trans_no": "MH20181229115220NBUu", "trans_time": "2020-05-20 17:25:58",
                                        'trans_channel': '20251', 'settle_type': '1', 'trans_amt': '1',
                                        "split_accnt_detail": [
                                            {"order_no": "test10", "amount": 1, "dispatch_event": "pay",
                                             'dispatch_type': '1', "mch_accnt_no": "T0020181229184441000000",
                                             'accnt_amt_before': 1}]},
                        "biz_type": "mchaccnt.pay.dispatch",
                        "out_trans_no": "225295c2068ae5405cada7edf1670749a6", "sign_type": "MD5",
                        "timestamp": "20191028022240", "mch_no": "MH20181229115220NBUu"}}
