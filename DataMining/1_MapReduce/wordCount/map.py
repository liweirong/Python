import sys
import re

# 正则去符号，匹配字母,去标点等
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
