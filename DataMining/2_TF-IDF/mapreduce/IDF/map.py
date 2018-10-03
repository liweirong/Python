import sys

for line in sys.stdin:
    ss = line.strip().split('\t')
    file_name = ss[0].strip()
    file_context = ss[1].strip()
    word_list = file_context.split(' ')

    # 对每一行出现的数据只要去重即可，不统计次数
    word_set = set()
    for word in word_list:
        word_set.add(word)

    for word in word_set:
        print('\t'.join([word, '1']))

    break;  # 加上为操作一篇

# cat merge_files.data | python map.py | sort | uniq |wc -l  #去重以后有多少个
# cat merge_files.data | python map.py > map.tmp 存入临时文件
