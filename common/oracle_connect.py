import cx_Oracle

# 连接数据库，下面括号里内容根据自己实际情况填写
db_conn = cx_Oracle.connect('jinwei', 'jinwei', '%s:%s/%s' % ('172.16.13.139', '1521', 'DG2'))
print(db_conn)
