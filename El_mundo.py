# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import sys
import re
import os

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

def dict_maker(soup):
	d = dict()
	for c in packing_words(soup):
		d[c] = 1 + d.get(c, 0)
	return d

def most_frequent(soup):
	histo_dict = dict_maker(soup)
	invert_dicti = sorted(invert_dict(histo_dict).items())
	list_mfreq = []
	for key, value in invert_dicti[:3]:
		list_mfreq.append(sorted(value))
		#print(key, sorted(value))
	return list_mfreq

def printer(list_mfreq):
	text1 = ", ".join(list_mfreq[0])
	text2 = ", ".join(list_mfreq[1])
	text3 = ", ".join(list_mfreq[2])

	making_text = ("Common words #1: \n %s " % text1 + "\n\n" + 
		"Common words #2: \n %s " % text2 + "\n\n" + "Common words #3: \n %s"
		 % text3)

	return making_text

def main(name, webname1="http://www.elmundo.es/", 
	webname2="http://elpais.com/", webname3="http://www.publico.es/", 
	webname4="http://www.abc.es/", webname5="https://www.washingtonpost.com/"):
	
	cwd = os.getcwd()

	req = requests.get(webname2)

	statusCode = req.status_code

	# Comprobamos que la petición nos devuelve un Status Code = 200
	status_code = req.status_code

	if status_code == 200:
		soup = BeautifulSoup(req.text, "html.parser")
		#print(dict_maker(soup))
		#most_frequent(soup)
		data = printer(most_frequent(soup))
		fout = open(cwd + '\Key_words.txt', 'w')
		fout.write(data)
		fout.close()
		os.startfile('Key_words.txt')

	else:
		print("Status Code %d" % status_code)


if __name__ == '__main__':
	main(*sys.argv)