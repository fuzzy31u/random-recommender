#!/usr/bin/env python

import cgi
import os
import sys
import MySQLdb
from mako.template import Template
from mako.lookup import TemplateLookup

def main():
    ## 
    print "Content-type: text/html\n"
    totalShownCnt = 60
    totalLikeCnt = 0
    connector = MySQLdb.connect(host="localhost",db="random-recommender",user="root",passwd="")
    connector.autocommit(True)
    cursor = connector.cursor()


    ## request parameters
    form = cgi.FieldStorage()
    # userId
    if form.has_key("userId"):
        userId = form["userId"].value
    # page
    if form.has_key("totalLikeCnt"):
        totalLikeCnt = form["totalLikeCnt"].value


    ## calculate hit_ratio
    ratio = float(totalLikeCnt) / float(totalShownCnt)

    sql3 = "insert into hit_analyzed_ratio (user_id, like_cnt, ratio) values (" + str(userId) + ", " + str(totalLikeCnt) + ", " + str(ratio) + ")"
    cursor.execute(sql3)


    ## data for view
    dirpath = os.path.dirname(os.path.abspath(__file__))
    t = Template(filename = dirpath + "/templates/result.html")
    data = {"userId": userId}
    html = t.render(**data)
    print html


main()
