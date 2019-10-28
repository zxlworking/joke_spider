#!/usb/bin/python
# coding=utf-8
import sched
import time

from com_zxl_spider_request.RequestMaoYan import RequestMaoYan
from com_zxl_spider_request.RequestMaoYanDetail import RequestMaoYanDetail

s = sched.scheduler(time.time, time.sleep)


def start():
    s.enter(6 * 3600, 1, start_request_now_mao_yan_task, ())
    s.run()


def start_request_now_mao_yan_task():
    requestMaoYan = RequestMaoYan()
    requestMaoYan.start_now_mao_yan()

    requestMaoYanDetail = RequestMaoYanDetail()
    requestMaoYanDetail.request_now_mao_yan_detail()

    start()


if __name__ == '__main__':
    start()
    # start_request_now_mao_yan_task()
