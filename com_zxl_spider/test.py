#!/usr/bin/python
# coding=UTF-8
import sys
import mysql.connector

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    print("test")

    # cnx = mysql.connector.connect(user='root',
    #                               password='Aa123456',
    #                               host='127.0.0.1',
    #                               database='mysql')

    cnx = mysql.connector.connect(user='zxlworking',
                                  password='working',
                                  host='zxltest.zicp.vip',
                                  port='42278',
                                  database='mysql')

    cnx.close()
