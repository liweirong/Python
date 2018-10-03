import sys
import math

doc_cunt = 508  # 文章总数

current_word = None
count_pool = []
sum = 0

for line in sys.stdin:
    ss = line.strip().split('\t')
    if len(ss) != 2:
        continue
    word, val = ss
    if current_word is None:
        current_word = word
    if current_word != word:
        for count in count_pool:
            sum += count
        # IDF
        idf_score = math.log(float(doc_cunt) / (float(sum) + 1))
        print('\t'.join([current_word, str(idf_score)]))
        # 求完一行后开始再次初始化
        current_word = word
        count_pool = []
        sum = 0

    count_pool.append(int(val))

for count in count_pool:
    sum += count
# 最后一个数据IDF
idf_score = math.log(float(doc_cunt) / (float(sum) + 1))
print('\t'.join([current_word, str(idf_score)]))

# cat map.tmp |sort -k1 | python red.py > red.tmp
# cat red.tmp | sort -k2 -nr > red.sort
