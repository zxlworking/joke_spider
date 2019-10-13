#!/usr/bin/python
# coding=utf-8
import mysql
from mysql.connector import errorcode

from com_zxl_spider_data.MaoYanBean import MaoYanBean
from com_zxl_spider_db.BaseDB import BaseDB


class MaoYanDB(BaseDB):

    TABLE_NAME = 'mao_yan_now'

    COLUME_ID = 'id'
    COLUME_MOVIE_ID = 'movie_id'
    COLUME_MOVIE_TITLE = 'movie_title'
    COLUME_MOVIE_POSTER_URL = 'movie_poster_url'
    COLUME_MOVIE_DETAIL_URL = 'movie_detail_url'
    COLUME_MOVIE_TYPE = 'movie_type'

    CREATE_TABLE_SQL = (
        "CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " ("
        "  " + COLUME_ID + " bigint(20) NOT NULL AUTO_INCREMENT,"
        "  " + COLUME_MOVIE_ID + "  text,"
        "  " + COLUME_MOVIE_TITLE + " text,"
        "  " + COLUME_MOVIE_POSTER_URL + " text,"
        "  " + COLUME_MOVIE_DETAIL_URL + " text,"
        "  " + COLUME_MOVIE_TYPE + " text,"
        "  PRIMARY KEY (" + COLUME_ID + ")"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci")

    INSERT_SQL = ("INSERT INTO " + TABLE_NAME + " ("
                                                     + COLUME_MOVIE_ID + ","
                                                     + COLUME_MOVIE_TITLE + ","
                                                     + COLUME_MOVIE_POSTER_URL + ","
                                                     + COLUME_MOVIE_DETAIL_URL + ","
                                                     + COLUME_MOVIE_TYPE
                                                     + ") "
                                                     + "VALUES (%s, %s, %s, %s, %s)")

    DELETE_SQL = ("DELETE FROM " + TABLE_NAME)

    QUERY_BY_MOVIE_ID = ("SELECT "
                         + COLUME_ID + ","
                         + COLUME_MOVIE_ID + ","
                         + COLUME_MOVIE_TITLE + ","
                         + COLUME_MOVIE_POSTER_URL + ","
                         + COLUME_MOVIE_DETAIL_URL + ","
                         + COLUME_MOVIE_TYPE
                         + " FROM " + TABLE_NAME
                         + " WHERE " + COLUME_MOVIE_ID + " = '%s'")

    def create_insert_data(self, mao_yan_bean):
        return (
            mao_yan_bean['movie_id'],
            mao_yan_bean['movie_title'],
            mao_yan_bean['movie_poster_url'],
            mao_yan_bean['movie_detail_url'],
            mao_yan_bean['movie_type']
        )

    def insert_bean(self, mao_yan_bean):
        self.insert(self.INSERT_SQL, self.create_insert_data(mao_yan_bean))

    def delete_all(self):
        self.delete(self.DELETE_SQL)

    def query_by_movie_id(self, movie_id):
        cursor = self.query(self.QUERY_BY_MOVIE_ID % (movie_id,))

        for (COLUME_ID,
             COLUME_MOVIE_ID,
             COLUME_MOVIE_TITLE,
             COLUME_MOVIE_POSTER_URL,
             COLUME_MOVIE_DETAIL_URL,
             COLUME_MOVIE_TYPE) in cursor:
            mao_yan_bean = MaoYanBean()
            return mao_yan_bean.create_bean(COLUME_ID,
                                             COLUME_MOVIE_ID,
                                             COLUME_MOVIE_TITLE,
                                             COLUME_MOVIE_POSTER_URL,
                                             COLUME_MOVIE_DETAIL_URL,
                                             COLUME_MOVIE_TYPE)
        return None
