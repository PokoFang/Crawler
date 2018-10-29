import jieba
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

''' # test jieba
seg_list = jieba.lcut("白先勇做出重大決定", cut_all=True) # return a list
print(seg_list)
#print("Full Mode: " + "/ ".join(seg_list))  # 全模式

voc_set = {}
seg_list1 = jieba.cut("白先勇做出重大的決定 他決定要去麥當勞吃白色的牛排", cut_all=False)
#print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

for item in seg_list1:
	if item in voc_set:
		voc_set[item] += 1
	else:
		voc_set[item] = 1
print(voc_set)

'''

''' # test remove punctuation
def remove_punctuation(line):
    rule = re.compile('[^a-zA-Z0-9\u4e00-\u9fa5]')
    line = rule.sub('',line)
    return line

#l = ' 愛的3.14159 劇名的意義．．．'
#print(remove_punctuation(l))
'''

# test wordcloud
#f = open('C:/Users/poko/voc_count_p500.txt').read()
f = open('text.txt').read()
stopwords = {}.fromkeys(['孩子']) # remove the word we don't want 
wordcloud = WordCloud(font_path="msjh.ttc", background_color="white",width=1000, height=860, margin=2, stopwords=stopwords).generate(f)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
