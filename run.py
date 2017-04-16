from ip_pool.api import tornado_run
from ip_pool.main import schedule


def main():
    s = schedule()
    s.run()
    tornado_run(5000)#启动tornado,5000是端口，默认是8000

if __name__ == '__main__':
    main()
