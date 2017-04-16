# import asyncio
# import aiohttp
#
# import time
# from multiprocessing import Process
# from ip_pool.database import RedisConnect
# from .ip_request import FreeProxyGetter
#
# min_num_ip=30
# max_num_ip =100
# class Test_ip(object):
#     url = 'http://ip.chinaz.com/getip.aspx'
#     def __init__(self):
#         self._conn=RedisConnect()
#         self.raw_proxies=None
#     def put_ip(self,proxy):#传进去的是列表
#         self.raw_proxies=proxy
#     async def test_one_ip(self,proxy):
#         async with aiohttp.ClientSession() as session:
#
#
#             proxies = {'http': 'http://{}'.format(proxy),
#                            'https': 'http://{}'.format(proxy)}
#             async with session.get(self.url,proxy=proxies,timeout=5) as response:
#                 if response.status == 200:
#                     self._conn.put(proxy)
#                     print('有效代理',proxy)
#             # except Exception as e:
#             #     print(e)
#
#     def test(self):
#         '测试代理'
#         print('正在测试代理')
#         try:
#             loop= asyncio.get_event_loop()
#             tasks=[self.test_one_ip(proxy) for proxy in self.raw_proxies]
#             loop.run_until_complete(asyncio.wait(tasks))
#         except Exception as e:
#             print(e)
#
#
# class Ip_catch(object):
#     def __init__(self,max_count=max_num_ip):
#         self.max_count = max_count
#         self._conn =RedisConnect()
#         self.test = Test_ip()
#         self.crawl = FreeProxyGetter()
#
#     def is_enough_ip(self):
#         if self._conn.ip_count >=self.max_count:
#             return False
#         return True
#
#     def add_to_pool(self):
#         print('正在增加代理')
#         try:
#             while self.is_enough_ip():
#                 for num_defination in range(self.crawl.__CrawlFuncCount__):
#                     callback = self.crawl.__CrawlFunc__[num_defination]#启动类里面的抓取函数，这里利用了元类里面的方法
#                     raw_proxies =self.crawl.get_raw_proxies(callback)#
#                     self.test.put_ip(raw_proxies)#将抓到的IP放进去列表以备测试
#                     self.test.test()#测试IP，好的就放进redis
#                     if self.is_enough_ip():
#                         print('IP够了')
#                         break
#         except Exception as e:
#             print(e)
#
#
#
#
# class schedule(object):
#     @staticmethod
#     def action_check_ip():
#         conn =RedisConnect()
#         tester = Test_ip()
#         while True:
#             print('开始检查IP')
#             count = int(0.5 * conn.ip_count)
#             if count ==0:
#                 print('库里没有IP要进行检查')
#                 time.sleep(50)
#                 continue
#             raw_proxy = conn.get_to_test(count)#一次检查一半
#             tester.put_ip(raw_proxy)
#             tester.test()
#             time.sleep(50)
#
#     @staticmethod
#     def action_get_ip():
#         conn=RedisConnect()
#         add_ip = Ip_catch()#默认最多100个IP
#         while True:
#             if conn.ip_count <min_num_ip:
#                 add_ip.add_to_pool()
#             time.sleep(50)
#
#     def run_pool(self):
#         print('开启代理池')
#         action_check_ip=Process(target=schedule.action_check_ip)
#         action_get_ip=Process(target=schedule.action_get_ip)
#         action_check_ip.start()
#         action_get_ip.start()

# from .Thread_pool import ThreadPool#导入线程池
from ip_pool.database import RedisConnect#导入数据库链接
import requests
import re
from ip_pool.ip_request import FreeProxyGetter
from ip_pool.Thread_pool import ThreadPool
import time
from multiprocessing import Process
check_time = 50#多久检查一次IP的有效性
count_time =50#多久严查一次IP数量是否够
lower_num_ip = 30#最少的IP数量
max_num_ip = 70#最多的IP数量

class Test_ip(object):#用于测试IP
    def __init__(self):
        self.url='http://ip.chinaz.com/getip.aspx'#用于测试的url
        self._conn=RedisConnect()
        self._raw_proxies =None
        self.Thread_pool =ThreadPool(10)
    def set_raw_proxies(self,proxies):#接收以备测试的代理
        self._raw_proxies =proxies

    def _test(self,proxy):#测试IP
        if isinstance(proxy,bytes):
            proxy=proxy.decode('utf-8')
        real_proxy= {'http':'http://{}'.format(proxy),
                    'https':'http://{}'.format(proxy),}
        print('正在测试，',proxy)
        try:
            html = requests.get(self.url, proxies=real_proxy, timeout=1)
            status_number = re.findall(r'\d\d\d', str(html))[0]  # 提取网页返回码
            re_ip = re.findall(r'\{ip', html.text)  # 有些 ip极其恶心，虽然返回的是200数字，表示正常，实则是bad request，这里去除掉
            if status_number == str(200):
                if re_ip:
                        # 检验代理是否能正常使用
                    self._conn.put(proxy)
                    print('网页返回状态码:', html, proxy, '代理有效,地址是：', html.text)
        except Exception as e:
            print('移除无效代理，',proxy)
    def Thread_test_ip(self,proxies):#传进去一个列表
        for proxy in proxies:
            self.Thread_pool.run(func=self._test, args=proxy)  # 用多线程测试
        print('本次测试用了多少线程',len(self.Thread_pool.generate_list))

class Get_ip(object):
    def __init__(self,max_ip_count=max_num_ip):#默认IP池里面最多的IP上面设置好了
        self._conn=RedisConnect()
        self.max_ip_count=max_ip_count
        self.crawl=FreeProxyGetter()
        self.Test=Test_ip()
        self.Thread_pool=ThreadPool(10)#用于多线程测试，这里设置最多10个线程
    def is_ip_enough(self):
        if self._conn.ip_count >= self.max_ip_count:#如果池里IP数大于规定最大的数量，则返回False
            return False
        return True

    def catch_ip(self):
        while self.is_ip_enough():
            print('代理数量不足，代理抓取中')
            for callback_lable in range(self.crawl.__CrawlFuncCount__):#该方法在元类里面添加了
                callback = self.crawl.__CrawlFunc__[callback_lable]
                raw_proxies = self.crawl.get_raw_proxies(callback)#这是接收抓取的代理
                if raw_proxies:
                    self.Test.Thread_test_ip(raw_proxies)
                else:
                    print('该源头没有代理')


class schedule(object):
    @staticmethod
    def check_ip(cycle_time=check_time):
        conn = RedisConnect()
        tester = Test_ip()
        while True:
            print('IP检查程序启动')
            count= int(0.5 * conn.ip_count)
            if count == 0:
                time.sleep(cycle_time)
                continue
            raw_proxies = conn.get_to_test(count)
            tester.Thread_test_ip(raw_proxies)#将列表传进去
            time.sleep(cycle_time)
    @staticmethod
    def catch_ip(cycle_time = count_time,max_ip=max_num_ip,min_ip=lower_num_ip):#时间多久检查一次IP数量是否足够
        conn= RedisConnect()
        Ip_catch = Get_ip()
        while True:
            if conn.ip_count <min_ip:#小于最少IP数量，启动抓取
                Ip_catch.catch_ip()
            print('代理暂时充足，不用抓取')
            time.sleep(cycle_time)

    def run(self):
        print('代理池启动')
        check_process =Process(target=schedule.check_ip)
        catch_process = Process(target=schedule.catch_ip)
        check_process.start()
        catch_process.start()





