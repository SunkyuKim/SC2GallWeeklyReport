import crawl
import datetime

if __name__ == '__main__':
    dtime = datetime.datetime.strptime("%s-%s-%s 14:00:00"%(2017,8,31),
                                           '%Y-%m-%d %H:%M:%S')
    posts = crawl.crawl(init=0)
