import os
import yaml
import configparser


class ConfigManager(object):
    """
    配置文件读取类
    """

    @staticmethod
    def get_ini_obj():
        """获取ini配置文件返回对象"""
        ini_path = '/config/config.ini'
        config_path = ''.join([os.path.dirname(os.path.dirname(__file__)), ini_path])
        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')
        return config

    @staticmethod
    def get_basic(key):
        """获取基础文件的配置项"""
        return ConfigManager.__get(key, 'basic_configuration')

    @staticmethod
    def get_service(key):
        """获取项目(服务)文件的配置项"""
        return ConfigManager.__get(key, 'service_configuration')

    @staticmethod
    def get_ex_name(ex_name):
        """获取用例excle的路径配置"""
        return ConfigManager.get_service('EXCLE.' + ex_name)

    @classmethod
    def __get(cls, key, config_name):
        keys = key.split('.')
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', config_name),
                  encoding='UTF-8') as config:
            value = yaml.load(config,Loader=yaml.FullLoader).get(keys[0])
            if len(keys) > 1:
                for index in range(1, len(keys)):
                    value = value[keys[index]]
            return value


if __name__ == '__main__':
    pass
