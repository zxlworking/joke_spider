#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# def request(flow):
#     print("request host = ", flow.request.pretty_host)
#    if flow.request.pretty_host == 'www.baidu.com':
#        flow.request.host = '192.168.29.128'
#        flow.request.port = 8080
from mitmproxy import ctx


def request(flow):
    print("request url = ", flow.request.url)
    # if 'bs/yoda-static/file' in flow.request.url:
    #     print('*' * 100)
    #     print(flow.request.url)
    #     flow.response.text = flow.response.text.replace("webdriver", "fuck_that")
    #     flow.response.text = flow.response.text.replace("Webdriver", "fuck_that")
    #     flow.response.text = flow.response.text.replace("WEBDRIVER", "fuck_that")
    # chang_ip()
    pass


def response(flow):
    # print("response = ", flow.response.text)
    # if 'webdriver' in flow.response.text:
    #     print('*' * 100)
    #     print('find web_driver key')
    #     flow.response.text = flow.response.text.replace("webdriver", "fuck_that_1")
    # if 'Webdriver' in flow.response.text:
    #     print('*' * 100)
    #     print('find web_driver key')
    #     flow.response.text = flow.response.text.replace("Webdriver", "fuck_that_2")
    # if 'WEBDRIVER' in flow.response.text:
    #     print('*' * 100)
    #     print('find web_driver key')
    #     flow.response.text = flow.response.text.replace("WEBDRIVER", "fuck_that_3")

    # webdriver_key = ['webdriver',
    #                  '__driver_evaluate',
    #                  '__webdriver_evaluate',
    #                  '__selenium_evaluate',
    #                  '__fxdriver_evaluate',
    #                  '__driver_unwrapped',
    #                  '__webdriver_unwrapped',
    #                  '__selenium_unwrapped',
    #                  '__fxdriver_unwrapped',
    #                  '_Selenium_IDE_Recorder',
    #                  '_selenium',
    #                  'calledSelenium',
    #                  '_WEBDRIVER_ELEM_CACHE',
    #                  'ChromeDriverw',
    #                  'driver-evaluate',
    #                  'webdriver-evaluate',
    #                  'selenium-evaluate',
    #                  'webdriverCommand',
    #                  'webdriver-evaluate-response',
    #                  '__webdriverFunc',
    #                  '__webdriver_script_fn',
    #                  '__$webdriverAsyncExecutor',
    #                  '__lastWatirAlert',
    #                  '__lastWatirConfirm',
    #                  '__lastWatirPrompt',
    #                  '$chrome_asyncScriptInfo',
    #                  '$cdc_asdjflasutopfhvcZLmcfl']

    if 'js' in flow.request.url:
        print("flow.request.url = ", flow.request.url)
        print("response = ", flow.response.text)

    """修改应答数据"""
    # 屏蔽selenium检测
    for webdriver_key in ['webdriver', '__driver_evaluate', '__webdriver_evaluate', '__selenium_evaluate',
                          '__fxdriver_evaluate', '__driver_unwrapped', '__webdriver_unwrapped',
                          '__selenium_unwrapped', '__fxdriver_unwrapped', '_Selenium_IDE_Recorder', '_selenium',
                          'calledSelenium', '_WEBDRIVER_ELEM_CACHE', 'ChromeDriverw', 'driver-evaluate',
                          'webdriver-evaluate', 'selenium-evaluate', 'webdriverCommand',
                          'webdriver-evaluate-response', '__webdriverFunc', '__webdriver_script_fn',
                          '__$webdriverAsyncExecutor', '__lastWatirAlert', '__lastWatirConfirm',
                          '__lastWatirPrompt', '$chrome_asyncScriptInfo', '$cdc_asdjflasutopfhvcZLmcfl_']:
        # ctx.log.info('Remove"{}"from{}.'.format(webdriver_key, flow.request.url))
        # flow.response.text = flow.response.text.replace('"{}"'.format(webdriver_key), '"NO-SUCH-ATTR"')
        # flow.response.text = flow.response.text.replace('t.webdriver', 'false')
        # flow.response.text = flow.response.text.replace('ChromeDriver', '')
        if webdriver_key in flow.response.text:
            print(webdriver_key, "==========in==============", flow.request.url)
