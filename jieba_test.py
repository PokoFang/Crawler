import jieba

'''
seg_list = jieba.lcut("白先勇做出重大決定", cut_all=True) # return a list
print(seg_list)
#print("Full Mode: " + "/ ".join(seg_list))  # 全模式
'''
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
seg_list = jieba.lcut_for_search("白先勇做出重大決定")  # 搜索引擎模式
print(", ".join(seg_list))
'''