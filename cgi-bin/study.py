#!/usr/bin/env python

import cgi
import os
import sys
import MySQLdb
from mako.template import Template
from mako.lookup import TemplateLookup

## import my modules
dirpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirpath+"/models")
from image import Image


def main():
    ## 
    print "Content-type: text/html\n"
    page = 1
    connector = MySQLdb.connect(host="localhost",db="random-recommender",user="root",passwd="")
    connector.autocommit(True)
    cursor = connector.cursor()


    ## request parameters
    form = cgi.FieldStorage()
    # userId
    if form.has_key("userId"):
        userId = form["userId"].value

    # page
    if form.has_key("page"):
        page = int(form["page"].value) + 1
    
    # like    
    if form.has_key("like"):
        ## insert result_like data
        for i in form.getlist("like"):
            sql5 = "select genre_id from image where id = " + str(i)
            cursor.execute(sql5)
            result5 = cursor.fetchall()
            genreId = result5[0][0]
            sql4 = "insert into result_like (image_id, user_id, genre_id) values (" + str(i) + " , " + str(userId) + " , " + str(genreId) + ")"
            cursor.execute(sql4)


    ## create data
    list = []
    for i in range(6):
        sql1 = "select * from history where genre_id = " + str(i) + " and user_id = " + str(userId) + " and shown_flg = 0 limit 1"
        cursor.execute(sql1)
        result1 = cursor.fetchall()

        for row in result1:
            imageId = row[0]
            
            sql2 = "select file_name from image where id = " + str(imageId)
            cursor.execute(sql2)
            result2 = cursor.fetchall()
    
            name = result2[0][0]
            
            image = Image(imageId, name, i)
            list.append(image)


    ## update history to be shown
    for image in list:
        sql3 = "update history set shown_flg = 1 where image_id = " + str(image.id) + " and user_id =  " + str(userId)
        cursor.execute(sql3)
        connector.commit()


    ## data for view
    t = Template(filename = dirpath + "/templates/study.html")
 
#    ip = os.environ["REMOTE_ADDR"]
    ip = "54.249.120.194"
    data = {"list": list, "ip": ip, "page": page, "userId": userId}
 
    html = t.render(**data)
    print html

main()
