from data_structure.sql_save import SqlSave


class PreconditionReconciliation(object):

    @staticmethod
    def precondition_reconciliation_result():
        """
        拿到预期结果的 手续费合计，对账单扣除手续费合计
        (手续费合计，对账单扣除手续费合计，是否对平)
        """
        a = SqlSave.select_reconciliation_result()
        return a

    @staticmethod
    def precondition_reconciliation_result_info():
        """
        拿到问题件产生的类型 [问题件]
        :return:
        """
        result = []
        a = SqlSave.select_reconciliation_result_info()
        for i in a:
            result.append(i[0])
        return result

    @staticmethod
    def info_assert_kwargs_actual():
        """实际结果的构造"""
        result = PreconditionReconciliation.precondition_reconciliation_result()
        result_info = PreconditionReconciliation.precondition_reconciliation_result_info()
        kwargs = {'trans_fee': result[0], 'recon_amt': result[1], 'account_type': result[2],
                  'info_len': len(result_info),
                  'info_list': result_info}
        return kwargs


if __name__ == '__main__':
    print(PreconditionReconciliation.precondition_reconciliation_result_info())
