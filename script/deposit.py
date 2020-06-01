from script.public import *
import requests

trans_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

biz_type = "mchaccnt.dispatch"
trans_channel = '2051'
trans_no = 'TRANS' + get_strip_id()
biz_content = {"split_accnt_detail":
                   [{"order_no": 'ID1' + get_strip_id(), "trans_no": trans_no, "trans_channel": trans_channel,
                     "trans_time": trans_time, "amount": "100",
                     "card_no": "62148354983258", "dispatch_event": "pay",
                     "mch_accnt_no": get_sub_mch('mucsub_1'), "dispatch_type": "1"},
                    {"order_no": 'ID2' + get_strip_id(), "trans_no": trans_no,
                     "trans_channel": trans_channel, "trans_time": trans_time, "amount": "50",
                     "dispatch_event": "transfer", "mch_accnt_no": get_sub_mch('mucsub_1'), "dispatch_type": "2"},
                    {"order_no": 'ID3' + get_strip_id(), "trans_no": trans_no, "trans_channel": trans_channel,
                     "trans_time": trans_time, "amount": "50", "dispatch_event": "transfer",
                     "mch_accnt_no": get_sub_mch('mucsub_2'), "dispatch_type": "1"}]}
data = public_data(biz_type, **biz_content)
re = requests.post(url=get_url(), data=data)
print(re.text)
