# #windowShopping will take all of the Amazon HTMLs from a data structure and will retrieve all of the used/new prices
import time
from datetime import date
from credentials import *
from amazon.api import AmazonAPI
from fileControls import loadFromFile, saveToFile

#amazon credentials, from credentials file
AMAZON_ACCESS_KEY = amazon_access_key
AMAZON_SECRET_KEY = amazon_secret_key
AMAZON_ASSOC_TAG = amazon_associate_tag

class smartPrice():
    #price object that holds the three different price points for a given book at a given time.
    def __init__ (self, newPrice, usedPrice, tradeIn):
        self.newPrice = newPrice
        self.usedPrice = usedPrice
        self.tradeIn = tradeIn

def getAmazonProductMeta(books,book):
    #finds the prices of a given book in the dict of books, and updates the book with a new dictionary entry, in the format of date:smartPrice.
    amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)

    item_id = books[book]["id"]

    try:
        product = amazon.lookup(ItemId=item_id)        
    except amazon.api.AsinNotFound:
        # log this ASIN
        return None
    except Exception:
    	return None

    newPrice = product._safe_get_element_text("OfferSummary.LowestNewPrice.FormattedPrice")
    usedPrice = product._safe_get_element_text("OfferSummary.LowestUsedPrice.FormattedPrice")
    tradeInPrice = product._safe_get_element_text("ItemAttributes.TradeInValue.FormattedPrice")

    if newPrice or usedPrice or tradeInPrice:
        books[book][str(date.today())] = smartPrice(newPrice, usedPrice, tradeInPrice)

def getPrices(books):
	#iterates through dict of books and updates price
    for book in books:
        getAmazonProductMeta(books, book)
        time.sleep(1)

def main():
    #loads dictionary of books from file, gets prices for all the books, updates each book's dict, and saves books dict back to file
	bookDicts = loadFromFile("addresses.dat")
	getPrices(bookDicts)
	saveToFile(bookDicts, "oldPrices.dat")


if __name__ == "__main__":
	main()