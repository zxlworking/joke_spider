#!/usr/bin/python
# coding=utf-8
import base64
import json
import os
import re
import time
from urllib import request

import requests
from fontTools.ttLib import TTFont
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from com_zxl_spider_request.BaseRequest import BaseRequest


class RequestNowMaoYan(BaseRequest):

    def __init__(self):
        pass

    def request(self, movie_id, movie_detail_url):
        print("request::movie_id = %s " % movie_id)
        print("request::movie_detail_url = %s " % movie_detail_url)
        # driver = self.get_web_content(movie_detail_url)
        driver = self.login_mao_yan()

        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')  # 触发ctrl + t
        time.sleep(5)

        driver.get(movie_detail_url)
        page_content = driver.page_source
        # print(page_content)

        print("=====start======")
        woff_url = ''
        find_result = re.findall(r'.*?url\(\'(.*?)\'\).*?', page_content)
        if len(find_result) > 0:
            for woff_url in find_result:
                if 'woff' in woff_url:
                    woff_url = "http:" + woff_url
                    print("woff_url--->", woff_url)
                    font_request = request.Request(woff_url)
                    font_res = request.urlopen(font_request)
                    font_respoen = font_res.read()
                    font_file = open('mao_yan_font.woff', 'wb')
                    font_file.write(font_respoen)
                    font_file.close()
                    woff_font = TTFont("mao_yan_font.woff")
                    woff_font.saveXML("mao_yan_font.xml")
        print("=====end======")

        try:
            movie_detail_path = "//div[@class='banner']"
            movie_detail_object = driver.find_element_by_xpath(movie_detail_path)

            movie_avatar_path = ".//img[@class='avatar']"
            movie_avatar_object = movie_detail_object.find_element_by_xpath(movie_avatar_path)
            movie_avatar_url = movie_avatar_object.get_attribute("src")
            if '@' in movie_avatar_url:
                movie_avatar_url = movie_avatar_url.split('@')[0]

            movie_introduce_path = ".//div[@class='celeInfo-right clearfix']"
            movie_introduce_object = movie_detail_object.find_element_by_xpath(movie_introduce_path)

            movie_brief_path = ".//div[@class='movie-brief-container']"
            movie_brief_object = movie_introduce_object.find_element_by_xpath(movie_brief_path)

            movie_name_path = ".//h3[@class='name']"
            movie_name_object = movie_brief_object.find_element_by_xpath(movie_name_path)
            movie_name = movie_name_object.text

            movie_en_name_path = ".//div[@class='ename ellipsis']"
            movie_en_name_object = movie_brief_object.find_element_by_xpath(movie_en_name_path)
            movie_en_name = movie_en_name_object.text

            movie_brief_info_list_path = ".//li"
            movie_brief_info_list_object = movie_brief_object.find_elements_by_xpath(movie_brief_info_list_path)

            movie_category = ''
            movie_country = ''
            movie_duration = ''
            movie_release_info = ''

            if len(movie_brief_info_list_object) > 0:
                movie_category = movie_brief_info_list_object[0].text
            if len(movie_brief_info_list_object) > 1:
                temp_str = movie_brief_info_list_object[1].text
                movie_country = temp_str
                if "/" in temp_str:
                    temp_str = temp_str.replace(" ", "")
                    temp_str = temp_str.split("/")
                    if len(temp_str) > 1:
                        movie_country = temp_str[0]
                        movie_duration = temp_str[1]
            movie_release_time = ''
            movie_release_area = ''
            if len(movie_brief_info_list_object) > 2:
                movie_release_info = movie_brief_info_list_object[2].text
                movie_release_info_find_result = re.findall('(\\d+.*?\\d+.*?\\d+.*?\\d+.*?\\d+)(.+)', movie_release_info, re.S)
                print("movie_release_info_find_result = ", movie_release_info_find_result)
                if len(movie_release_info_find_result) > 0 and len(movie_release_info_find_result[0]) > 1:
                    movie_release_time = movie_release_info_find_result[0][0]
                    movie_release_area = movie_release_info_find_result[0][1]

            movie_stats_path = ".//div[@class='movie-stats-container']"
            movie_stats_object = movie_introduce_object.find_element_by_xpath(movie_stats_path)

            movie_score_path = ".//span[@class='index-left info-num ']"
            movie_score_object = movie_stats_object.find_element_by_xpath(movie_score_path)
            movie_score_content_path = ".//span"
            movie_score_content_object = movie_score_object.find_element_by_xpath(movie_score_content_path)
            movie_score_content = self.get_mao_yan_num(woff_url, movie_score_content_object.text, "score.png")
            # movie_score_content = self.get_mao_yan_num_by_object(movie_score_content_object, "score.png")

            movie_stats_people_count_parent_path = ".//span[@class='score-num']"
            movie_stats_people_count_parent_object = movie_stats_object.find_element_by_xpath(movie_stats_people_count_parent_path)
            movie_stats_people_count_path = ".//span"
            movie_stats_people_count_object = movie_stats_people_count_parent_object.find_element_by_xpath(movie_stats_people_count_path)
            movie_stats_people_count_content = self.get_mao_yan_num(woff_url, movie_stats_people_count_object.text, "stats_people_count.png")
            # movie_stats_people_count_content = self.get_mao_yan_num_by_object(movie_stats_people_count_object, "stats_people_count.png")
            temp_movie_stats_people_count_unit_content = movie_stats_people_count_object.text
            print("temp_movie_stats_people_count_unit_content = ", temp_movie_stats_people_count_unit_content, len(temp_movie_stats_people_count_unit_content))
            movie_stats_people_count_unit_content = temp_movie_stats_people_count_unit_content[len(temp_movie_stats_people_count_unit_content)-1:len(temp_movie_stats_people_count_unit_content)]

            movie_box_path = ".//div[@class='movie-index-content box']"
            movie_box_object = movie_stats_object.find_element_by_xpath(movie_box_path)

            movie_box_value_path = ".//span[@class='stonefont']"
            movie_box_value_object = movie_box_object.find_element_by_xpath(movie_box_value_path)
            movie_box_value_content = self.get_mao_yan_num(woff_url, movie_box_value_object.text, "box.png")
            # movie_box_value_content = self.get_mao_yan_num_by_object(movie_box_value_object, "box.png")

            movie_box_unit_path = ".//span[@class='unit']"
            movie_box_unit_object = movie_box_object.find_element_by_xpath(movie_box_unit_path)
            movie_box_unit_content = movie_box_unit_object.text


            # ================tab==================
            tab_content_path = "//div[@class='tab-content-container']"
            tab_content_object = driver.find_element_by_xpath(tab_content_path)

            # ================简介 评论============
            introduce_content = ''
            comment_list_object = None

            tab_content_detail_path = ".//div[@class='tab-desc tab-content active']"
            tab_content_detail_object = tab_content_object.find_element_by_xpath(tab_content_detail_path)

            tab_content_detail_list_path = ".//div[@class='module']"
            tab_content_detail_list_object = tab_content_detail_object.find_elements_by_xpath(tab_content_detail_list_path)
            print("tab_content_detail_list_object = ",  len(tab_content_detail_list_object), tab_content_detail_list_object)
            if len(tab_content_detail_list_object) >= 4:
                introduce_object = tab_content_detail_list_object[0].find_element_by_xpath(".//span[@class='dra']")
                introduce_content = introduce_object.text

                comment_list_object = tab_content_detail_list_object[3].find_element_by_xpath(".//div[@class='comment-list-container']").find_elements_by_xpath(".//li")


            # ================演职人员==============
            tab_celebrity_path = ".//div[@class='tab-celebrity tab-content']"
            tab_celebrity_object = tab_content_object.find_element_by_xpath(tab_celebrity_path)
            tab_celebrity_list_object = tab_celebrity_object.find_elements_by_xpath(".//div[@class='celebrity-group']")
            print("tab_celebrity_list_object = ",  len(tab_celebrity_list_object), tab_celebrity_list_object)

            # ================奖项=================
            tab_award_path = ".//div[@class='tab-award tab-content']"
            tab_award_object = tab_content_object.find_element_by_xpath(tab_award_path)
            tab_award_list_object = tab_award_object.find_elements_by_xpath(".//li[@class='award-item']")
            print("tab_award_list_object = ",  len(tab_award_list_object), tab_award_list_object)

            # ================图集=================
            tab_img_path = ".//div[@class='tab-img tab-content']"
            tab_img_object = tab_content_object.find_element_by_xpath(tab_img_path)
            tab_img_list_object = tab_img_object.find_elements_by_xpath(".//li")
            print("tab_img_list_object = ",  len(tab_img_list_object), tab_img_list_object)

            print("movie_avatar_url = ", movie_avatar_url)
            print("movie_name = ", movie_name)
            print("movie_en_name ", movie_en_name)
            print("movie_category ", movie_category)
            print("movie_country = ", movie_country)
            print("movie_duration = ", movie_duration)
            print("movie_release_info = ", movie_release_info)
            print("movie_release_time = ", movie_release_time)
            print("movie_release_area = ", movie_release_area)
            print("movie_score_content = ", movie_score_content)
            print("movie_stats_people_count_content = ", movie_stats_people_count_content)
            print("movie_stats_people_count_unit_content = ", movie_stats_people_count_unit_content)
            print("movie_box_value_content = ", movie_box_value_content)
            print("movie_box_unit_content = ", movie_box_unit_content)

            print("introduce_content = ", introduce_content)
            print("comment_list_object = ", comment_list_object)

        except NoSuchElementException as noSuchElementException:
            print(noSuchElementException)

        driver.close()

    def get_mao_yan_num(self, woff_url, num_content, img_save_name):
        print("get_mao_yan_num::num_content = ", num_content)
        print("get_mao_yan_num::woff_url = ", woff_url)

        replace_woff_url = '------'
        replace_num_content = '======'

        temp_file = open('base_maoyan_detail.html', 'r', encoding='utf-8')
        new_file = open('new_maoyan_detail.html', 'wb')

        line = temp_file.readline()
        while len(line) > 0:
            if replace_woff_url in line:
                line = line.replace(replace_woff_url, woff_url)
            if replace_num_content in line:
                line = line.replace(replace_num_content, num_content)
            line = line.replace("\n", "")
            new_file.write(line.encode())
            line = temp_file.readline()
            # print("get_mao_yan_num::line = ", line)
            # print("get_mao_yan_num::len(line) = ", len(line))

        new_file.close()
        temp_file.close()

        new_file_path = 'file://' + os.path.abspath('new_maoyan_detail.html')
        print("get_mao_yan_num::new_file_path = ", new_file_path)
        new_driver = self.get_web_content(new_file_path)
        new_driver.get_screenshot_as_file(img_save_name)
        print("get_mao_yan_num::page_source = ", new_driver.page_source)
        num_pic_base64 = new_driver.get_screenshot_as_base64()
        print("get_mao_yan_num::num_pic_base64 = ", num_pic_base64)
        new_driver.close()

        baidu_token_result = requests.get(
            'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Wk03dOF1kRG1SnajCmyKELNx&client_secret=XAqRaMFFCUY2ZUGNSvtGsL8ZYbYRkERp&')
        print('baidu_token_result_json = ', baidu_token_result.text)
        baidu_token_result_json = json.loads(baidu_token_result.text)
        print('baidu_token = ', baidu_token_result_json['access_token'])

        postdata = {'access_token': baidu_token_result_json['access_token'], 'image': num_pic_base64}
        # result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic', data=postdata)
        result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic', data=postdata)
        # result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/webimage', data=postdata)
        # result =  {"log_id": 2337563219107430326, "words_result_num": 1, "words_result": [{"words": "9.4"}]}
        print("result = ", result.text)
        result_json_object = json.loads(result.text)

        words = ''
        if 'words_result' in result_json_object:
            words_result = result_json_object['words_result']
            if len(words_result) > 0:
                words = words_result[0]['words']
                words_find_result = re.findall('(\\d+.?\\d+).*?', words, re.S)
                if len(words_find_result) > 0:
                    words = words_find_result[0]

        print("words = ", words)

        return words

    # def get_mao_yan_num_by_object(self, num_object, img_save_name):
    #
    #     num_object.screenshot(img_save_name)
    #
    #     num_pic_base64_data = ''
    #     with open(img_save_name, 'rb') as f:
    #         base64_data = base64.b64encode(f.read())
    #         s = base64_data.decode()
    #         # print('data:image/jpeg;base64,%s' % s)
    #         num_pic_base64_data = num_pic_base64_data + s
    #
    #     baidu_token_result = requests.get(
    #         'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Wk03dOF1kRG1SnajCmyKELNx&client_secret=XAqRaMFFCUY2ZUGNSvtGsL8ZYbYRkERp&')
    #     print('baidu_token_result_json = ', baidu_token_result.text)
    #     baidu_token_result_json = json.loads(baidu_token_result.text)
    #     print('baidu_token = ', baidu_token_result_json['access_token'])
    #
    #     postdata = {'access_token': baidu_token_result_json['access_token'], 'image': num_pic_base64_data}
    #     # result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic', data=postdata)
    #     result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic', data=postdata)
    #     # result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/webimage', data=postdata)
    #     # result =  {"log_id": 2337563219107430326, "words_result_num": 1, "words_result": [{"words": "9.4"}]}
    #     print("result = ", result.text)
    #     result_json_object = json.loads(result.text)
    #
    #     words = ''
    #     if 'words_result' in result_json_object:
    #         words_result = result_json_object['words_result']
    #         if len(words_result) > 0:
    #             words = words_result[0]['words']
    #             words_find_result = re.findall('(\\d+.?\\d+).*?', words, re.S)
    #             if len(words_find_result) > 0:
    #                 words = words_find_result[0]
    #
    #     print("words = ", words)
    #
    #     return words

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
        print("login success")
        return driver


if __name__ == "__main__":
    requestNowMaoYan = RequestNowMaoYan()
    # 267
    # requestNowMaoYan.request("1211270", "https://maoyan.com/films/1230121")
    requestNowMaoYan.request("1211270", "https://maoyan.com/films/1211270")
    # requestNowMaoYan.request("1211270", "https://passport.meituan.com/account/unitivelogin?service=maoyan&continue=https%3A%2F%2Fmaoyan.com%2Fpassport%2Flogin%3Fredirect%3D%252F")

    # new_driver = requestNowMaoYan.get_web_content("file:///home/mi/zxl/workspace/my_github/joke_spider/com_zxl_spider_request/new_maoyan_detail.html")
    # time.sleep(10)
    # new_driver.get_screenshot_as_file('new_maoyan_detail.png')
    # print("get_mao_yan_num::page_source = ", new_driver.page_source)
    # new_driver.close()
    # while True:
    #     pass

    # num_pic_base64 = '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ACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAAAqgQgAAMAIRAAAACqBCAAAwAhEAAAAKoEIAADACEQAAACq+j+Gse57AvcRUgAAAABJRU5ErkJggg=='
    # baidu_token_result = requests.get(
    #     'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Wk03dOF1kRG1SnajCmyKELNx&client_secret=XAqRaMFFCUY2ZUGNSvtGsL8ZYbYRkERp&')
    # print('baidu_token_result_json = ', baidu_token_result.text)
    # baidu_token_result_json = json.loads(baidu_token_result.text)
    # print('baidu_token = ', baidu_token_result_json['access_token'])
    #
    # postdata = {'access_token': baidu_token_result_json['access_token'], 'image': num_pic_base64}
    # result = requests.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic', data=postdata)
    # print("result = ", result.text)
