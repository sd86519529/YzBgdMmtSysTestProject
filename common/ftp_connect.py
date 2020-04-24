import ftplib
from common.config_manager import ConfigManager


class FtpConnect(object):
    def __init__(self):
        obj = ConfigManager.get_ini_obj()
        self.username = obj.get('ftp_config', 'username')
        self.password = obj.get('ftp_config', 'password')
        self.host = obj.get('ftp_config', 'server_host')
        self.f = self.__connect_ftp()

    def __connect_ftp(self):
        f = ftplib.FTP(host=self.host)
        f.login(self.username, self.password)
        f.cwd('deposit_test')
        print(f.nlst())
        return f

    def get_dir_list(self):
        return self.f.nlst()


if __name__ == '__main__':
    lis = FtpConnect().get_dir_list()

    print(lis)
    print('----------------------')
    print(len(lis))
