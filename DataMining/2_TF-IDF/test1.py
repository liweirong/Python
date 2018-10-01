# stop_words = set()
# with open('stop_words','r',encoding='utf-8') as f:
#     for word_lst in f.readlines():
#         word = word_lst[0]
#         stop_words.add(word)
# print(stop_words)

# with open('./data/1business.seg.cln.txt', 'r', encoding='utf-8') as f:
#     word_freq = dict()
#     for line in f.readlines():
#         words = line.strip().split(' ')
#         print(words)

# a = '   \n排'
# print(a.strip())

a = [[1,2],[3,9]]
print(a[-1][-1])