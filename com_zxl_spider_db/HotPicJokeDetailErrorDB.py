#!/usr/bin/python
# coding=utf-8

from com_zxl_spider_data.JokeDetailBean import JokeDetailBean
from com_zxl_spider_db.BaseDB import BaseDB


class HotPicJokeDetailErrorDB(BaseDB):

    TABLE_NAME = 'hot_pic_joke_detail_error'

    COLUME_ID = 'id'
    COLUME_HOT_PIC_ID = 'hot_pic_id'
    COLUME_ARTICLE_ID = 'article_id'

    CREATE_TABLE_SQL = (
        "CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " ("
        "  " + COLUME_ID + " bigint(20) NOT NULL AUTO_INCREMENT,"
        "  " + COLUME_HOT_PIC_ID + "  varchar(16),"
        "  " + COLUME_ARTICLE_ID + " text,"
        "  PRIMARY KEY (" + COLUME_ID + ")"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

    INSERT_JOKE_SQL = ("INSERT INTO " + TABLE_NAME + " ("
                                                     + COLUME_HOT_PIC_ID + ","
                                                     + COLUME_ARTICLE_ID
                                                     + ") "
                                                     + "VALUES (%s, %s)")

    DELETE_JOKE_SQL = ("DELETE FROM " + TABLE_NAME)

    DELETE_JOKE_SQL_BY_HOT_PIC_ID = ("DELETE FROM " + TABLE_NAME + " WHERE " + COLUME_HOT_PIC_ID + " = '%s'")

    QUERY_ALL = ("SELECT "
                                + COLUME_ID + ","
                                + COLUME_HOT_PIC_ID + ","
                                + COLUME_ARTICLE_ID
                                + " FROM " + TABLE_NAME)

    QUERY_JOKE_BY_ARTICLE_ID = ("SELECT "
                         + COLUME_ID + ","
                         + COLUME_HOT_PIC_ID + ","
                         + COLUME_ARTICLE_ID
                         + " FROM " + TABLE_NAME
                         + " WHERE " + COLUME_ARTICLE_ID + " = '%s'")

    def create_insert_data(self, joke_detail_bean):
        return (
            joke_detail_bean['hot_pic_id'],
            joke_detail_bean['article_id'],
        )

    def insert_joke_detail(self, joke_detail_bean):
        self.insert(self.INSERT_JOKE_SQL, self.create_insert_data(joke_detail_bean))

    def delete_joke_detail(self):
        self.delete(self.DELETE_JOKE_SQL)

    def delete_joke_detail_by_hot_pic_id(self, hot_pic_id):
        self.delete(self.DELETE_JOKE_SQL_BY_HOT_PIC_ID % (hot_pic_id,))

    def query_all(self):
        cursor = self.query(self.QUERY_ALL)

        jokeDetailBeanList = []
        for (COLUME_ID,
             COLUME_HOT_PIC_ID,
             COLUME_ARTICLE_ID) in cursor:
            jokeDetailBean = JokeDetailBean()
            jokeDetailBean = jokeDetailBean.create_joke_detail_bean(COLUME_ID,
                                                          COLUME_HOT_PIC_ID,
                                                          COLUME_ARTICLE_ID,
                                                          '',
                                                          '',
                                                          '')
            jokeDetailBeanList.append(jokeDetailBean)
        return jokeDetailBeanList

    def query_by_article_id(self, article_id):
        cursor = self.query(self.QUERY_JOKE_BY_ARTICLE_ID % (article_id,))

        for (COLUME_ID,
             COLUME_HOT_PIC_ID,
             COLUME_ARTICLE_ID) in cursor:
            jokeDetailBean = JokeDetailBean()
            return jokeDetailBean.create_joke_detail_bean(COLUME_ID,
                                                     COLUME_HOT_PIC_ID,
                                                     COLUME_ARTICLE_ID,
                                                     '',
                                                     '',
                                                     '')
        return None
