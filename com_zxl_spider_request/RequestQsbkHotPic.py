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


class RequestQsbkTxt(BaseRequest):

    def __init__(self):
        global jokeDB
        jokeDB = JokeDB()

    def parse(self, end_url, index):
        print("parse::end_url = ", end_url, "::index = ", index)

        driver = self.get_web_content("https://www.qiushibaike.com/" + end_url + str(index))

        elem1 = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//ul[@class="pagination"]')))
        print("elem1 = ", elem1)
        elem2 = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="article block untagged mb15"]')))
        print("elem2 = ", elem2)

        # page_source = driver.page_source

        isFindNextPage = False
        paginationObject = driver.find_element_by_xpath('//ul[@class="pagination"]')
        pageListObject = paginationObject.find_elements_by_xpath('.//li')
        for pageItemObject in pageListObject:
            page_index_txt = pageItemObject.text
            print("pageItemObject::page_index_txt = ", page_index_txt)
            itemFindResult = re.findall(".*?(\d+).*?", page_index_txt)
            print("pageItemObject::itemFindResult = ", itemFindResult)
            if len(itemFindResult) > 0:
                if int(itemFindResult[0]) > index:
                    index = int(itemFindResult[0])
                    isFindNextPage = True
                    break
                # if index - int(itemFindResult[0]) == 1:
                #     index = int(itemFindResult[0])
                #     isFindNextPage = True
                #     break
        print("parse::isFindNextPage = ", isFindNextPage, "::index = ", index, "::end_url = ",)

        hotPicJokeItemPath = '//div[@class="article block untagged mb15"]'
        hotPicJokeItems = driver.find_elements_by_xpath(hotPicJokeItemPath)

        print('hotPicJokeItems length = ', len(hotPicJokeItems))

        for hotPicJokeItem in hotPicJokeItems:
            jokeId = hotPicJokeItem.get_attribute('id')
            md5Object = hashlib.md5()
            md5Object.update(jokeId.encode('utf-8'))
            jokeMd5Value = md5Object.hexdigest()

            authorObject = hotPicJokeItem.find_element_by_xpath('.//div[@class="author clearfix"]')
            authorNickObject = authorObject.find_element_by_xpath('.//h2')
            authorNickName = authorNickObject.text
            authorImgObject = authorObject.find_element_by_xpath('.//img')
            authorImgUrl = authorImgObject.get_attribute('src')

            authorGender = ''
            authorAge = -1
            try:
                authorGenderObject = authorObject.find_element_by_xpath(".//div[starts-with(@class,'articleGender')]")
                authorGender = authorGenderObject.get_attribute('class')
                authorAge = authorGenderObject.text
            except NoSuchElementException as e:
                print(e)

            contentObject = hotPicJokeItem.find_element_by_xpath('.//div[@class="content"]')
            content = contentObject.text

            thumbImgUrl = ''
            try:
                thumbObject = hotPicJokeItem.find_element_by_xpath('.//div[@class="thumb"]')
                thumbImgObject = thumbObject.find_element_by_xpath('.//img')
                thumbImgUrl = thumbImgObject.get_attribute('src')
            except NoSuchElementException as e:
                print(e)

            statsVoteContent = ''
            statsCommentContent = ''
            statsCommentDetailUrl = ''
            try:
                statsObject = hotPicJokeItem.find_element_by_xpath('.//div[@class="stats"]')
                try:
                    statsVoteObject = statsObject.find_element_by_xpath('.//span[@class="stats-vote"]')
                    statsVoteContent = statsVoteObject.text
                except NoSuchElementException as e:
                    print(e)
                try:
                    statsCommentObject = statsObject.find_element_by_xpath('.//span[@class="stats-comments"]')
                    statsCommentContent = statsCommentObject.find_element_by_xpath(
                        './/a[@class="qiushi_comments"]').text
                    statsCommentDetailUrl = statsCommentObject.find_element_by_xpath(
                        './/a[@class="qiushi_comments"]').get_attribute('href')
                except NoSuchElementException as e:
                    print(e)
            except NoSuchElementException as e:
                print(e)

            # print authorNickName
            # print authorGender
            # print authorAge
            # print authorImgUrl
            # print content
            # print thumbImgUrl
            # print statsVoteContent
            # print statsCommentContent
            # print statsCommentDetailUrl
            # print jokeId
            # print jokeMd5Value

            # print '\n'
            # print '======================================end=========================================='
            # print '\n'

            joke_bean = JokeBean()
            joke_bean = joke_bean.create_joke_bean(
                authorNickName.encode('utf-8'),
                authorGender,
                authorAge,
                authorImgUrl,
                content.encode('utf-8'),
                thumbImgUrl,
                statsVoteContent,
                statsCommentContent,
                statsCommentDetailUrl,
                jokeMd5Value)

            isExistJokeItem = jokeDB.query_by_md5(jokeMd5Value)
            print(isExistJokeItem)
            if isExistJokeItem is None:
                print("not ExistJokeItem")
                jokeDB.insert_joke(joke_bean)
            else:
                print("ExistJokeItem")
                driver.close()
                return

        print("==============end=================")
        print("\n")

        driver.close()
        if not isFindNextPage:
            return
        else:
            self.parse(end_url, index)

    def close_db(self):
        if jokeDB is not None:
            jokeDB.close_db()

    def start_task(self):
        print("start_task::", 'Now Time::', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.parse("pic/page/", 1)
        self.close_db()


if __name__ == "__main__":
    request = RequestQsbkTxt()
    # request.parse("pic/page/", 1)
    request.parse("pic/page/", 1)

    request.clas_db()
