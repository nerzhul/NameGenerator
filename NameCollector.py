# -*- coding: utf-8 -*- #

"""
* Copyright (c) 2014, Loïc BLOT <http://www.unix-experience.fr>
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*
* 1. Redistributions of source code must retain the above copyright notice, this
*    list of conditions and the following disclaimer.
* 2. Redistributions in binary form must reproduce the above copyright notice,
*    this list of conditions and the following disclaimer in the documentation
*    and/or other materials provided with the distribution.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
* ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
* ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*
* The views and conclusions contained in the software and documentation are those
* of the authors and should not be interpreted as representing official policies,
* either expressed or implied, of the FreeBSD Project.
"""

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





