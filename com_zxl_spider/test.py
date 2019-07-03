#!/usr/bin/python
# coding=UTF-8
import platform
import mysql.connector

if __name__ == "__main__":
    print("test")

    # cnx = mysql.connector.connect(user='zxlworking',
    #                               password='working',
    #                               host='zxltest.zicp.vip',
    #                               port='42278',
    #                               database='mysql')
    # print(cnx)
    # cnx.close()

    sysstr = platform.system()
    print(sysstr)
