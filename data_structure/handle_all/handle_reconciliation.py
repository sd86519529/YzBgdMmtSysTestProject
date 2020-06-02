class HandleReconciliation(object):
    """对账校验文件"""

    @staticmethod
    def handle_assert(self, expect, actual):
        # 对比手续费总额
        self.assertEqual(expect['trans_fee'], actual['trans_fee'],
                         msg='手续费总额不匹配，预期为%s,实际为%s' % (expect['trans_fee'], actual['trans_fee']))
        # 对比对账单扣除手续费总额
        self.assertEqual(expect['recon_amt'], actual['recon_amt'],
                         msg='对账单扣除手续费总额不匹配，预期为%s,实际为%s' % (expect['recon_amt'], actual['recon_amt']))
        # 是否对平校验
        self.assertEqual(expect['account_type'], actual['account_type'],
                         msg='是否对平不匹配，预期为%s,实际为%s' % (expect['account_type'], actual['account_type']))
        # 问题件数量不匹配
        self.assertEqual(expect['info_len'], actual['info_len'],
                         msg='问题件数量不匹配，预期为%s,实际为%s' % (expect['info_len'], actual['info_len']))
        # 问题件类型不匹配
        self.assertListEqual(expect['info_list'], actual['info_list'],
                             msg='问题件类型不匹配，预期为%s,实际为%s' % (expect['info_list'], actual['info_list']))
