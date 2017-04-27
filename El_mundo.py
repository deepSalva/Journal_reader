# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import sys
import re

def dict_maker(soup):
	d = dict()
	for c in packing_words(soup):
		d[c] = 1 + d.get(c, 0)
	return d

def list_maker(soup):
	pattern = re.compile(r'>((([a-zA-Z]{2,})\s)+?(\w{2,})+?)<')
	word_list = pattern.findall(str(soup))
	return(word_list)

def unpacking_tuples(soup):
	word_list = list_maker(soup)
	keys = []
	for item in word_list:
		a, b, c, d = item
		keys.append(a)
	return keys

def packing_words(soup):
	list_from_tuples = unpacking_tuples(soup)
	final_list = list()
	for i in range(len(list_from_tuples)):
		res = list(list_from_tuples[i].split())
		for i in range(len(res)):
			if len(res[i]) > 3:
				final_list.append(res[i])
	return final_list

def invert_dict(d): #invert a dictionary 'd'
	reverse = dict()
	for key in d:
		val = d[key]
		if val not in reverse:
			reverse[val] = [key]
		else:
			reverse[val].append(key)
	return reverse

def most_frequent(soup):
	histo_dict = dict_maker(soup)
	invert_dicti = sorted(invert_dict(histo_dict).items())
	for key, value in invert_dicti[:3]:
		print(key, value)

def main(name, webname1="http://www.elmundo.es/", 
	webname2="http://elpais.com/", webname3="http://www.publico.es/", 
	webname4="http://www.abc.es/", webname5="https://www.washingtonpost.com/"):
	
	req = requests.get(webname2)

	statusCode = req.status_code

	# Comprobamos que la petición nos devuelve un Status Code = 200
	status_code = req.status_code

	if status_code == 200:
		soup = BeautifulSoup(req.text, "html.parser")
		#print(dict_maker(soup))
		most_frequent(soup)

	else:
		print("Status Code %d" % status_code)


if __name__ == '__main__':
	main(*sys.argv)