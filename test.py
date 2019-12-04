#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re

from com_zxl_spider_request.BaseRequest import BaseRequest

# 使用 mitmproxy + python 做拦截代理
# https://blog.csdn.net/freeking101/article/details/83901842

if __name__ == "__main__":
    request = BaseRequest()
    driver = request.get_web_content("https://maoyan.com/films?showType=1")
    # driver = request.get_web_content("https://chromedevtools.github.io/devtools-protocol/")
    print("page_source============>", driver.page_source)
