# -*- coding: utf-8 -*-

import redis
import time
import log_util


class Redis():
    host_default = 'localhost'
    port_default = 6379
    db_finish = 0         #redis 第一个db存放已解析的url
    db_redis = {}

    log_filename = 'redis_log'
    log_filepath = './'
    l = log_util.Log(log_filename,log_filepath)


    def __init__(self, db_number):
        self.db_finish = db_number
        pool_finish = redis.ConnectionPool(host=self.host_default,
                                    port=self.port_default,
                                    db=self.db_finish)
        r_finish = redis.Redis(connection_pool=pool_finish)
        self.db_redis = {'r_finish': r_finish}

    def __store_item__(self, item):
        try:
            if not self.__isexist__(item):
                return False
            else:
                store_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                value = {'id': item, 'store_time': store_time}
                self.db_redis['r_finish'].setnx(item, value)     #不会重复的存入数据库
                self.db_redis['r_finish'].expire(item, 2592000)  #设定url过期时间  一个月
                return True
        except Exception as e:
            self.l.print_log(e)

    def __isexist__(self, item):
        try:
            if self.db_redis['r_finish'].exists(item):
                return True
            else:
                return False
        except Exception as e:
            self.l.print_log(e)