import requests
from requests_html import HTML
import pandas as pd
import numpy as np
import urllib
import jieba
import os
import sys
import re

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

def remove_punctuation(title_str):
    rule = re.compile('[^a-zA-Z0-9\u4e00-\u9fa5]')
    title_str = rule.sub('',title_str)
    return title_str

def count_voc(voc_set, seg_list, w_file):
	for item in seg_list:
		w_file.write(item) # not count, output all voc
		w_file.write(' ')
		if item in voc_set:
			voc_set[item] += 1
		else:
			voc_set[item] = 1
	return voc_set

def write_file(sorted_by_value, page_num):
	file_name = 'voc_count_p%d.txt'%page_num
	with open (file_name, 'w', errors='ignore') as out_f: # ignore the character cannot be decoded when writing (it's ok if we only print out)
		for v_tuple in sorted_by_value:
			padding = ' ' * (15 - len(v_tuple[0]))
			out_f.write("%s%s%d\n"%(v_tuple[0], padding, v_tuple[1]))

'''
def write_csv(sorted_by_value, page_num):
	file_name = 'voc_count_p%d.csv'%page_num
	df = pd.DataFrame(sorted_by_value, columns=['voc', 'count'])
	df.to_csv(file_name, index=False, encoding='cp950')
'''

page_num = 1 # total page number you want to crawl
url = 'https://www.ptt.cc/bbs/TaiwanDrama/index.html'
del_list = []
voc_set = {}
print("程式預設編碼 : ",sys.getdefaultencoding(), ", cmd預設編碼 : ",sys.stdin.encoding)

w_file = open('text.txt', 'w')
for i in range(page_num):
	print('page: ', i, ', remaining page number: ', page_num - i)
	resp = fetch(url)
	html = HTML(html=resp.text)
	entries = html.find('div.r-ent')

	# get information of each post
	for entry in entries: 
		entry_dict = get_infor(entry)
		if '(本文已被刪除)' in entry_dict['title']:
			entry_dict['author'] = entry_dict['title'][len('(本文已被刪除)') + 2:-1] # find the author ID of a deleted article
			del_list.append(entry_dict)

		else:
			start_idx = entry_dict['title'].find(']') + 2 # skip the article class
			title_str = entry_dict['title'][start_idx: ]
			title_str = remove_punctuation(title_str) # remove the punctuation
			seg_list = jieba.cut(title_str, cut_all=False)
			count_voc(voc_set, seg_list, w_file)

	# get the url of the previous page
	controls = html.find('a.btn.wide')
	link = controls[1].attrs['href']
	pre_url = urllib.parse.urljoin('https://www.ptt.cc/', link)
	url = pre_url
	i += 1

sorted_by_value = sorted(voc_set.items(), key=lambda kv: kv[1], reverse=True) # return a list of tuple ('str', num)
#write_file(sorted_by_value, page_num)
