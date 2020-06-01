from script.public import *
import requests
import time

time = int(time.time())
biz_type = 'submerchant.add'
merchant_id = '80000001'
sign_time = get_time_str()

mch_accnt_no = 'T0020191216201443099999'
account_type = 'PERSONAL_COMMERCIAL'
wechat_category = 'a1'  # 快餐
alipay_category = 'a1'  # chaoshi
merchant_name = '靳伟测试'
province = '浙江省'
city = '杭州市'
area = '滨江区'
address = '东方通讯科技园4号楼'
telphone = '17746847259'
email = '2561134773@qq.com'
legal_person = '靳伟'
customer_telphone = '17746847259'
responsible_person = '靳伟'
responsible_person_phone = '17746847259'
responsible_idcard_number = '610525199504280018'
responsible_idcard_startdate = '2020-02-02'
responsible_idcard_enddate = '2020-02-03'
idcard_picture_fron = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1589863334129&di=8226424bf1d9dfcdbe1cf8e762567180&imgtype=0&src=http%3A%2F%2Fimg3.tbcdn.cn%2Ftfscom%2Fi2%2F101742512%2FTB2x7C0nFXXXXbsXpXXXXXXXXXX_%2521%2521101742512.jpg'
idcard_picture_back = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1589863334129&di=8226424bf1d9dfcdbe1cf8e762567180&imgtype=0&src=http%3A%2F%2Fimg3.tbcdn.cn%2Ftfscom%2Fi2%2F101742512%2FTB2x7C0nFXXXXbsXpXXXXXXXXXX_%2521%2521101742512.jpg'
business_license = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1589863334129&di=8226424bf1d9dfcdbe1cf8e762567180&imgtype=0&src=http%3A%2F%2Fimg3.tbcdn.cn%2Ftfscom%2Fi2%2F101742512%2FTB2x7C0nFXXXXbsXpXXXXXXXXXX_%2521%2521101742512.jpg'
facade_picture = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1589863334129&di=8226424bf1d9dfcdbe1cf8e762567180&imgtype=0&src=http%3A%2F%2Fimg3.tbcdn.cn%2Ftfscom%2Fi2%2F101742512%2FTB2x7C0nFXXXXbsXpXXXXXXXXXX_%2521%2521101742512.jpg'
bank_account_license = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1589863334129&di=8226424bf1d9dfcdbe1cf8e762567180&imgtype=0&src=http%3A%2F%2Fimg3.tbcdn.cn%2Ftfscom%2Fi2%2F101742512%2FTB2x7C0nFXXXXbsXpXXXXXXXXXX_%2521%2521101742512.jpg'
business_license_number = 'yingyezhizhaobianhao'
business_license_startdate = '2020-02-02'
business_license_enddate = '2020-02-03'
account_code = '6210985961000138330'
account_name = '张运珍'
bank_name = '中国邮政储蓄银行股份有限公司'
branch_name = '吉林省长春市宽城区支行'
bank_province = '黑龙江省'
bank_city = '黑龙江省绥化市'

biz_content = {
    'mch_list': [{'mch_accnt_no': mch_accnt_no, 'account_type': account_type, 'wechat_category': wechat_category,
                  'alipay_category': alipay_category, 'merchant_name': merchant_name, 'province': province,
                  'city': city,
                  'area': area, 'address': address, 'telphone': telphone, 'email': email, 'legal_person': legal_person,
                  'customer_telphone': customer_telphone, 'responsible_person': responsible_person,
                  'responsible_person_phone': responsible_person_phone,
                  'responsible_idcard_number': responsible_idcard_number,
                  'responsible_idcard_startdate': responsible_idcard_startdate,
                  'responsible_idcard_enddate': responsible_idcard_enddate, 'idcard_picture_fron': idcard_picture_fron,
                  'idcard_picture_back': idcard_picture_back, 'business_license': business_license,
                  'facade_picture': facade_picture, 'bank_account_license': bank_account_license,
                  'business_license_number': business_license_number,
                  'business_license_startdate': business_license_startdate,
                  'business_license_enddate': business_license_enddate, 'account_code': account_code,
                  'account_name': account_name,
                  'bank_name': bank_name, 'branch_name': branch_name, 'bank_province': bank_province,
                  'bank_city': bank_city}]}

data = {'merchant_id': merchant_id, 'timestamp': time, 'biz_type': biz_type, 'biz_content': biz_content}
print(data)
print(type(data))
print(sign_time)
sign = get_sign(data, sign_time, token='a4147fb821c24fc0bc8275c7e5d09f8d')
data = json.dumps(data, ensure_ascii=False)
data = {'data': data, 'sign': sign}
print(data)
url = 'http://merchant.visastandards.com/gclients'
re = requests.post(url=url, data=data)
print(re.text)
