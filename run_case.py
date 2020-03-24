# 本类主要实现测试执行分类大概思路是设计成传参格式在持续集成运行时能够区分所运行的测试集合
from HTMLTestRunner import HTMLTestRunner
import os, time
import unittest
import sys


class RunCase(object):

    def __init__(self, end_path):
        self.test_path = os.path.join(os.path.abspath('.'), 'project_case', end_path)
        # 传入测试用例路径，改变默认参数为测试用例文件名test.py

    @classmethod
    def run(cls, end_path):
        if hasattr(cls, end_path):
            getattr(cls(end_path), end_path)()

    @staticmethod
    def run_all():
        discover = unittest.defaultTestLoader.discover(os.path.join(os.path.abspath('.'), 'project_case'),
                                                       pattern='*.py')
        RunCase.html_report(discover)

    @staticmethod
    def html_report(discover):
        """生成测试报告"""
        report_path = os.path.join(os.path.abspath('.'), 'report/')
        report_name = time.strftime("%Y-%m-%d") + '_' + end_path
        report_end_path = report_path + report_name + '_result.html'
        with open(report_end_path, 'wb') as fp:
            runner = HTMLTestRunner(stream=fp,
                                    title='银准网络科技有限公司',
                                    description='测试结果如下：')
            runner.run(discover)

    def machaccnt_pay_dispatch(self):
        """支付记账接口discover"""
        discover = unittest.defaultTestLoader.discover(self.test_path, pattern='*.py')
        RunCase.html_report(discover)

    def machaccnt_refund_dispatch(self):
        """退款记账接口discover"""
        discover = unittest.defaultTestLoader.discover(self.test_path, pattern='*.py')
        RunCase.html_report(discover)

    def machaccnt_promotion_dispatch(self):
        """活动记账接口discover"""
        discover = unittest.defaultTestLoader.discover(self.test_path, pattern='*.py')
        RunCase.html_report(discover)


if __name__ == '__main__':
    end_path = '123'
    RunCase.run_all()
