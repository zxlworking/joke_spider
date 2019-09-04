# /usr/bin/python
# coding=utf-8

class JokeBean:

    def create_joke_bean(self,
                         id,
                         author_nick_name,
                         author_gender,
                         author_age,
                         author_img_url,
                         content,
                         thumb_img_url,
                         stats_vote_content,
                         stats_comment_content,
                         stats_comment_detail_url,
                         md5):
        bean = {'id': id,
                'author_nick_name': author_nick_name,
                'author_gender': author_gender,
                'author_age': author_age,
                'author_img_url': author_img_url,
                'content': content,
                'thumb_img_url': thumb_img_url,
                'stats_vote_content': stats_vote_content,
                'stats_comment_content': stats_comment_content,
                'stats_comment_detail_url': stats_comment_detail_url,
                'md5': md5}
        return bean
