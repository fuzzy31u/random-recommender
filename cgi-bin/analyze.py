#!/usr/bin/env python

import cgi
import os
import sys
import random
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
    trialPageCnt = 10
    dispCntPerPage = 6
    connector = MySQLdb.connect(host="localhost",db="random_recommender",user="root",passwd="")
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
    if form.has_key("totalLikeCnt"):
        totalLikeCnt = form["totalLikeCnt"].value
        if form.has_key("like"):
            likeCnt = form.getlist("like")
            if len(likeCnt) > 0:
                lc = len(likeCnt)
                totalLikeCnt = lc + int(totalLikeCnt)
    else:
        totalLikeCnt = 0

    ## create total image data
    if page == 1:
        list = []

        # create ratio image list
        for i in range(dispCntPerPage):
            sql3 = "select * from history where shown_flg = 0 and user_id = " + str(userId) + " and genre_id = " + str(i) + " limit 10"
            cursor.execute(sql3)
            result3 = cursor.fetchall()
            for row in result3:
                imageId = row[0]

                sql4 = "select file_name from image where id = " + str(imageId)
                cursor.execute(sql4)
                result4 = cursor.fetchall()
    
                name = result4[0][0]
           
                image = Image(imageId, name, k)
                list.append(image)
    
        random.shuffle(list)


        ## save list data temporary
        for l in list:
            sql5 = "insert into temp_analyzed_image values (" + str(l.id) + ", " + str(userId) + ", " + str(l.genreId) + ", '" + l.name + "')"
            cursor.execute(sql5)



    ## create display data
    dispList = []    
    offset = dispCntPerPage * (page - 1)
    sql6 = "select * from temp_analyzed_image where user_id = " + str(userId) + " limit " + str(dispCntPerPage) + " offset " + str(offset)
    cursor.execute(sql6)
    result6 = cursor.fetchall()
    for row in result6:
        image = Image(row[0], row[3], row[2])
        dispList.append(image)


    ## data for view
    t = Template(filename = dirpath + "/templates/analyze.html")

#    ip = os.environ["REMOTE_ADDR"]
    ip = "localhost"
    data = {"ip": ip, "page": page, "totalLikeCnt": totalLikeCnt, "dispList": dispList, "userId": userId}

    html = t.render(**data)
    print html

main()
