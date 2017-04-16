# from flask import Flask, g
from .database import RedisConnect
import tornado.ioloop
import tornado.web

conn=RedisConnect()
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
class GetIpHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write(conn.pop())
class Count_ipHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write(str(conn.ip_count))#不加str，在浏览器就显示不出来

application = tornado.web.Application([
    (r"/index", MainHandler),(r'/get',GetIpHandler),(r'/count',Count_ipHandler)
])



def tornado_run(port=8888):#默认是8888端口
    application.listen(port)  # 监听端口
    print('tornado服务器已经启动,正在监听{}端口'.format(port))
    tornado.ioloop.IOLoop.instance().start()

#
# __all__ = ['app']
# app = Flask(__name__)


# def get_conn():
#     """
#     Opens a new redis connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'redis_client'):
#         g.redis_client = RedisConnect()
#     return g.redis_client
#
#
# @app.route('/')
# def index():
#     return '<h2>Welcome to Proxy Pool System</h2>'
#
#
# @app.route('/get')
# def get_proxy():
#     """
#     Get a proxy
#     """
#     conn = get_conn()
#     return conn.pop()
#
#
# @app.route('/count')
# def get_counts():
#     """
#     Get the count of proxies
#     """
#     conn = get_conn()
#     return str(conn.ip_count)
#
#
# if __name__ == '__main__':
#     app.run()
