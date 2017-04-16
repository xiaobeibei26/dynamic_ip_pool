# import requests
#
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

# class MyRequest(object):
#     def get(self,url,timeout=3,headers=headers,):
#         return requests.get(url,timeout=timeout,headers=headers).text
'''这是一个封装无限循环进行访问网页的请求，用来请求代理网页'''
import requests
import re
import random
import time


class download():
    def __init__(self):

        self.iplist = []  ##初始化一个list用来存放我们获取到的IP
        html = requests.get("http://haoip.cc/tiqu.htm")  ##不解释咯
        iplistn = re.findall(r'r/>(.*?)<b', html.text,
                             re.S)  ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
        for ip in iplistn:
            i = re.sub('\n', '', ip)  ##re.sub 是re模块替换的方法，这儿表示将\n替换为空
            self.iplist.append(i.strip())  ##添加到我们上面初始化的list里面

        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    def get(self, url, timeout, proxy=None, num_retries=6):  ##给函数一个默认参数proxy为空
        UA = random.choice(self.user_agent_list)  ##从self.user_agent_list中随机取出一个字符串
        headers = {'User-Agent': UA}  ##构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串哦）

        if proxy == None:  ##当代理为空时，不使用代理获取response
            try:
                return requests.get(url, headers=headers, timeout=timeout).text
            except:  ##如过上面的代码执行报错则执行下面的代码

                if num_retries > 0:  ##num_retries是我们限定的重试次数
                    time.sleep(8)
                    print(u'获取网页出错，10S后将获取倒数第：', num_retries, u'次')
                    return self.get(url, timeout, num_retries - 1)  ##调用自身 并将次数减1
                else:
                    print(u'开始使用代理')
                    time.sleep(8)
                    IP = ''.join(str(random.choice(self.iplist)).strip())  ##下面有解释哦
                    proxy = {'http': IP}
                    return self.get(url, timeout, proxy, )  ##代理不为空的时候

        else:  ##当代理不为空
            try:
                IP = ''.join(
                    str(random.choice(self.iplist)).strip())  ##将从self.iplist中获取的字符串处理成我们需要的格式（处理了些什么自己看哦，这是基础呢）
                proxy = {'http': IP}  ##构造成一个代理
                return requests.get(url, headers=headers, proxies=proxy, timeout=timeout).text  ##使用代理获取response
            except:

                if num_retries > 0:
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http': IP}
                    print(u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次')
                    print(u'当前代理是：', proxy)
                    return self.get(url, timeout, proxy, num_retries - 1)
                else:
                    print(u'代理也不好使了！取消代理')
                    return self.get(url, 3)


MyRequest = download()