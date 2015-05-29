import json
from datetime import date, timedelta as td
from fileControls import loadFromFile, saveToFile

def findAverage(books,priceType):
	priceSet = {}

	d1 = date(2015, 5, 23)
	d2 = date.today()

	delta = d2 - d1

	for i in range(delta.days + 1):
		day = d1 + td(days=i)

		todaysAverage = 0
		bookCount = 0
		for book in books:
			try:
				price = float(books[book][str(day)][str(priceType)][1:])
				bookCount = bookCount + 1
				todaysAverage = todaysAverage + price
			except:
				print("")

		averageToday = float(todaysAverage)/float(bookCount)
		priceSet[str(day)] = averageToday

	return(priceSet)


def main():
	library = loadFromFile("pricesBackup.dat")
	#get newPrices
	newAverages = findAverage(library,"newPrice")
	saveToFile(newAverages, "newAverages.dat")
	#get usedPrices
	oldAverages = findAverage(library,"usedPrice")
	saveToFile(oldAverages, "oldAverages.dat")
	#get tradeInPrices
	tradeInAverages = findAverage(library,"tradeIn")
	saveToFile(tradeInAverages, "tradeInAverages.dat")


if __name__ == '__main__':
	main()