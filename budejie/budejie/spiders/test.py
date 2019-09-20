# -*- coding: utf-8 -*-
import hashlib

import scrapy

from budejie.com_zxl_spider_data.JokeBean import JokeBean
from budejie.com_zxl_spider_db.HotPicJokeDB import HotPicJokeDB


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['www.budejie.com']
    start_urls = ['http://www.budejie.com/']
    jokeDB = HotPicJokeDB()

    # def start_requests(self):  # 由此方法通过下面链接爬取页面
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse)  # 爬取到的页面如何处理？提交给parse方法处理

    def parse(self, response):
        print("parse")
        print("response.url::", response.url)

        # page = response.url.split("/")[-2]
        # filename = 'budejie-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('保存文件: %s' % filename)

        j_r_list_path = '//div[@class="j-r-list"]'
        j_r_list_obj = response.xpath(j_r_list_path)
        print('j_r_list_obj===>', j_r_list_obj)

        j_r_list_user_list_path = './/div[@class="j-list-user"]'
        j_r_list_user_list_obj = response.xpath(j_r_list_user_list_path)

        j_r_list_content_list_path = './/div[@class="j-r-list-c"]'
        j_r_list_content_list_obj = response.xpath(j_r_list_content_list_path)

        j_r_list_tool_list_path = './/div[@class="j-r-list-tool"]'
        j_r_list_tool_list_obj = response.xpath(j_r_list_tool_list_path)

        for i in range(len(j_r_list_user_list_obj)):
            user_item = j_r_list_user_list_obj[i]
            # print('test_item===>', user_item.get())
            user_img_path = './/img[@class="u-logo lazy"]/@data-original'
            user_img_obj = user_item.xpath(user_img_path)
            print('user_img_obj===>', user_img_obj.get())
            user_name_path = './/a[@class="u-user-name"]/text()'
            user_name_obj = user_item.xpath(user_name_path)
            print('user_name_obj===>', user_name_obj.get())

            content_item = j_r_list_content_list_obj[i]
            content_desc_path = './/div[@class="j-r-list-c-desc"]/a/text()'
            content_desc_obj = content_item.xpath(content_desc_path)
            print('content_desc_obj===>', content_desc_obj.get())

            content_detail_path = './/div[@class="j-r-list-c-desc"]/a/@href'
            content_detail_obj = content_item.xpath(content_detail_path)
            detail_url = 'http://www.budejie.com/' + content_detail_obj.get()
            print('content_detail_obj===>', detail_url)

            md5_object = hashlib.md5()
            md5_object.update(detail_url.encode('utf-8'))
            joke_md5_value = md5_object.hexdigest()
            print('joke_md5_value===>', joke_md5_value)

            content_img_path = './/img[@class="lazy"]/@data-original'
            content_img_obj = content_item.xpath(content_img_path)
            print('content_img_obj===>', content_img_obj.get())

            comment_item = j_r_list_tool_list_obj[i]
            vote_path = './/li[@class="j-r-list-tool-l-up"]/span/text()'
            vote_obj = comment_item.xpath(vote_path)
            print('vote_obj===>', vote_obj.get())

            comment_content_path = './/span[@class="comment-counts"]/text()'
            comment_content_obj = comment_item.xpath(comment_content_path)
            print('comment_content_obj===>', comment_content_obj.get())

            joke_bean = JokeBean()
            joke_bean = joke_bean.create_joke_bean(
                "",
                user_name_obj.get().encode('utf-8'),
                '0',
                '0',
                user_img_obj.get(),
                content_desc_obj.get().encode('utf-8'),
                content_img_obj.get(),
                '好笑' + vote_obj.get(),
                '评论' + comment_content_obj.get(),
                detail_url,
                joke_md5_value)

            is_exist_joke_item = self.jokeDB.query_by_md5(joke_md5_value)
            print(is_exist_joke_item)
            if is_exist_joke_item is None:
                print("not ExistJokeItem")
                self.jokeDB.insert_joke(joke_bean)

            else:
                print("ExistJokeItem")
                self.jokeDB.delete_joke_detail_id(is_exist_joke_item['id'])
                self.jokeDB.insert_joke(joke_bean)
                continue

        next_page_path = './/a[@class="pagenxt"]/@href'
        next_page_obj = response.xpath(next_page_path)
        print("next_page_obj::", next_page_obj)
        if next_page_obj is not None:
            next_page = next_page_obj.get()
            print("next_page::", next_page)
            next_page_url = 'http://www.budejie.com/' + next_page
            print("next_page_url::", next_page_url)
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)
