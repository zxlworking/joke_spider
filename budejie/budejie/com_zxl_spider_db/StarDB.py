#!/usr/bin/python
# coding=utf-8
import mysql
from mysql.connector import errorcode

from com_zxl_spider_data.StarInfoBean import StarInfoBean
from com_zxl_spider_db.BaseDB import BaseDB


class StarDB(BaseDB):

    TABLE_NAME = 'star_info'

    COLUME_ID = 'id'
    COLUME_STAR_NAME = 'star_name'
    COLUME_STAR_IMG_URL = 'star_img_url'
    COLUME_STAR_DETAIL_URL = 'star_detail_url'
    COLUME_FACE_ID = 'face_id'

    CREATE_TABLE_SQL = (
        "CREATE TABLE IF NOT EXISTS " + TABLE_NAME + " ("
        "  " + COLUME_ID + " bigint(20) NOT NULL AUTO_INCREMENT,"
        "  " + COLUME_STAR_NAME + "  text,"
        "  " + COLUME_STAR_IMG_URL + " text,"
        "  " + COLUME_STAR_DETAIL_URL + " text,"
        "  " + COLUME_FACE_ID + " text,"
        "  PRIMARY KEY (" + COLUME_ID + ")"
        ") ENGINE=InnoDB")

    INSERT_STAR_INFO_SQL = ("INSERT INTO " + TABLE_NAME + " ("
                       + COLUME_STAR_NAME + ","
                       + COLUME_STAR_IMG_URL + ","
                       + COLUME_STAR_DETAIL_URL + ","
                       + COLUME_FACE_ID
                       + ") "
                       + "VALUES (%s, %s, %s, %s)")

    QUERY_STAR_INFO_BY_STAR_NAME = ("SELECT "
                         + COLUME_ID + ","
                         + COLUME_STAR_NAME + ","
                         + COLUME_STAR_IMG_URL + ","
                         + COLUME_STAR_DETAIL_URL + ","
                         + COLUME_FACE_ID
                         + " FROM " + TABLE_NAME
                         + " WHERE " + COLUME_STAR_NAME + " = '%s'")

    QUERY_STAR_INFO_BY_STAR_ID = ("SELECT "
                                   + COLUME_ID + ","
                                   + COLUME_STAR_NAME + ","
                                   + COLUME_STAR_IMG_URL + ","
                                   + COLUME_STAR_DETAIL_URL + ","
                                   + COLUME_FACE_ID
                                   + " FROM " + TABLE_NAME
                                   + " WHERE " + COLUME_ID + " = '%s'")

    QUERY_ALL_STAR_INFO = ("SELECT "
                                   + COLUME_ID + ","
                                   + COLUME_STAR_NAME + ","
                                   + COLUME_STAR_IMG_URL + ","
                                   + COLUME_STAR_DETAIL_URL + ","
                                   + COLUME_FACE_ID
                                   + " FROM " + TABLE_NAME
                                   + " LIMIT %s,%s")

    QUERY_ALL_STAR_INFO_COUNT = ("SELECT "
                           + " count(*) "
                           + " FROM " + TABLE_NAME)

    UPDATE_STAR_FACE_ID = ("UPDATE " + TABLE_NAME
                                 + " SET face_id = '%s' "
                                 + " WHERE id = %d ")

    def create_insert_data(self, star_info_bean):
        return (
            star_info_bean['id'],
            star_info_bean['star_name'],
            star_info_bean['star_img_url'],
            star_info_bean['star_detail_url'],
            star_info_bean['face_id'],
        )

    def insert_star_info(self, star_info_bean):
        self.insert(self.INSERT_STAR_INFO_SQL, (
            star_info_bean['star_name'],
            star_info_bean['star_img_url'],
            star_info_bean['star_detail_url'],
            star_info_bean['face_id'],
        ))

    def query_by_star_name(self, star_name):
        cursor = self.query(self.QUERY_STAR_INFO_BY_STAR_NAME % (star_name,))

        for (COLUME_ID,
             COLUME_STAR_NAME,
             COLUME_STAR_IMG_URL,
             COLUME_STAR_DETAIL_URL,
             COLUME_FACE_ID) in cursor:
            star_info_bean = StarInfoBean()
            return star_info_bean.create_star_info_bean(COLUME_ID,
                                                        COLUME_STAR_NAME,
                                                        COLUME_STAR_IMG_URL,
                                                        COLUME_STAR_DETAIL_URL,
                                                        COLUME_FACE_ID)
        return None

    def query_by_star_id(self, star_id):
        cursor = self.query(self.QUERY_STAR_INFO_BY_STAR_ID % (star_id,))

        for (COLUME_ID,
             COLUME_STAR_NAME,
             COLUME_STAR_IMG_URL,
             COLUME_STAR_DETAIL_URL,
             COLUME_FACE_ID) in cursor:
            print("query_by_star_id", COLUME_ID,
                  COLUME_STAR_NAME,
                  COLUME_STAR_IMG_URL,
                  COLUME_STAR_DETAIL_URL,
                  COLUME_FACE_ID)

            star_info_bean = StarInfoBean()
            return star_info_bean.create_star_info_bean(COLUME_ID,
                                                        COLUME_STAR_NAME,
                                                        COLUME_STAR_IMG_URL,
                                                        COLUME_STAR_DETAIL_URL,
                                                        COLUME_FACE_ID)
        return None

    def query_all_star_info_count(self):
        cursor = self.query(self.QUERY_ALL_STAR_INFO_COUNT)

        for (count) in cursor:
            return count
        return 0

    def query_all_star_info(self, start_index, end_index):
        cursor = self.query(self.QUERY_ALL_STAR_INFO % (start_index, end_index))

        star_info_bean_list = []
        for (COLUME_ID,
             COLUME_STAR_NAME,
             COLUME_STAR_IMG_URL,
             COLUME_STAR_DETAIL_URL,
             COLUME_FACE_ID) in cursor:
            star_info_bean = StarInfoBean()
            star_info_bean = star_info_bean.create_star_info_bean(COLUME_ID,
                                                                  COLUME_STAR_NAME,
                                                                  COLUME_STAR_IMG_URL,
                                                                  COLUME_STAR_DETAIL_URL,
                                                                  COLUME_FACE_ID)
            star_info_bean_list.append(star_info_bean)
        return star_info_bean_list

    def update_star_face_id(self, star_info_bean):
        # self.query_by_star_id(star_info_bean['id'])
        self.update(self.UPDATE_STAR_FACE_ID % (star_info_bean['face_id'], int(star_info_bean['id'])))
        # self.query_by_star_id(star_info_bean['id'])
