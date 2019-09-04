#!/usr/bin/python
# coding=utf-8
import mysql
from mysql.connector import errorcode

from com_zxl_spider_data.JokeBean import JokeBean
from com_zxl_spider_db.BaseDB import BaseDB


class TxtJokeDB(BaseDB):

    TABLE_NAME = 'txt_joke'

    COLUME_ID = 'id'
    COLUME_AUTHOR_NICK_NAME = 'author_nick_name'
    COLUME_AUTHOR_GENDER = 'author_gender'
    COLUME_AUTHOR_AGE = 'author_age'
    COLUME_AUTHOR_IMG_URL = 'author_img_url'
    COLUME_CONTENT = 'content'
    COLUME_THUMB_IMG_URL = 'thumb_img_url'
    COLUME__STATS_VOTE_CONTENT = 'stats_vote_content'
    COLUME_STATS_COMMENT_CONTENT = 'stats_comment_content'
    COLUME_STATS_COMMENT_DETAIL_URL = 'stats_comment_detail_url'
    COLUME_MD5 = 'md5'

    CREATE_TABLE_SQL = (
        "CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " ("
        "  " + COLUME_ID + " bigint(20) NOT NULL AUTO_INCREMENT,"
        "  " + COLUME_AUTHOR_NICK_NAME + "  varchar(16),"
        "  " + COLUME_AUTHOR_GENDER + " text,"
        "  " + COLUME_AUTHOR_AGE + " text,"
        "  " + COLUME_AUTHOR_IMG_URL + " text,"
        "  " + COLUME_CONTENT + " text,"
        "  " + COLUME_THUMB_IMG_URL + " text,"
        "  " + COLUME__STATS_VOTE_CONTENT + " text,"
        "  " + COLUME_STATS_COMMENT_CONTENT + " text,"
        "  " + COLUME_STATS_COMMENT_DETAIL_URL + " text,"
        "  " + COLUME_MD5 + " text,"
        "  PRIMARY KEY (" + COLUME_ID + ")"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

    INSERT_JOKE_SQL = ("INSERT INTO " + TABLE_NAME + " ("
                                                     + COLUME_AUTHOR_NICK_NAME + ","
                                                     + COLUME_AUTHOR_GENDER + ","
                                                     + COLUME_AUTHOR_AGE + ","
                                                     + COLUME_AUTHOR_IMG_URL + ","
                                                     + COLUME_CONTENT + ","
                                                     + COLUME_THUMB_IMG_URL + ","
                                                     + COLUME__STATS_VOTE_CONTENT + ","
                                                     + COLUME_STATS_COMMENT_CONTENT + ","
                                                     + COLUME_STATS_COMMENT_DETAIL_URL + ","
                                                     + COLUME_MD5
                                                     + ") "
                                                     + "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    DELETE_JOKE_SQL = ("DELETE FROM " + TABLE_NAME)

    QUERY_JOKE_BY_MD5 = ("SELECT "
                         + COLUME_ID + ","
                         + COLUME_AUTHOR_NICK_NAME + ","
                         + COLUME_AUTHOR_GENDER + ","
                         + COLUME_AUTHOR_AGE + ","
                         + COLUME_AUTHOR_IMG_URL + ","
                         + COLUME_CONTENT + ","
                         + COLUME_THUMB_IMG_URL + ","
                         + COLUME__STATS_VOTE_CONTENT + ","
                         + COLUME_STATS_COMMENT_CONTENT + ","
                         + COLUME_STATS_COMMENT_DETAIL_URL + ","
                         + COLUME_MD5
                         + " FROM " + TABLE_NAME
                         + " WHERE " + COLUME_MD5 + " = '%s'")

    def create_insert_data(self, joke_bean):
        return (
            joke_bean['author_nick_name'],
            joke_bean['author_gender'],
            joke_bean['author_age'],
            joke_bean['author_img_url'],
            joke_bean['content'],
            joke_bean['thumb_img_url'],
            joke_bean['stats_vote_content'],
            joke_bean['stats_comment_content'],
            joke_bean['stats_comment_detail_url'],
            joke_bean['md5']
        )

    def insert_joke(self, joke_bean):
        self.insert(self.INSERT_JOKE_SQL, self.create_insert_data(joke_bean))

    def delete_joke(self):
        self.delete(self.DELETE_JOKE_SQL)

    def query_by_md5(self, md5):
        cursor = self.query(self.QUERY_JOKE_BY_MD5 % (md5,))

        for (COLUME_ID,
             COLUME_AUTHOR_NICK_NAME,
             COLUME_AUTHOR_GENDER,
             COLUME_AUTHOR_AGE,
             COLUME_AUTHOR_IMG_URL,
             COLUME_CONTENT,
             COLUME_THUMB_IMG_URL,
             COLUME__STATS_VOTE_CONTENT,
             COLUME_STATS_COMMENT_CONTENT,
             COLUME_STATS_COMMENT_DETAIL_URL,
             COLUME_MD5) in cursor:
            jokeBean = JokeBean()
            return jokeBean.create_joke_bean(COLUME_ID,
                                             COLUME_AUTHOR_NICK_NAME,
                                             COLUME_AUTHOR_GENDER,
                                             COLUME_AUTHOR_AGE,
                                             COLUME_AUTHOR_IMG_URL,
                                             COLUME_CONTENT,
                                             COLUME_THUMB_IMG_URL,
                                             COLUME__STATS_VOTE_CONTENT,
                                             COLUME_STATS_COMMENT_CONTENT,
                                             COLUME_STATS_COMMENT_DETAIL_URL,
                                             COLUME_MD5)
        return None
