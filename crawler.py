import requests
from requests_html import HTML
import pandas as pd
import numpy as np
import urllib
import jieba
import os

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

def count_voc(voc_set, seg_list):
	for item in seg_list:
		if item in voc_set:
			voc_set[item] += 1
		else:
			voc_set[item] = 1
	return voc_set

page_num = 1 # total page number you want to crawl

url = 'https://www.ptt.cc/bbs/TaiwanDrama/index.html'
del_list = []
voc_set = {}

for i in range(page_num):
	print(url)
	resp = fetch(url)
	html = HTML(html=resp.text)
	entries = html.find('div.r-ent')

	for entry in entries: # get information of each post
		entry_dict = get_infor(entry)
		if '(本文已被刪除)' in entry_dict['title']:
			entry_dict['author'] = entry_dict['title'][len('(本文已被刪除)') + 2:-1] # 抓出原文作者
			del_list.append(entry_dict)

		else:
			seg_list = jieba.cut(entry_dict['title'], cut_all=False)
			count_voc(voc_set, seg_list)

	controls = html.find('a.btn.wide')
	link = controls[1].attrs['href']
	pre_url = urllib.parse.urljoin('https://www.ptt.cc/', link)
	url = pre_url
	i += 1

with open ('voc_count.txt', 'w') as out_f: # Users dic
	for v in voc_set:
		padding = ' ' * (10 - len(v))
		out_f.write("%s%s%d\n"%(v, padding, voc_set[v]))