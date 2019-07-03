#!/usr/bin/python
# coding=utf-8
import re

from com_zxl_spider_request.BaseRequest import BaseRequest


class RequestStarPic(BaseRequest):

    def parse(self, index):
        print("index::",index)
        driver = self.get_web_content("http://www.mingxing.com/ziliao/index?&p=%s"%index)
        # print(driver.page_source)

        pageObject = driver.find_element_by_xpath('//div[@class="page_starlist"]')
        starPicItems = pageObject.find_elements_by_xpath('.//li')

        print("starPicItems::", len(starPicItems))

        for starPicItem in starPicItems:
            starImgObject = starPicItem.find_element_by_xpath('.//img')
            starImgUrl = starImgObject.get_attribute('src')
            starNameObject = starPicItem.find_element_by_xpath('.//h3')
            starName = starNameObject.text

            print(starName, "---", starImgUrl)

        lastPageValue = 1
        pageBottomObject = driver.find_element_by_xpath('//div[@class="pages"]')
        lastPageBottomObject = pageBottomObject.find_element_by_xpath('//a[@title="末页"]')
        lastPageBottomContent = lastPageBottomObject.get_attribute('href')
        lastPageContent = re.findall(".*?p=(\\d+)", lastPageBottomContent)
        if(len(lastPageContent) > 0):
            lastPageValue = int(lastPageContent[0])

        if(index > lastPageValue):
            return
        else:
            index = index + 1
            self.parse(index)


if __name__ == "__main__":
    request = RequestStarPic()
    request.parse(1)