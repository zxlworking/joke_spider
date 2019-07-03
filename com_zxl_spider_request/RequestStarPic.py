#!/usr/bin/python
# coding=utf-8
import re

from com_zxl_spider_request.BaseRequest import BaseRequest


class RequestStarPic(BaseRequest):

    def request(self):
        driver = self.get_web_content("http://www.mingxing.com/ziliao/index.html")
        main_object = driver.find_element_by_xpath('//div[@class="t_05"]')
        category_items = main_object.find_elements_by_xpath('.//a')
        for category_tem in category_items:
            print('=========================================================\n')
            print(category_tem.text)
            if category_tem.text != '全部分类':
                self.parse(category_tem.get_attribute('href'), 1)
        driver.close()

    def parse(self, category_url, index):
        print("category_url::", category_url)
        print("index::", index)
        driver = self.get_web_content("%s?&p=%s" % (category_url, index))
        # print(driver.page_source)

        page_object = driver.find_element_by_xpath('//div[@class="page_starlist"]')
        star_pic_items = page_object.find_elements_by_xpath('.//li')

        print("star_pic_items::", len(star_pic_items))

        for star_pic_item in star_pic_items:
            star_img_object = star_pic_item.find_element_by_xpath('.//img')
            star_img_url = star_img_object.get_attribute('src')
            star_name_object = star_pic_item.find_element_by_xpath('.//h3')
            star_name = star_name_object.text

            print(star_name, "---", star_img_url)

        last_page_value = 2
        page_bottom_object = driver.find_element_by_xpath('//div[@class="pages"]')
        last_page_bottom_object = page_bottom_object.find_element_by_xpath('//a[@title="末页"]')
        last_page_bottom_content = last_page_bottom_object.get_attribute('href')
        last_page_content = re.findall(".*?p=(\\d+)", last_page_bottom_content)
        if len(last_page_content) > 0:
            last_page_value = int(last_page_content[0])

        driver.close()

        if index >= last_page_value:
            return
        else:
            index = index + 1
            self.parse(category_url, index)


if __name__ == "__main__":
    request = RequestStarPic()
    request.request()