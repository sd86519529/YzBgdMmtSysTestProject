class HandleDowStatement(object):
    @staticmethod
    def assert_dow_statement(self, **kwargs):
        """
        验证对账单拉去是否正确
        1.验证ftp对账单数量 ftp_number
        2.验证数据库生成明细数量 db_number
        3.验证数据库生成对账单的渠道 db_type
        4.验证ftp对账单的大小 file_size
        5.验证ftp的文件名是否存记录在db中
        """
        befor_data = kwargs['befor_data']
        after_data = kwargs['after_data']
        name_bool = True
        for name in befor_data['ftp_name']:
            if name in after_data['ftp_name']:
                continue
            else:
                name_bool = False
        self.assertEqual(name_bool, True, msg='对账单名称列表不匹配，请检查')
        self.assertEqual(befor_data['ftp_number'], after_data['ftp_number'],
                         msg='上传ftp的对账单数量应为%s,实际只有%s' % (befor_data['ftp_number'], after_data['ftp_number']))
        self.assertEqual(befor_data['db_number'], after_data['db_number'],
                         msg='数据库的对账单明细应为%s,实际只有%s' % (befor_data['db_number'], after_data['db_number']))
        for size in after_data['file_size']:
            self.assertGreater(size, 5000, msg='FTP上对账单的大小异常，小于5kb，请确认')
        self.assertListEqual(after_data['db_type'], befor_data['db_type'], msg='对账单类型不符合预期结果，请检查')

    @staticmethod
    def assert_mch_account_details():
        """
        1.比对解析后明细数量
        2.比对download_info表中明细是否解析开关
        """


