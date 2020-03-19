import pymysql
from common import logger
from common.config_manager import ConfigManager

log = logger.Logger('ConnectionMysql').get_log()


class ConnectionMysql(object):
    def __init__(self):
        config = ConfigManager.get_ini_obj()
        self.db = pymysql.connect(config.get('Mysql', 'server_host'), config.get('Mysql', 'username'),
                                  config.get('Mysql', 'password'), config.get('Mysql', 'database'),
                                  int(config.get('Mysql', 'port')), charset='utf8')
        self.cursor = self.db.cursor()

    def execute_db(self, sql):
        # 插入
        try:
            log.info('正在执行的sql语句为%s' % sql)
            # 执行sql
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            # 发生错误时回滚
            log.error('文件：%s,\r\n行数： %s,\r\n错误内容： %s' % (
                e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, e))
            self.db.rollback()
        finally:
            self.cursor.close()

    def select_db(self, sql):
        """查询"""
        log.info('正在执行的查询语句为%s' % sql)
        try:
            self.cursor.execute(sql)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            return self.cursor.fetchall()  # 返回所有记录列表
        except Exception as e:
            log.error('文件：%s,\r\n行数： %s,\r\n错误内容： %s' % (
                e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, e))
        finally:
            self.cursor.close()

    def close_db(self):
        """数据库连接关闭"""
        self.db.close()


if __name__ == '__main__':
    # 测试
    pass
