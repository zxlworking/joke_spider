#!/usr/bin/python
# coding=utf-8
from selenium import webdriver


class BaseRequest:

    # def __init__(self):
    #     print "BaseRequest init"

    def get_web_content(self, url):
        #chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        chromedriver = "/Users/zxl/Downloads/chromedriver"

        # 创建chrome参数对象
        opt = webdriver.ChromeOptions()

        # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
        opt.set_headless()
        prefs = {"profile.managed_default_content_settings.images": 2}
        opt.add_experimental_option("prefs", prefs)

        # 创建chrome无界面对象
        driver = webdriver.Chrome(executable_path=chromedriver, options=opt)

        driver.get(url)

        return driver
