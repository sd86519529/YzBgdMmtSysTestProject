import json
import requests
import hashlib
from common import logger
from common.constants import Constants
from common.config_manager import ConfigManager

log = logger.Logger('RequestManager').get_log()


class RequestManager(object):
    """请求的实现类"""

    @staticmethod
    def send_requests(**kwargs):
        url = ConfigManager.get_service(Constants.HOST.TEST)  # 请求路由地址
        # todo 关于接口签名认证的方法可以做进一步处理如：直接去数据库查询等。
        headers = {'User-Agent': ConfigManager.get_basic(Constants.UserAgent.CHROME)}  # 请求头默认带浏览器chrome 可配置
        headers = headers if kwargs.get('HEADERS') is None else dict(headers, **kwargs.get('HEADERS'))  # 和传入的请求头合并
        method = 'post' if kwargs.get('请求类型') is '' else kwargs.get('METHOD')
        allow_redirects = True if kwargs.get('allow_redirects') is None else kwargs.get('allow_redirects')  # 是否重定向
        timeout = 500 if kwargs.get('time_out') is None else kwargs.get('time_out')  # 超时时间的设置
        data = dict()
        format_data = kwargs.get('data')
        if isinstance(format_data, str):
            format_data = json.loads(format_data)
        format_data['mch_no'] = ConfigManager.get_service(Constants.Merchant.SW)
        format_data = json.dumps(format_data)
        data['data'] = format_data
        log.info("==============================本次请求data:::%s" % format_data)
        data['sign'] = RequestManager.get_sign(format_data)  # 为请求增加签名认证
        if method.upper().__eq__('GET'):
            res = requests.get(url, params=kwargs.get('params'), headers=headers,
                               allow_redirects=allow_redirects,
                               timeout=timeout, verify=False)  # verify 由于该请求走fiddler会报错 所以关闭verify保证能抓到请求
            return res, res.json()

        if method.upper().__eq__('POST'):
            res = requests.post(url, json=kwargs.get('json'), headers=headers, data=data,
                                params=kwargs.get('params'),
                                allow_redirects=allow_redirects,
                                timeout=timeout, verify=False)
            return res, json.loads(res.json().get('data'))

    @staticmethod
    def get_sign(data):
        """获取请求时需要的sign"""
        token = ConfigManager.get_service(Constants.MD5Token.CS)
        sign = ''.join((data, "&", json.loads(data).get('timestamp'), token))
        sign_md5 = hashlib.md5(sign.encode(encoding='utf-8')).hexdigest()
        return sign_md5

# if method.upper().__eq__('PUT'):
#     for again in range(2):
#         res = requests.put(url, json=kwargs.get('json'), headers=headers, params=kwargs.get('params'),
#                            allow_redirects=allow_redirects,
#                            timeout=timeout, verify=False)
#
#         return res, json.loads(res.text)
# if method.upper().__eq__('DELETE'):
#     for again in range(2):
#         res = requests.delete(url, params=kwargs.get('params'), headers=headers, data=kwargs.get('data'),
#                               allow_redirects=allow_redirects,
#                               timeout=timeout, verify=False)
#
#         return res, json.loads(res.text)
