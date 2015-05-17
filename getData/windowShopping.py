# #windowShopping will take all of the Amazon HTMLs from a data structure and will retrieve all of the used/new prices
import re
import json
import requests
from bs4 import BeautifulSoup
from amazon.api import AmazonAPI
import time

AMAZON_ACCESS_KEY = 'AKIAIZS67S2JYM7RGUAA'
AMAZON_SECRET_KEY = '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'
AMAZON_ASSOC_TAG = 'sddang'

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
    else:
        # log this URL
        return None

def get_amazon_product_meta(url):
    # the input URL is always of amazon
    amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

    item_id = get_amazon_item_id(url)
    if not item_id:
        return None

    try:
        product = amazon.lookup(ItemId=item_id)        
    except amazon.api.AsinNotFound:
        # log this ASIN
        return None
    except Exception:
    	return None


    # product.price_and_currency returns in the form (price, currency)
	# product_price = product.price_and_currency[0]

    new_price = product._safe_get_element_text("OfferSummary.LowestNewPrice.FormattedPrice")
    used_price = product._safe_get_element_text("OfferSummary.LowestUsedPrice.FormattedPrice")
    trade_in_price = product._safe_get_element_text("ItemAttributes.TradeInValue.FormattedPrice")

    if new_price or used_price or trade_in_price:
        return new_price, used_price, trade_in_price

    return Nonesting.Price.FormattedPrice

def unpickle(fileName):
	f = open(fileName, 'r')
	HTML_Dict = json.load(f)
	print(fileName)
	f.close()

	return HTML_Dict

def pickle(structure,fileName):
	f = open(fileName, 'w' )
	json.dump(structure,f)
	f.close()

def get_prices(urls,newPricesDict, usedPricesDict, tradeInDict):
	#iterates through document of book urls
	for url in urls:
		price = get_amazon_product_meta(urls[url])
		newPricesDict[url] = price[0]
		usedPricesDict[url] = price[1]
		tradeInDict[url] = price[2]
		time.sleep(1)
		print(url)
		print("\t" + str(price))


def main():
	newPrices = {}
	usedPrices = {}
	tradeInPrices = {}
	urlDict = unpickle('addresses.dat')
	get_prices(urlDict, newPrices, usedPrices, tradeInPrices)
	pickle(newPrices, "newPrices.dat")
	pickle(usedPrices, "usedPrices.dat")
	pickle(tradeInPrices, "tradeInPrices.dat")

if __name__ == '__main__':
	main()