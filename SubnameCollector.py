# -*- coding: utf-8 -*- #

import string, re
from bs4 import BeautifulSoup
from NameGenHTTP import Page

class Collector:
	def __init__(self, entryLimit = -1):
		self._subnameList = ()
		self.rootURL = "http://nominis.cef.fr"
		self.baseURL = "%s/contenus/prenom/alphabetique" % self.rootURL
		self.alphabet = string.ascii_uppercase
		self.entryLimit = entryLimit

	def collectSubnames(self):
		self._subnameList = ()

		# For each letter collect all subnames
		for letter in self.alphabet:
			# If we are on the entry limit, stop process
			if self.entryLimit > 0 and len(self._subnameList) >= self.entryLimit:
				break

			self.getPageAndStoreResults(letter, "%s/%s.html" % (self.baseURL, letter))

		print "Total collected subnames: %d" % len(self._subnameList)

	def getPageAndStoreResults(self, letter, url, otherPages = True):
		htmlPage = Page.get(url)

		pageSoup = BeautifulSoup(htmlPage)

		# First, get all subnames in this page
		subnameSoup = BeautifulSoup("%s" % pageSoup.body.find_all(self.getsubnameDiv)).find_all("a")

		# And bufferize them all
		for entry in subnameSoup:
			# If we are on the entry limit, stop process
			if self.entryLimit > 0 and len(self._subnameList) >= self.entryLimit:
				break

			subname = entry.string
			if subname not in self._subnameList:
				self._subnameList += (subname, )

		print "Collected %d entries for letter %s - Total collected: %d" % (len(subnameSoup), letter, len(self._subnameList))

		if otherPages == True:
			# Second, seek other pages
			otherPagesSoup = BeautifulSoup("%s" %
				BeautifulSoup("%s" %
					pageSoup.find_all("div", {"class":"span11"})
				).find_all(self.getsubnamePaginationDiv)
			).find_all("a")

			for entry in otherPagesSoup:
				# If we are on the entry limit, stop process
				if self.entryLimit > 0 and len(self._subnameList) >= self.entryLimit:
					break

				if not re.search("%s-1.html" % letter, entry["href"]):
					self.getPageAndStoreResults(letter, "%s/%s" % (self.rootURL, entry["href"]), False)

	def getsubnameDiv(self, tag):
		return (
			tag.name == 'div'
			and 'well' in tag.get('class')
			and len(tag.get('class')) == 1
		)

	def getsubnamePaginationDiv(self, tag):
		return (
			tag.name == 'div'
			and 'pagination' in tag.get('class')
			and len(tag.get('class')) == 2
		)


