from common.ftp_connect import FtpConnect


class DownloadStatement(object):
    """下载对账单"""

    @staticmethod
    def info_assert_kwargs(ftp_name, ftp_number, db_number, db_type='', file_size=''):
        """
        1.验证ftp对账单数量 ftp_number
        2.验证数据库生成明细数量 db_number
        3.验证数据库生成对账单的渠道 db_type
        4.验证ftp对账单的大小 file_size
        :return:
        """
        kwarg = {'ftp_name': ftp_name, 'ftp_number': ftp_number, 'db_number': db_number, 'db_type': db_type,
                 'file_size': file_size}
        return kwarg
