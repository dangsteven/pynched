#add comment soon

import json

def load_from_file(fileName):
	f = open(fileName, 'r')
	data = json.load(f)
	f.close()
	return data

def save_to_file(structure, fileName):
	f = open(fileName, 'w')
	json.dump(structure,f, default=jdefault)
	f.close()

def jdefault(o):
	return o.__dict__