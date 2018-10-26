import requests
from requests_html import HTML
import pandas as pd
import numpy as np
import urllib
import jieba
import os
import sys

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

page_num = 30 # total page number you want to crawl

url = 'https://www.ptt.cc/bbs/TaiwanDrama/index.html'
del_list = []
voc_set = {}
print("程式預設編碼 : ",sys.getdefaultencoding(), ", cmd預設編碼 : ",sys.stdin.encoding)

for i in range(page_num):
	print('page: ', i, ', remaining page number: ', page_num - i)
	resp = fetch(url)
	html = HTML(html=resp.text)
	entries = html.find('div.r-ent')

	for entry in entries: # get information of each post
		entry_dict = get_infor(entry)
		if '(本文已被刪除)' in entry_dict['title']:
			entry_dict['author'] = entry_dict['title'][len('(本文已被刪除)') + 2:-1] # find the author ID of a deleted article
			del_list.append(entry_dict)

		else:
			start_idx = entry_dict['title'].find(']') + 2 # skip the article class
			# print(entry_dict['title'][start_idx: ])
			seg_list = jieba.cut(entry_dict['title'][start_idx: ], cut_all=False)
			count_voc(voc_set, seg_list)

	controls = html.find('a.btn.wide')
	link = controls[1].attrs['href']
	pre_url = urllib.parse.urljoin('https://www.ptt.cc/', link)
	url = pre_url
	i += 1

sorted_by_value = sorted(voc_set.items(), key=lambda kv: kv[1], reverse=True) # return a list of tuple ('str', num)

# output to a file in Users dic
with open ('voc_count.txt', 'w', errors='ignore') as out_f: # ignore the character cannot be decoded when writing (it's ok if we only print out)
	for v_tuple in sorted_by_value:
		padding = ' ' * (10 - len(v_tuple[0]))
		out_f.write("%s%s%d\n"%(v_tuple[0], padding, v_tuple[1]))
