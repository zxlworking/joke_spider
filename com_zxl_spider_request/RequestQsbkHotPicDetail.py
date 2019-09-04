#!/usr/bin/python
# coding=utf-8
import datetime
import re

from selenium.common.exceptions import NoSuchElementException

from com_zxl_spider_data.JokeDetailBean import JokeDetailBean
from com_zxl_spider_db.HotPicJokeDetailDB import HotPicJokeDetailDB
from com_zxl_spider_request.BaseRequest import *


class RequestQsbkHotPicDetail(BaseRequest):

    def __init__(self):
        global jokeDB
        jokeDB = HotPicJokeDetailDB()
        jokeDB.delete_joke_detail()

    def parse(self, hot_pic_id, url):
        print("parse::url = ", url)

        article_id = -1
        find_article_id_result_array = re.findall(".*?(\d+).*?", url)
        if len(find_article_id_result_array) > 0:
            article_id = int(find_article_id_result_array[0])
        print("id = ", article_id)

        driver = self.get_web_content(url)

        # page_source = driver.page_source
        # print(page_source)

        stats_time_path = '//span[@class="stats-time"]'
        stats_time_object = driver.find_element_by_xpath(stats_time_path)
        stats_time = stats_time_object.text

        content_parent_path = '//div[@class="article block untagged noline"]'
        content_parent_object = driver.find_element_by_xpath(content_parent_path)

        content_object = content_parent_object.find_element_by_xpath('.//div[@class="content"]')
        content = content_object.text

        thumb_img_url = ''
        try:
            thumb_object = content_parent_object.find_element_by_xpath('.//div[@class="thumb"]')
            thumb_img_object = thumb_object.find_element_by_xpath('.//img')
            thumb_img_url = thumb_img_object.get_attribute('src')
        except NoSuchElementException as e:
            print(e)

        print(article_id)
        print(stats_time)
        print(content)
        print(thumb_img_url)

        jokeDetailBean = JokeDetailBean()
        jokeDetailBean = jokeDetailBean.create_joke_detail_bean(
            "",
            hot_pic_id,
            article_id,
            stats_time,
            content,
            thumb_img_url
        )
        jokeDB.insert_joke_detail(jokeDetailBean)

        driver.close()

    def parse_comment(self, article_id, page):
        print("parse_comment::page = ", page)
        # https://www.qiushibaike.com/commentpage/122204240?page=2&count=10
        url = "https://www.qiushibaike.com/commentpage/" + str(article_id) + "?page=" + str(page) + "&count=10"
        print("parse_comment::url = ", url)
        driver = self.get_web_content(url)

        comment_parent_path = '//div[@class="comments-list comments-all clearfix"]'
        comment_parent_object = driver.find_element_by_xpath(comment_parent_path)

        self.parse_page_comment(comment_parent_object)

        comment_pager_path = './/div[@class="pager"]'
        comment_pager_object = comment_parent_object.find_element_by_xpath(comment_pager_path)

        comment_pager_items_path = './/span[@class="page-numbers"]'
        comment_pager_items_object = comment_pager_object.find_elements_by_xpath(comment_pager_items_path)
        if len(comment_pager_items_object) > 0:
            max_page = int(comment_pager_items_object[len(comment_pager_items_object) - 1].text)
            print("parse_comment::max_page = ", max_page)
            if page < max_page:
                self.parse_comment(article_id, page + 1)

        driver.close()

    def parse_page_comment(self, comment_parent_object):
        try:
            comment_list_path = './/div[@class="comment-list clearfix"]'
            comment_list_object = comment_parent_object.find_element_by_xpath(comment_list_path)

            comment_item_path = './/div[starts-with(@id,"comment-")]'
            comment_items_object = comment_list_object.find_elements_by_xpath(comment_item_path)

            for comment_item_object in comment_items_object:
                comment_user_path = './/a[@class="userlogin"]'
                comment_user_object = comment_item_object.find_element_by_xpath(comment_user_path)
                comment_user_name = comment_user_object.text

                comment_content_path = './/span[@class="body"]'
                comment_content_object = comment_item_object.find_element_by_xpath(comment_content_path)
                comment_content = comment_content_object.text

                print(comment_user_name)
                print(comment_content)
        except NoSuchElementException as e:
            print(e)


    def get_detail(self, hot_pic_id, url):
        print("start_task::", 'Now Time::', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.parse(hot_pic_id, url)


if __name__ == "__main__":
    request = RequestQsbkHotPicDetail()
    # request.parse("https://www.qiushibaike.com/article/122197536")
    request.parse("", "https://www.qiushibaike.com/article/122204240")
