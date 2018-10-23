import requests
from requests_html import HTML
import pandas as pd
import numpy as np

def fetch(url):
	response = requests.get(url) 
	# response.encoding = 'utf-8'
	#response = requests.get(url, cookies={'over18': '1'})  # Yes, I am 18 years old.
	return response

def find_entries(doc):
	html = HTML(html=doc)
	post_entries = html.find('div.r-ent')
	return (post_entries)

def get_infor(entry):
	return {
    'title': entry.find('div.title', first=True).text,
    'push': entry.find('div.nrec', first=True).text,
    'date': entry.find('div.date', first=True).text,
    'author': entry.find('div.author', first=True).text,
	}

url = 'https://www.ptt.cc/bbs/TaiwanDrama/index.html'
resp = fetch(url)
entries =  find_entries(resp.text)

for entry in entries:
	print(get_infor(entry))


	
