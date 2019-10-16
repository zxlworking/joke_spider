#!/usr/bin/python
# coding=utf-8
import base64
import re
import time
from urllib import request

from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from com_zxl_spider_data.MaoYanBean import MaoYanBean
from com_zxl_spider_db.MaoYanDB import MaoYanDB
from com_zxl_spider_request.BaseRequest import BaseRequest


class RequestNowMaoYan(BaseRequest):

    fontdict = {'uniE997': '0', 'uniEE22': '8', 'uniE526': '9', 'uniF652': '2', 'uniE811': '6',
                'uniE635': '3', 'uniF85A': '1', 'uniE6D4': '4', 'uniE9C8': '5', 'uniEA6D': '7'}

    def __init__(self):
        pass

    def request(self, movie_id, movie_detail_url):
        print("request::movie_id = %s " % movie_id)
        print("request::movie_detail_url = %s " % movie_detail_url)
        # driver = self.get_web_content(movie_detail_url)
        driver = self.login_mao_yan()
        driver.get("view-source:" + movie_detail_url)
        page_content = driver.page_source
        print(page_content)

        print("===============BeautifulSoup\n\n\n\n\n\n\n")

        soup = BeautifulSoup(page_content, 'lxml')
        print(soup.find_all('&#x'))

        # print("=====start======")
        # woff_font = None
        # find_result = re.findall(r'.*?url\(\'(.*?)\'\).*?', page_content)
        # if len(find_result) > 0:
        #     for woff_url in find_result:
        #         if 'woff' in woff_url:
        #             woff_url = "http:" + woff_url
        #             print("woff_url--->", woff_url)
        #             font_request = request.Request(woff_url)
        #             font_res = request.urlopen(font_request)
        #             font_respoen = font_res.read()
        #             font_file = open('mao_yan_font.woff', 'wb')
        #             font_file.write(font_respoen)
        #             font_file.close()
        #             woff_font = TTFont("mao_yan_font.woff")
        #             woff_font.saveXML("mao_yan_font.xml")
        #             print('respoen::', font_respoen)
        # print("=====end======")
        #
        # try:
        #     movie_detail_path = "//div[@class='banner']"
        #     movie_detail_object = driver.find_element_by_xpath(movie_detail_path)
        #
        #     movie_avatar_path = ".//img[@class='avatar']"
        #     movie_avatar_object = movie_detail_object.find_element_by_xpath(movie_avatar_path)
        #     movie_avatar_url = movie_avatar_object.get_attribute("src")
        #
        #     movie_introduce_path = ".//div[@class='celeInfo-right clearfix']"
        #     movie_introduce_object = movie_detail_object.find_element_by_xpath(movie_introduce_path)
        #
        #     movie_brief_path = ".//div[@class='movie-brief-container']"
        #     movie_brief_object = movie_introduce_object.find_element_by_xpath(movie_brief_path)
        #
        #     movie_name_path = ".//h3[@class='name']"
        #     movie_name_object = movie_brief_object.find_element_by_xpath(movie_name_path)
        #     movie_name = movie_name_object.text
        #
        #     movie_en_name_path = ".//div[@class='ename ellipsis']"
        #     movie_en_name_object = movie_brief_object.find_element_by_xpath(movie_en_name_path)
        #     movie_en_name = movie_en_name_object.text
        #
        #     movie_brief_info_list_path = ".//li"
        #     movie_brief_info_list_object = movie_brief_object.find_elements_by_xpath(movie_brief_info_list_path)
        #
        #     movie_category = ''
        #     movie_country = ''
        #     movie_duration = ''
        #     movie_release_info = ''
        #
        #     if len(movie_brief_info_list_object) > 0:
        #         movie_category = movie_brief_info_list_object[0].text
        #     if len(movie_brief_info_list_object) > 1:
        #         temp_str = movie_brief_info_list_object[1].text
        #         movie_country = temp_str
        #         if "/" in temp_str:
        #             temp_str = temp_str.replace(" ", "")
        #             temp_str = temp_str.split("/")
        #             if len(temp_str) > 1:
        #                 movie_country = temp_str[0]
        #                 movie_duration = temp_str[1]
        #     if len(movie_brief_info_list_object) > 2:
        #         movie_release_info = movie_brief_info_list_object[2].text
        #
        #     movie_stats_path = ".//div[@class='movie-stats-container']"
        #     movie_stats_object = movie_introduce_object.find_element_by_xpath(movie_stats_path)
        #
        #     movie_score_path = ".//span[@class='index-left info-num ']"
        #     movie_score_object = movie_stats_object.find_element_by_xpath(movie_score_path)
        #     movie_score_content_path = ".//span"
        #     movie_score_content_object = movie_score_object.find_element_by_xpath(movie_score_content_path)
        #
        #     print(movie_score_content_object.get_attribute('innerHTML'))
        #     file = open('test_num.txt', 'wb')
        #     regex_font = re.compile('(?<=&#x).{4}(?=;)')
        #     ms = regex_font.findall(movie_score_content_object.text)
        #     for m in ms:
        #         file.write(m)
        #     file.close()
        #
        #     movie_score_find_result = re.findall(".*?&#x(.*?);.&#x(.*?);", movie_score_content_object.text)
        #     print("movie_score_find_result = ", movie_score_find_result)
        #     if len(movie_score_find_result) > 0:
        #         for movie_score_find_item in movie_score_find_result:
        #             print("movie_score_find_result = ", movie_score_find_item)
        #             self.get_mao_yan_num(movie_score_find_item, woff_font)
        #
        #     print("movie_avatar_url = %s" % movie_avatar_url)
        #     print("movie_name = %s" % movie_name)
        #     print("movie_en_name = %s" % movie_en_name)
        #     print("movie_category = %s" % movie_category)
        #     print("movie_country = %s" % movie_country)
        #     print("movie_duration = %s" % movie_duration)
        #     print("movie_release_info = %s" % movie_release_info)
        #     print("movie_score_content = ", '')
        #
        # except NoSuchElementException as noSuchElementException:
        #     print(noSuchElementException)

        driver.close()


    def get_mao_yan_num(self, num_str, woff_font):
        print("get_mao_yan_num::num_str = ", num_str)
        if woff_font is not None:
            new_font_value = woff_font['glyf'][num_str.upper()]
            print("new_font_key = ", new_font_value)
            base_woff_font = TTFont("base_mao_yan_font.woff")
            for k, v in self.fontdict:
                if new_font_value == base_woff_font['glyf'][k]:
                    return v
        return 0

    def login_mao_yan(self):
        driver = self.get_web_content(
            "https://passport.meituan.com/account/unitivelogin?service=maoyan&continue=https%3A%2F%2Fmaoyan.com%2Fpassport%2Flogin%3Fredirect%3D%252F")
        user_name_input = driver.find_element_by_xpath("//input[@class='f-text phone-input']")
        pass_word_input = driver.find_element_by_xpath("//input[@class='f-text pw-input']")
        login_input = driver.find_element_by_xpath("//input[@value='登录']")
        user_name_input.send_keys('15850687360')
        pass_word_input.send_keys('working')
        login_input.click()
        time.sleep(10)
        return driver


if __name__ == "__main__":
    requestNowMaoYan = RequestNowMaoYan()
    requestNowMaoYan.request("1211270", "https://maoyan.com/films/1230121")
    # requestNowMaoYan.request("1211270", "https://passport.meituan.com/account/unitivelogin?service=maoyan&continue=https%3A%2F%2Fmaoyan.com%2Fpassport%2Flogin%3Fredirect%3D%252F")


