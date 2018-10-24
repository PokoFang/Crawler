import jieba

seg_list = jieba.lcut("白先勇做出重大決定", cut_all=True) # return a list
print(seg_list)
#print("Full Mode: " + "/ ".join(seg_list))  # 全模式

seg_list = jieba.lcut("白先勇做出重大決定", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = jieba.lcut_for_search("白先勇做出重大決定")  # 搜索引擎模式
print(", ".join(seg_list))
