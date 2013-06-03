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

    ## data for view
    dirpath = os.path.dirname(os.path.abspath(__file__))
    t = Template(filename = dirpath + "/templates/welcome.html")
    data = {}
    html = t.render(**data)
    print html


main()
