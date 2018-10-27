import re

def remove_punctuation(line):
    rule = re.compile('[^a-zA-Z0-9\u4e00-\u9fa5]')
    line = rule.sub('',line)
    return line

l = ' 愛的3.14159 劇名的意義．．．'
print(remove_punctuation(l))