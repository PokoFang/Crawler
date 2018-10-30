import requests
from requests_html import HTML
import pandas as pd
import numpy as np
import urllib
import jieba
import os
import sys
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def fetch(url):
	response = requests.get(url) 
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

def count_voc(voc_set, seg_list):
	for item in seg_list:
		if item in voc_set:
			voc_set[item] += 1
		else:
			voc_set[item] = 1
		
	return voc_set

def write_file(sorted_by_value, page_num, i):
	file_name = 'C:/Users/poko/Documents/GitHub/Crawler/voc_count_p%d.txt'%i
	with open (file_name, 'w', errors='ignore') as out_f: # ignore the character cannot be decoded when writing (it's ok if we only print out)
		for v_tuple in sorted_by_value:
			padding = ' '# * (15 - len(v_tuple[0]))
			out_f.write("%s%s%d\n"%(v_tuple[0], padding, v_tuple[1]))

# jieba dictionay adjustment
jieba.suggest_freq('八點檔', True)
jieba.suggest_freq(('集', '台視'), True)
jieba.suggest_freq(('你的孩子不是你的孩子'), True)
jieba.suggest_freq(('一把青'), True)
jieba.suggest_freq(('如朕親臨'), True)
jieba.suggest_freq(('台', '八點'), True)
jieba.suggest_freq(('請閉眼'), True)
jieba.suggest_freq(('20之後'), True)
jieba.suggest_freq(('必娶女人'), True)
jieba.suggest_freq(('艋舺'), True)
jieba.suggest_freq(('愛上哥們'), True)

page_num = 1500 # total page number you want to crawl
url = 'https://www.ptt.cc/bbs/TaiwanDrama/index.html'
del_list = []
voc_set = {}
print("程式預設編碼 : ",sys.getdefaultencoding(), ", cmd預設編碼 : ",sys.stdin.encoding)

#w_file = open('text_p%d.txt'%page_num, 'w', errors='ignore')
for i in range(1, page_num + 1):
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
			with open ('C:/Users/poko/Documents/GitHub/Crawler/del_infor_p%d.txt'%page_num, 'w') as d_f:
				d_f.write(entry_dict['author'] + ' ' + entry_dict['date'] + '\n')

		else:
			start_idx = entry_dict['title'].find(']') + 2 # skip the article class
			title_str = entry_dict['title'][start_idx: ]
			title_str = remove_punctuation(title_str) # remove the punctuation
			seg_list = jieba.cut(title_str, cut_all=False)
			voc_set = count_voc(voc_set, seg_list)

	# get the url of the previous page
	controls = html.find('a.btn.wide')
	link = controls[1].attrs['href']
	pre_url = urllib.parse.urljoin('https://www.ptt.cc/', link)
	url = pre_url

	stopwords = ['的', '第', '集', '是', '嗎' ,'了', '之', '在', '篇']
	for sw in stopwords:
		voc_set.pop(sw, None)
	
	if i % 500 == 0: # output the result every 100 page
		# create wordcloud
		wordcloud = WordCloud(font_path="msjh.ttc", background_color="white",width=1000, height=860, margin=2).generate_from_frequencies(frequencies=voc_set)
		plt.imshow(wordcloud)
		plt.axis("off")
		wordcloud.to_file('C:/Users/poko/Documents/GitHub/Crawler/wc_p%d.png'%i)
		# plt.show()

		sorted_by_value = sorted(voc_set.items(), key=lambda kv: kv[1], reverse=True) # return a list of tuple ('str', num)
		write_file(sorted_by_value, page_num, i)
	
	i += 1