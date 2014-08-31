# -*- coding: utf-8 -*- #

import string, re
from bs4 import BeautifulSoup
from NameGenHTTP import Page
import SubnameCollector, NameCollector

def collectNames():
	_nameList = ()

sCollector = SubnameCollector.Collector(entryLimit = 150)
sCollector.collectSubnames()
nCollector = NameCollector.Collector(entryLimit = 750)
nCollector.collectSubnames()
