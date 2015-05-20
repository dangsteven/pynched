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

class smartPrice():
    def __init__ (self, newPrice, usedPrice, tradeIn):
        self.newPrice = newPrice
        self.usedPrice = usedPrice
        self.tradeIn = tradeIn


def getAmazonProductMeta(books,book):
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

    newPrice = product._safe_get_element_text("OfferSummary.LowestNewPrice.FormattedPrice")
    usedPrice = product._safe_get_element_text("OfferSummary.LowestUsedPrice.FormattedPrice")
    tradeInPrice = product._safe_get_element_text("ItemAttributes.TradeInValue.FormattedPrice")

    if newPrice or usedPrice or tradeInPrice:
        books[book][str(date.today())] = smartPrice(newPrice, usedPrice, tradeInPrice)
    # return Nonesting.Price.FormattedPrice

def getPrices(books):
	#iterates through document of book urls
    for book in books:
        getAmazonProductMeta(books, book)
        time.sleep(1)

def main():
	# newPrices = {}[href]
	# usedPrices = {}
	# tradeInPrices = {}
	bookDicts = fileControls.loadFromFile("addresses.dat")
	getPrices(bookDicts)
	fileControls.saveToFile(bookDicts, "oldPrices.dat")


if __name__ == '__main__':
	main()