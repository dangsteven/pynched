# #windowShopping will take all of the Amazon HTMLs from a data structure and will retrieve all of the used/new prices

import json
import requests
from bs4 import BeautifulSoup
from amazon.api import AmazonAPI
import time
from credentials import *
import file_controls
import datetime

AMAZON_ACCESS_KEY = amazon_access_key
AMAZON_SECRET_KEY = amazon_secret_key
AMAZON_ASSOC_TAG = amazon_associate_tag

class smart_price():
    def __init__ (self, new_price, used_price, trade_in):
        self.new_price = new_price
        self.used_price = used_price
        self.trade_in = trade_in


def get_amazon_product_meta(book):
    # the input URL is always of amazon
    amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

    # item_id = get_amazon_item_id(url)
    # if not item_id:
    #     return None

    item_id = book.id

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

    book[datetime.date.time()] = smart_price(new_price, used_price, trade_in)
    # return Nonesting.Price.FormattedPrice

def get_prices(books):
	#iterates through document of book urls
	for book in books:
		get_amazon_product_meta(book)
		time.sleep(1)
		print(url)
		print("\t" + str(price))

def main():
	# newPrices = {}[href]
	# usedPrices = {}
	# tradeInPrices = {}
	book_dicts = file_controls.load_from_file("addresses.dat")
	get_prices(book_dicts)
	# save_to_file(newPrices, "newPrices.dat")
	# save_to_file(usedPrices, "usedPrices.dat")
	# save_to_file(tradeInPrices, "tradeInPrices.dat")

if __name__ == '__main__':
	main()