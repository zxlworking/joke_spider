#!/usr/bin/python
# coding=utf-8
import datetime
import hashlib
import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from com_zxl_spider_db.JokeDB import JokeDB
from com_zxl_spider_request.BaseRequest import *
from com_zxl_spider_data.JokeBean import *


class RequestQsbkHomeTxt(BaseRequest):

    def __init__(self):
        global jokeDB
        jokeDB = JokeDB()
        # jokeDB.delete_joke()

    def parse(self, url_path):
        print("parse::url_path = ", url_path)

        driver = self.get_web_content("https://www.qiushibaike.com/" + url_path)
        page_source = driver.page_source
        # print("parse::page_source::\n")
        # print(page_source)

        text_joke_item_path = "//div[starts-with(@class,'article block untagged mb15')]"
        text_joke_items = driver.find_elements_by_xpath(text_joke_item_path)

        print('text_joke_items length = ', len(text_joke_items))

        for text_joke_item in text_joke_items:
            joke_id = text_joke_item.get_attribute('id')
            md5_object = hashlib.md5()
            md5_object.update(joke_id.encode('utf-8'))
            joke_md5_value = md5_object.hexdigest()

            author_object = text_joke_item.find_element_by_xpath('.//div[@class="author clearfix"]')
            author_nick_object = author_object.find_element_by_xpath('.//h2')
            author_nick_name = author_nick_object.text
            author_img_object = author_object.find_element_by_xpath('.//img')
            author_img_url = author_img_object.get_attribute('src')

            author_gender = ''
            author_age = -1
            try:
                author_gender_object = author_object.find_element_by_xpath(".//div[starts-with(@class,'articleGender')]")
                author_gender = author_gender_object.get_attribute('class')
                author_age = author_gender_object.text
            except NoSuchElementException as e:
                print(e)

            content_object = text_joke_item.find_element_by_xpath('.//div[@class="content"]')
            content = content_object.text

            thumb_img_url = ''
            try:
                thumb_object = text_joke_item.find_element_by_xpath('.//div[@class="thumb"]')
                thumb_img_object = thumb_object.find_element_by_xpath('.//img')
                thumb_img_url = thumb_img_object.get_attribute('src')
            except NoSuchElementException as e:
                print(e)

            stats_vote_content = ''
            stats_comment_content = ''
            stats_comment_detail_url = ''
            try:
                stats_object = text_joke_item.find_element_by_xpath('.//div[@class="stats"]')
                try:
                    stats_vote_object = stats_object.find_element_by_xpath('.//span[@class="stats-vote"]')
                    stats_vote_content = stats_vote_object.text
                except NoSuchElementException as e:
                    print(e)
                try:
                    stats_comment_object = stats_object.find_element_by_xpath('.//span[@class="stats-comments"]')
                    stats_omment_content = stats_comment_object.find_element_by_xpath(
                        './/a[@class="qiushi_comments"]').text
                    stats_comment_detail_url = stats_comment_object.find_element_by_xpath(
                        './/a[@class="qiushi_comments"]').get_attribute('href')
                except NoSuchElementException as e:
                    print(e)
            except NoSuchElementException as e:
                print(e)

            print(author_nick_name)
            print(author_gender)
            print(author_age)
            print(author_img_url)
            print(content)
            print(thumb_img_url)
            print(stats_vote_content)
            print(stats_comment_content)
            print(stats_comment_detail_url)
            print(joke_id)
            print(joke_md5_value)

            print('\n')
            print('======================================text_joke_item end==========================================')
            print('\n')

            joke_bean = JokeBean()
            joke_bean = joke_bean.create_joke_bean(
                author_nick_name.encode('utf-8'),
                author_gender,
                author_age,
                author_img_url,
                content.encode('utf-8'),
                thumb_img_url,
                stats_vote_content,
                stats_comment_content,
                stats_comment_detail_url,
                joke_md5_value)

            is_exist_joke_item = jokeDB.query_by_md5(joke_md5_value)
            print(is_exist_joke_item)
            if is_exist_joke_item is None:
                print("not ExistJokeItem")
                jokeDB.insert_joke(joke_bean)
            else:
                print("ExistJokeItem")
                driver.close()
                return

        print("==============parse end=================")
        print("\n")

        driver.close()

    def close_db(self):
        if jokeDB is not None:
            jokeDB.close_db()

    def start_task(self):
        print("start_task::", 'Now Time::', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.parse("text")
        self.close_db()


if __name__ == "__main__":
    request = RequestQsbkHomeTxt()
    request.parse("text")

    request.close_db()
