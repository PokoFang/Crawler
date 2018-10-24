import requests
from requests_html import HTML
import pandas as pd
import numpy as np
import urllib

def fetch(url):
	response = requests.get(url) 
	# response.encoding = 'utf-8'
	#response = requests.get(url, cookies={'over18': '1'})  # Yes, I am 18 years old.
	return response

def get_infor(entry):
	return {
    'title': entry.find('div.title', first=True).text,
    'push': entry.find('div.nrec', first=True).text,
    'date': entry.find('div.date', first=True).text,
    'author': entry.find('div.author', first=True).text,
	}

page_num = 3 # total page number you want to crawl

url = 'https://www.ptt.cc/bbs/TaiwanDrama/index.html'

for i in range(page_num):
	print(url)
	resp = fetch(url)
	html = HTML(html=resp.text)
	entries = html.find('div.r-ent')

	for entry in entries: # get information of each post
		print(get_infor(entry))

	controls = html.find('a.btn.wide')
	link = controls[1].attrs['href']
	pre_url = urllib.parse.urljoin('https://www.ptt.cc/', link)
	url = pre_url
	i += 1