import json

def unpickle(fileName):
	f = open(fileName, 'r')
	HTML_Dict = json.load(f)
	print(fileName)
	f.close()

	return HTML_Dict

def main():
	datapoints = unpickle("addresses.dat")	
	count = 0		
	for i in datapoints:
		count += 1

	print(count)	 

if __name__ == '__main__':
	main()