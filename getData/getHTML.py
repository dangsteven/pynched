# getHTML.py is part of the Pynched package. getHTML is a web crawler designed specifically to browse Amazon's
# textbook selection and will retrieve the HTMLs of the top books from each refined category and discipline.

import sys
import requests
from bs4 import BeautifulSoup
import json
import file_controls
import re

asin_regex = r'/([A-Z0-9]{10})'
isbn_regex = r'/([0-9]{10})'

def get_amazon_item_id(url):
    # return either ASIN or ISBN
    asin_search = re.search(asin_regex, url)
    isbn_search = re.search(isbn_regex, url)
    if asin_search:
        return asin_search.group(1)
    elif isbn_search:
        return isbn_search.group(1)
    else: #should log this url
        return None

def getInfo(url, List):
	source_code = requests.get(url)
	plain_text = source_code.text 
	soup = BeautifulSoup(plain_text)

	for addresses in soup.find_all('li', {'class','s-result-item'}):
		for a in addresses.find_all(title=True):
			if a.text and a.get('href') not in List:
				List[a.text] = {"href":a.get('href'), "keywords":[],
				"id":get_amazon_item_id(a.get('href'))}
	print(List)
	print('\n')

def getPagesFromRefinementLinks(url, List):
	source_code = requests.get(url)
	plain_text = source_code.text 
	soup = BeautifulSoup(plain_text)
	c = 0
	for link in soup.find_all('span', {'class', 'refinementLink'}):
		c += 1
		href = link.parent.get('href')
		print(link.string)
		getPagesFromRefinementLinks(href, List)
	if(c == 0):
		getInfo(url, List)
	return

def getHTMLs(List): #will only run once. ever.
	#url = "http://www.amazon.com/New-Used-Textbooks-Books"\
	#"/b/ref=bhp_brws_txt_stor?ie=UTF8&node=465600&pf_rd_m"\
	#"=ATVPDKIKX0DER&pf_rd_s=merchandised-search-leftnav&pf_rd_r"\
	#"=08W1VWTWWBKQKYRF42A2&pf_rd_t=101&pf_rd_p=2079831362&pf_rd_i=283155"
	#tinier sample size:
	url = "http://www.amazon.com/s/ref=lp_465600_nr_n_2?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%212349030011%2Cn%3A465600%2Cn%3A468204&bbn=465600&ie=UTF8&qid=1431228922&rnid=465600"
	getPagesFromRefinementLinks(url,List)

def main():
	book_dicts = {}
	getHTMLs(book_dicts)
	file_controls.save_to_file(book_dicts, "addresses.dat")

if __name__ == '__main__':
	main()