import sys
import re

# 正则去符号，匹配字母和数字,去标点等
p = re.compile(r'\w+')
for line in sys.stdin:
    ss = line.strip().split(' ')
    for s in ss:
        if len(p.findall(s)) < 1:  # 防止单个符号“，”
            continue
        s_low = p.findall(s)[0].lower()
        print(s_low + '\t' + '1')

# 调试:
# head -2 The_Man_of_Property.txt| python map_t.py

# 直接读文件看效果
# file = open("The_Man_of_Property.txt", 'r', encoding='UTF-8')
# for line in file:
#     strings = line.strip().split(" ")
#     for string in strings:
#         # 正则去除无关的东西
#         if len(p.findall(string)) < 1:
#             continue
#         s_low = p.findall(string)[0].lower()
#         print(s_low, "\t", 1)
# file.close()
