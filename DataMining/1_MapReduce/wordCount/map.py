import sys
import re

# 正则去符号，匹配字母
p = re.compile(r'\w+')
for line in sys.stdin:
    ss = line.strip().split(' ')
    for s in ss:
        if len(p.findall(s)) < 1:  # 防止单个符号“，”
            continue
        s_low = p.findall(s)[0].lower()
        print(s_low + '\t' + '1')
