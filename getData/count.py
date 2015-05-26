import json
from fileControls import loadFromFile, saveToFile

def unpickle(fileName):
	f = open(fileName, 'r')
	HTML_Dict = json.load(f)
	print(fileName)
	f.close()

	return HTML_Dict

def findProfits(books):
	profitable = {}
	for book in books:
		try:
			profit = float(books[book]["2015-05-24"]["tradeIn"][1:]) - float(books[book]["2015-05-24"]["usedPrice"][1:])
		except:
			print("")

		if profit >= 20.0:
			profitable[str(profit)] = book 

	# for key in sorted(profitable.iterkeys(), reverse=True):
	#     print "%s: %s" % (key, profitable[key])

	return(profitable)


def main():
	library = loadFromFile("pricesBackup.dat")
	profitable = findProfits(library)
	saveToFile(profitable, "profitableBooks.dat")


if __name__ == '__main__':
	main()