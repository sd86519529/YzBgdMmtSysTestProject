import redis
from common.config_manager import ConfigManager


def remove_withdrawal_info(mch_no, order_no):
    """提现接口调用时会写入缓存，自动化脚本跑时会重复提交redis所以需要删除redis的缓存数据"""
    obj = ConfigManager.get_ini_obj()
    r = redis.Redis(connection_pool=redis.ConnectionPool(host=obj.get('redis_config', 'server_host'),
                                                         password=obj.get('redis_config', 'password'),
                                                         db=obj.get('redis_config', 'db')))
    keys = 'com.deposit.withdraw:' + mch_no + order_no
    v = r.get(keys)
    print('正在清理缓存%s' % v)
    if v is None:
        print('没有缓存')
        return
    r.delete(keys)

def remove_mch_accnt_no_settle_key():
    """提现接口调用时会写入缓存，自动化脚本跑时会重复提交redis所以需要删除redis的缓存数据"""
    obj = ConfigManager.get_ini_obj()
    r = redis.Redis(connection_pool=redis.ConnectionPool(host=obj.get('redis_config', 'server_host'),
                                                         password=obj.get('redis_config', 'password'),
                                                         db='0'))
    keys = 'mch_accnt_no_settle_key'

    r.delete(keys)

if __name__ == '__main__':
    remove_mch_accnt_no_settle_key()