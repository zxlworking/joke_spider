# /usr/bin/python
# coding=utf-8

class JokeDetailBean:

    def create_joke_detail_bean(self,
                         id,
                         hot_pic_id,
                         article_id,
                         stats_time,
                         content,
                         thumb_img_url):
        bean = {'id': id,
                'hot_pic_id': hot_pic_id,
                'article_id': article_id,
                'stats_time': stats_time,
                'content': content,
                'thumb_img_url': thumb_img_url}
        return bean
