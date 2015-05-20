# getHTML.py is part of the Pynched package. getHTML is a web crawler designed specifically to browse Amazon's
# textbook selection and will retrieve the HTMLs of the top books from each refinement category and discipline.

import sys
import requests
from bs4 import BeautifulSoup
import json
import fileControls
import re

#regex comands for finding ASIN or ISBN
asin_regex = r"/([A-Z0-9]{10})"
isbn_regex = r"/([0-9]{10})"

def getAmazonItemId(url):
    # return either ASIN or ISBN
    asin_search = re.search(asin_regex, url)
    isbn_search = re.search(isbn_regex, url)
    if asin_search:
        return asin_search.group(1)
    elif isbn_search:
        return isbn_search.group(1)
    else: #should log this url
        return None

def getKeywords(title, href):
	#finds the keywords associated with a book, either from the title or its hierarchy.
	words = []
	uselessWords = ("and", "in", "or", "the", "of", "for", "a", "an", "to", "from", "with", "on", "in", "guide", "books")
	source_code = requests.get(href)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text)
	#Now that we have the soup, find the keywords
	for span in soup.find_all("span", {"class", "zg_hrsr_ladder"}):
		for phrases in span.find_all("a"):
			for word in phrases.text.split():
				if word not in uselessWords and word not in words:
					words.append(word)
	for word in title.split():
		if word not in uselessWords and word not in words:
			words.append(word)
	return words

def getInfo(url, List):
	#for all the results on a page, create a dict describing each book, containing the book's url, any keywords, and its id (ASIN or ISBN).
	source_code = requests.get(url)
	plain_text = source_code.text 
	soup = BeautifulSoup(plain_text)

	for addresses in soup.find_all("li", {"class","s-result-item"}):
		for a in addresses.find_all(title=True):
			if a.text and a.get("href") not in List:
				List[a.text] = {"href":a.get("href"), "keywords":getKeywords(a.text, a.get("href")),
				"id":getAmazonItemId(a.get("href"))}

def getPagesFromRefinementLinks(url, List):
	#given a page with results and refinement links, run this code recursively on all the refinement links, and get the info for all the results.
	source_code = requests.get(url)
	plain_text = source_code.text 
	soup = BeautifulSoup(plain_text)
	c = 0
	getInfo(url, List)
	print(List)
	for link in soup.find_all("span", {"class", "refinementLink"}):
		c += 1
		href = link.parent.get("href")
		getPagesFromRefinementLinks(href, List)

def getHTMLs(List): #will only run once. ever.
	#given a base url, get all the pages from the refinement links on the page.
	# url = "http://www.amazon.com/New-Used-Textbooks-Books"\
	# "/b/ref=bhp_brws_txt_stor?ie=UTF8&node=465600&pf_rd_m"\
	# "=ATVPDKIKX0DER&pf_rd_s=merchandised-search-leftnav&pf_rd_r"\
	# "=08W1VWTWWBKQKYRF42A2&pf_rd_t=101&pf_rd_p=2079831362&pf_rd_i=283155"
	#tinier sample size:
	url = "http://www.amazon.com/s/ref=lp_465600_nr_n_2?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%212349030011%2Cn%3A465600%2Cn%3A468204&bbn=465600&ie=UTF8&qid=1431228922&rnid=465600"
	getPagesFromRefinementLinks(url,List)

def main():
	#creation of bookDicts, a dictionary of textbooks found, gets the HTMLs and other appropriate data for the books, and saves the resulting dict to a file.
	bookDicts = {}
	getHTMLs(bookDicts)
	fileControls.saveToFile(bookDicts, "addresses.dat")

if __name__ == "__main__":
	main()