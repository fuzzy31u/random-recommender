#!/usr/bin/env python

import cgi
import os
import sys
import MySQLdb

def main():

    ## import my modules
    dirpath = os.path.dirname(os.path.abspath(__file__))

    ## 
    print "Content-type: text/html\n"
    connector = MySQLdb.connect(host="localhost",db="research",user="root",passwd="")
    connector.autocommit(True)
    cursor = connector.cursor()


    ## 
    sql1 = "select id from genre"
    cursor.execute(sql1)
    result1 = cursor.fetchall()


    ## get files from image directory
    for row in result1:
        list = os.listdir(dirpath + "/cgi-bin/images/" + str(row[0]))

        for f in list:
            sql2 = "insert into image (genre_id, file_name) values (" + str(row[0]) + ", '" + f + "')"
            print sql2
            cursor.execute(sql2)



main()
