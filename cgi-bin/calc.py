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
    connector = MySQLdb.connect(host="localhost",db="random_recommender",user="root",passwd="")
    connector.autocommit(True)
    cursor = connector.cursor()


    ## request parameters
    form = cgi.FieldStorage()
    # userId
    if form.has_key("userId"):
        userId = form["userId"].value


    ## CALUCULATION 1
    ## calculate hit_ratio
    sql1 = "select count(*) from history where shown_flg = 1 and user_id = " + str(userId)
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    totalShownCnt = result1[0][0]

    sql2 = "select count(*) from result_like where user_id = " + str(userId)
    cursor.execute(sql2)
    result2 = cursor.fetchall()
    totalLikeCnt = result2[0][0]
    ratio = float(totalLikeCnt) / float(totalShownCnt)

    sql3 = "insert into hit_study_ratio (user_id, like_cnt, ratio) values (" + str(userId) + ", " + str(totalLikeCnt) + ", " + str(ratio) + ")"
    cursor.execute(sql3)


    ## CALUCULATION 2
    ## calculate result_ratio
    # get each ratio for calculate result_ratio
    totalGenreRatio = float(0)
    genreRatioDict = {}
    for i in range(6):
        sql4 = "select count(*) from result_like where user_id = " + str(userId) + " and genre_id = " + str(i)
        cursor.execute(sql4)
        result4 = cursor.fetchall()
        genreLikeCnt = result4[0][0]

        sql5 = "select count(*) from history where shown_flg = 1 and user_id = " + str(userId) + " and genre_id = " + str(i)
        cursor.execute(sql5)
        result5 = cursor.fetchall()
        genreShownCnt = result5[0][0]

        if genreShownCnt != 0:
            genreRatio = float(genreLikeCnt) / float(genreShownCnt)
            totalGenreRatio += genreRatio
            genreRatioDict[i] = genreRatio


    # calculate normalisation ratio
    for k, v in genreRatioDict.items():
        genreRatio = float(v)
        normRatio = genreRatio / float(totalGenreRatio)
        sql6 = "insert into result_ratio (genre_id, user_id, ratio, normalisation_ratio) values (" + str(k) + ", " + str(userId) + ", " + str(genreRatio) + ", " + str(normRatio) + ")"
        cursor.execute(sql6)


    ## data for view
    dirpath = os.path.dirname(os.path.abspath(__file__))
    t = Template(filename = dirpath + "/templates/calc.html")
    data = {"userId": userId} 
    html = t.render(**data)
    print html


main()
