# -*- coding: utf-8 -*- #

import string, re
from bs4 import BeautifulSoup
from NameGenHTTP import Page

class Collector:
	def __init__(self, entryLimit = -1):
		self._nameList = ()
		self.rootURL = "http://www.genealogie.com"
		self.baseURL = "%s/nom-de-famille/classement-general-0" % self.rootURL
		self.lastPageId = -1
		self.entryLimit = entryLimit

	def collectSubnames(self):
		self._nameList = ()

		self.getPageAndStoreResults(1)

		print "Total collected names: %d" % len(self._nameList)

	def getPageAndStoreResults(self, pageId, getRange=True):
		htmlPage = Page.get("%s-%d" % (self.baseURL, pageId))

		pageSoup = BeautifulSoup(htmlPage)

		# on genealogie.com we need to find how many pages of names we have
		if self.lastPageId == -1:
			paginationSoup = BeautifulSoup("%s" % pageSoup.body.find_all("div", {"class": "pageNo"})).find_all("a")
			self.lastPageId = int(re.sub("\n","",re.sub(" ","",paginationSoup[-1].string)))

		nameSoup = pageSoup.find_all("label", {"class":"nameValue"})
		for entry in nameSoup:
			# If we are on the entry limit, stop process
			if self.entryLimit > 0 and len(self._nameList) >= self.entryLimit:
				break

			# We get the first <a> element, it's the name label
			entrySoup = BeautifulSoup("%s" %
				BeautifulSoup("%s" % entry).find_all("a")[-1]
			)
			for entry2 in entrySoup:

				tmpName = "%s" % re.sub("\n","", re.sub(" ","",entry2.string))
				if tmpName not in self._nameList:
					self._nameList += (tmpName,)

		print "Current ID %d - Total Collected Names %d" % (pageId, len(self._nameList))

		# If page is page 1, then we loop the results
		if getRange == True:
			for pId in range(2, self.lastPageId+1):
				# If we are on the entry limit, stop process
				if self.entryLimit > 0 and len(self._nameList) >= self.entryLimit:
					break

				self.getPageAndStoreResults(pId, False)





