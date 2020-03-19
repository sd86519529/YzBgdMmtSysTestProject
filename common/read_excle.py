import xlrd
import os
from common import logger
from common.config_manager import ConfigManager

log = logger.Logger('ReadExl').get_log()


class ReadExl(object):
    """
    读取excle中的数据，默认从第二行开始读取，以字典格式输入，提供接口使用
    """

    def __init__(self, ex_name, sheet=0):
        """
        初始化excle,传入服务名称查询到excle_name和case_data
        """
        # 获取在配置文件中管理的文件名称，然后拿到文件的存储路径
        case_dir, case_data = ConfigManager.get_ex_name(ex_name).split(',')
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'project_data', case_dir, case_data)
        log.info('准备读取的测试数据为%s' % path)
        self.data = xlrd.open_workbook(path, encoding_override='utf-8')
        # 默认选取第一张sheet
        self.table = self.data.sheet_by_index(sheet)
        # 获取第一行的值作为key
        self.keys = self.table.row_values(0)
        # 获取总行数
        self.rowNumber = self.table.nrows
        # 获取总列数
        self.colNumber = self.table.ncols

    def obtain_data(self):
        """
        获取excle表数据的方法
        :return: 从第二行开始以字典格式输出
        """
        if self.rowNumber < 1:
            log.info('%s数据表中的数据少于一行，请重新定义数据')
        else:
            try:
                s = []
                j = 1  # 定义行数为1
                for i in range(self.rowNumber - 1):  # 循环从0开始到行数减1次
                    new_dict = {}
                    log.info('开始读取第%s行数据' % j)
                    value = self.table.row_values(j)  # 拿到第二行的数据
                    for k in range(self.colNumber):  # 循环列的总数
                        number = value[k]  # 取出从第二行开始的所有列的数据添加到字典new_dict中
                        # 字典的键为读取的第一行的数据作为key
                        new_dict[self.keys[k]] = number
                    s.append(new_dict)  # 将一行的数据读取完成后添加至列表中,行数加1重新循环
                    j += 1
                return s
            except Exception as e:
                log.error('读取测试数据发生异常：文件：%s,\r\n行数： %s,\r\n错误内容： %s' % (
                    e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, e))

    @staticmethod
    def screen_case(case_name, data):
        """
        根据用例编号筛选用例数据
        1.case_name: 当前流程case编号：对应脚本本身文件名称
        2.data：
        """
        return_list = list()
        for d in data:
            if d['测试用例名称'].__eq__(case_name):
                if d['备注'].__eq__('skip'):
                    continue
                return_list.append(d)
            continue
        return return_list


if __name__ == '__main__':
    # ReadExl.screen_case(os.path.split(__file__)[-1].split(".")[0],
    #                     ReadExl(Constants.EXL.PAY, sheet=0).obtain_data())
    print(os.path.split(__file__)[-1].split(".")[0])
