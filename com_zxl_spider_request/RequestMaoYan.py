#!/usr/bin/python
# coding=utf-8
import re

from selenium.common.exceptions import NoSuchElementException

from com_zxl_spider_db.StarDB import StarDB
from com_zxl_spider_data.StarInfoBean import StarInfoBean
from com_zxl_spider_request.BaseRequest import BaseRequest


class RequestStarPic(BaseRequest):

    def __init__(self):
        pass

    def request(self, url):
        print("request::url = %s " % url)
        driver = self.get_web_content(url)
        # print(driver.page_source)

        movies_list_path = "//div[@class='movies-list']"
        movies_list_obj = driver.find_element_by_xpath(movies_list_path)

        movie_items_path = ".//dd"
        movie_items_obj = movies_list_obj.find_elements_by_xpath(movie_items_path)

        for movie_item in movie_items_obj:
            print("----------start-----------")
            movie_item_path = ".//div[@class='movie-item']"
            movie_item_obj = movie_item.find_element_by_xpath(movie_item_path)

            movie_poster_path = ".//div[@class='movie-poster']"
            movie_poster_obj = movie_item_obj.find_element_by_xpath(movie_poster_path)

            movie_poster_img_list_obj = movie_poster_obj.find_elements_by_xpath(".//img")
            movie_poster_url = ''
            movie_poster_default_url = ''
            for movie_poster_img in movie_poster_img_list_obj:
                if movie_poster_img.get_attribute('data-src') is None:
                    movie_poster_default_url = movie_poster_img.get_attribute('src')
                else:
                    movie_poster_url = movie_poster_img.get_attribute('data-src')

            if movie_poster_url == '':
                movie_poster_url = movie_poster_default_url

            movie_item_detail_path = ".//div[@class='channel-detail movie-item-title']"
            movie_item_detail_obj = movie_item.find_element_by_xpath(movie_item_detail_path)
            movie_item_detail_obj = movie_item_detail_obj.find_element_by_xpath(".//a")
            movie_id = movie_item_detail_obj.get_attribute('data-val')
            movie_title = movie_item_detail_obj.text
            movie_detail_url = movie_item_detail_obj.get_attribute('href')

            print("movie_id = %s" % movie_id)
            print("movie_title = %s" % movie_title)
            print("movie_poster_url = %s" % movie_poster_url)
            print("movie_detail_url = %s" % movie_detail_url)

            print("----------end-----------\n")

        try:
            page_list_path = '//ul[@class="list-pager"]'
            page_list_obj = driver.find_element_by_xpath(page_list_path)

            page_items = page_list_obj.find_elements_by_xpath(".//a")
            for page_item in page_items:
                page_item_text = page_item.text
                if page_item_text == '下一页':
                    self.request(page_item.get_attribute("href"))
        except NoSuchElementException as e:
            print(e)

        driver.close()


if __name__ == "__main__":
    request = RequestStarPic()
    # request.request("https://maoyan.com/films?showType=1")
    # request.request("https://maoyan.com/films?showType=2")
    request.request("https://maoyan.com/films?showType=3")