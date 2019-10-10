#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ['maoyan.com', 'm.maoyan.com']
    start_urls = ['http://m.maoyan.com/']

    def parse(self, response):
        print("parse")
        print("response.url::", response.url)

        page = response.url.split("/")[-2]
        filename = 'maoyan-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('保存文件: %s' % filename)