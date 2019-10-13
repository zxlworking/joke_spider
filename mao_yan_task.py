#!/usb/bin/python
# coding=utf-8
import sched
import time

from com_zxl_spider_request.RequestMaoYan import RequestNowMaoYan

s = sched.scheduler(time.time, time.sleep)


def start():
    s.enter(24 * 3600, 1, start_request_now_mao_yan_task, ())
    # s.enter(60, 1, start_request_now_mao_yan_task, ())
    s.run()


def start_request_now_mao_yan_task():
    requestNowMaoYan = RequestNowMaoYan()
    requestNowMaoYan.start()
    start()


if __name__ == '__main__':
    start()
