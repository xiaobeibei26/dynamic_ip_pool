from .html_request import MyRequest
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup

class ProxyMetaclass(type):
    """
        __CrawlFunc__和__CrawlFuncCount__
        两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """
    def __new__(cls, name, bases, attrs):#这几个是固定参数
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:#坚持每个方法里面的key值是否有crawl字符，然后运行，方便以后添加代理的抓取进去
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):

    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):#eval这里用于执行字符串
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            try:
                html = MyRequest.get(url,3)
                if html:
                    doc = pq(html)
                    trs = doc('.containerbox table tr:gt(0)').items()
                    for tr in trs:
                        ip = tr.find('td:nth-child(1)').text()
                        port = tr.find('td:nth-child(2)').text()
                        yield ':'.join([ip, port])
            except Exception as e:
                print('Crawling faild', url)

    def crawl_proxy360(self):
        start_url = 'http://www.proxy360.cn/Region/China'
        print('Crawling', start_url)
        try:
            html = MyRequest.get(start_url,3)
            if html:
                doc = pq(html)
                lines = doc('div[name="list_proxy_ip"]').items()
                for line in lines:
                    ip = line.find('.tbBottomLine:nth-child(1)').text()
                    port = line.find('.tbBottomLine:nth-child(2)').text()
                    yield ':'.join([ip, port])
        except:
            print('Crawling faild', start_url)

    def crawl_goubanjia(self):
        start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
        try:
            html = MyRequest.get(start_url,3)
            if html:
                doc = pq(html)
                tds = doc('td.ip').items()
                for td in tds:
                    td.find('p').remove()
                    yield td.text().replace(' ', '')
        except:
            print('Crawling faild', start_url)

    def crawl_haoip(self):
        start_url = 'http://haoip.cc/tiqu.htm'
        try:
            html =MyRequest.get(start_url,3)
            if html:
                doc = pq(html)
                results = doc('.row .col-xs-12').html().split('<br/>')
                for result in results:
                    if result: yield result.strip()
        except:
            print('Crawling faild', start_url)


    def crawl_xici(self):#西刺网的爬取
        start_url ='http://www.xicidaili.com/nn/1'
        try:
            data = MyRequest.get(start_url, 3)
            all_data = BeautifulSoup(data, 'lxml')
            all_ip = all_data.find_all('tr', class_='odd')
            for i in all_ip:
                ip = i.find_all('td')[1].get_text()  # ip
                port = i.find_all('td')[2].get_text()  # 端口
                proxy = (ip + ':' + port).strip()  # 组成成proxy代理
                if proxy:
                    yield proxy
        except:
            print('Crawling faild', start_url)