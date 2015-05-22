#helper file with useful file related functions
import json
import requests
from bs4 import BeautifulSoup

def loadFromFile(fileName):
	#loads data from a file and returns said data
	f = open(fileName, 'r')
	data = json.load(f)
	f.close()
	return data

def saveToFile(structure, fileName):
	#takes in a data structure and writes it to a file
	f = open(fileName, 'w')
	json.dump(structure,f, default=jdefault)
	f.close()

def jdefault(o):
	#needed to save objects (makes objects writable, even if unwritable by default)
	return o.__dict__

def makeSoup(href):
	source_code = requests.get(href)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text)
	return soup