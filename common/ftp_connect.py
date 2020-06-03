import ftplib
import os
from common.config_manager import ConfigManager


class FtpConnect(object):
    def __init__(self):
        obj = ConfigManager.get_ini_obj()
        self.username = obj.get('ftp_config', 'username')
        self.password = obj.get('ftp_config', 'password')
        self.host = obj.get('ftp_config', 'server_host')
        print(self.username,self.password,self.host)
        self.f = self.__connect_ftp()

    def __connect_ftp(self):
        f = ftplib.FTP(host=self.host)
        f.login(self.username, self.password)
        # /var/ftp/test
        f.cwd('deposit_test')
        return f

    def get_dir_list(self):
        """返回ftp的文件列表和文件数量"""
        return self.f.nlst(), len(self.f.nlst())

    def delete_file(self, file_name):
        return self.f.delete(file_name)

    def get_file_size(self, file_name):
        """获取文件大小 25kb返回为25000"""
        return self.f.size(file_name)

    def push_file_csv_on_ftp(self,path):
        """上传csv文件到对ftp"""
        bufsize = 1024
        fp = open(path, 'rb')
        self.f.storbinary('STOR ' + os.path.basename(path), fp, bufsize)
        self.f.set_debuglevel(0)
        self.f.close()
        return os.path.basename(path)


if __name__ == '__main__':
    # a = FtpConnect().push_file_csv_on_ftp()
    # print(a)
    FtpConnect()
