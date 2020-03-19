import logging
import os
import time

"""
此类是日志打印类，封装日志打印工具提供其他类的调用，obj为其他类名称
创建日期格式文件夹公共方法，以及扩展方法
"""


class Logger(object):
    """
    日志信息类创建后class logger(object),在初始化方法中完成保存日志的路径，日志的级别，调用的文件将
    日志储存到指定文件中。
    :param object:
    :return logger:
    """

    def __init__(self, obj, log_name='YZ_'):
        # 使用logging.getLogger传入其他类名称来创建一个logger
        self.log = logging.Logger(obj)
        # 设置日志的等级
        self.log.setLevel(logging.DEBUG)
        # 创建好log对象后编辑log的储存位置，文件名以时间方式避免重复
        str_list = [log_name, time.strftime('%Y%m%d'), '.logs']
        file_name = ''.join(str_list)
        log_path = os.path.join(Logger.mkdir_path('\logs\\'), file_name)
        # 创建一个handler,用于输出到指定文件，并且设置日志的等级
        file = logging.FileHandler(log_path, encoding='utf-8')
        file.setLevel(logging.INFO)
        # 创建另一个handler,用于输出至控制台，并设置日志等级
        stream = logging.StreamHandler()
        stream.setLevel(logging.INFO)
        # 定义handler的输出格式，file和stream分别添加
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file.setFormatter(formatter)
        stream.setFormatter(formatter)
        # 给日志添加对应的handler
        self.log.addHandler(file)
        self.log.addHandler(stream)

    @staticmethod
    def generation_path(path, replenish_path=None):
        """生成需要循环创建文件夹的路径,replenish_path,补充的路径，如果需要在日期后在加文件夹可以传入"""
        # 系统当前时间年份
        file_list = []
        year = time.strftime('%Y', time.localtime(time.time()))
        # 月份
        month = time.strftime('%m', time.localtime(time.time()))
        # 日期
        day = time.strftime('%d', time.localtime(time.time()))

        str_path = [os.path.dirname(os.path.dirname(__file__)), path]
        file_path = ''.join(str_path)
        file_year = file_path + year
        file_month = os.path.join(file_year, month)
        file_day = os.path.join(file_month, day)
        file_list.append(file_year)
        file_list.append(file_month)
        file_list.append(file_day)
        if replenish_path is None:
            return file_list
        file_list.append(os.path.join(file_day, replenish_path))
        return file_list

    @staticmethod
    def mkdir_path(path, replenish_path=None):
        """通过路径创建文件夹"""
        file_list = Logger.generation_path(path, replenish_path)
        result_file_list = file_list[-1]
        for file in file_list:
            if not os.path.exists(file):
                os.mkdir(file)
            else:
                continue
        return result_file_list

    def get_log(self):
        """
        实例化类后调用此方法返回log对象
        :return:
        """
        return self.log


if __name__ == '__main__':
    pass
