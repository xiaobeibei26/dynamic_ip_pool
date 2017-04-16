import redis


class RedisConnect(object):
    def __init__(self):
        self.db=redis.Redis(host='localhost',port=6379)

    def get_to_test(self,count=1):#获取代理以备检查
        proxy = self.db.lrange('proxies',0,count-1)
        self.db.ltrim('proxies',count,-1)
        return proxy


    def put(self,proxy):
        self.db.rpush('proxies',proxy)


    def pop(self):
        try:
            return self.db.rpop('proxies')
        except Exception as e:
            return  '没有代理可用'
    @property
    def ip_count(self):
        return self.db.llen("proxies")



