import paramiko
from common.config_manager import ConfigManager


class ExcSsh(object):
    def __init__(self):
        obj = ConfigManager.get_ini_obj()
        self.username = obj.get('param_iko', 'username').strip()
        self.password = obj.get('param_iko', 'password').strip()
        self.server_host = obj.get('param_iko', 'server_host').strip()
        self.port = obj.get('param_iko', 'port').strip()
        self.ssh = self.connect()

    def connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.server_host,
                       port=self.port,
                       username=self.username,
                       password=self.password
                       )
        return client

    def sftp_down_file(self, server_path, local_path):
        """下载配置文件到本地resouce目录下"""
        sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        sftp.get(server_path, local_path)
        self.ssh.close()

    def do_store(self):
        """执行进件脚本"""
        a = self.ssh.exec_command('php /home/marcus/lnmp/nginx/html/storeadd/cronjob.php merstorenoti')
        print(a[1].read().decode())

    def do_find_store(self):
        """执行进件查询脚本"""
        a = self.ssh.exec_command('php /home/marcus/lnmp/nginx/html/storeadd/cronjob.php merstorestatusfetchnoti')
        print(a[1].read().decode())


if __name__ == '__main__':
    ExcSsh().do_store()
