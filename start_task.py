#!/usb/bin/python
# coding=utf-8
import sched
import time

from com_zxl_spider_request.RequestQsbkHomeHotPic import RequestQsbkHomeHotPic

s = sched.scheduler(time.time, time.sleep)


def start():
    s.enter(3600, 1, start_qsbk_hot_pic_spider, ())
    s.run()


def start_qsbk_hot_pic_spider():
    request = RequestQsbkHomeHotPic()
    request.start_task()
    start()


if __name__ == '__main__':
    # start()
    request = RequestQsbkHomeHotPic()
    request.start_task()
