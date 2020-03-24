from common.request_manager import RequestManager


class RequestBase(object):
    """测试用例继承类，用于需要使用请求时继承的类"""

    def __init__(self):
        pass

    @staticmethod
    def send_request(**kwargs):
        """
        :param args:
        :param kwargs:
            接口名称         name
            请求方式         method
            参数             data
            用户             user
            是否重定向       allow_redirects
            可选参数超时时间  time_out
        :return:
        """

        res, html = RequestManager.send_requests(**kwargs)
        print('本次请求返回:::>>' + str(html))
        return res, html
