# #windowShopping will take all of the Amazon HTMLs from a data structure and will retrieve all of the used/new prices
import requests
from bs4 import BeautifulSoup
from amazon.api import AmazonAPI
import time
from credentials import *
import fileControls
from datetime import date

AMAZON_ACCESS_KEY = amazon_access_key
AMAZON_SECRET_KEY = amazon_secret_key
AMAZON_ASSOC_TAG = amazon_associate_tag

class smart_price():
    def __init__ (self, new_price, used_price, trade_in):
        self.new_price = new_price
        self.used_price = used_price
        self.trade_in = trade_in


def get_amazon_product_meta(books,book):
    # the input URL is always of amazon
    amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

    # item_id = get_amazon_item_id(url)
    # if not item_id:
    #     return None
    item_id = books[book]["id"]

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
        books[book][str(date.today())] = smart_price(new_price, used_price, trade_in_price)
    # return Nonesting.Price.FormattedPrice

def get_prices(books):
	#iterates through document of book urls
    for book in books:
        get_amazon_product_meta(books, book)
        time.sleep(1)

def main():
	# newPrices = {}[href]
	# usedPrices = {}
	# tradeInPrices = {}
	book_dicts = fileControls.load_from_file("addresses.dat")
	get_prices(book_dicts)
	fileControls.save_to_file(book_dicts, "oldPrices.dat")


if __name__ == '__main__':
	main()