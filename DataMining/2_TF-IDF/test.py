import jieba

s1 = "这只皮靴号码大了。那只号码合适"
s2 = "这只皮靴号码不小，那只更合适"

# 读取停用词表
stop_words = set()
with open('stop_words', 'r', encoding='utf-8') as f:
    for word_lst in f.readlines():
        word = word_lst[0]
        stop_words.add(word)
# print(stop_words)

s1_seg = '/'.join([x for x in jieba.cut(s1, cut_all=True) if x not in stop_words and x != ''])
s1_lst = [x for x in jieba.cut(s1, cut_all=True) if x not in stop_words and x != '']
print(s1_lst)
s1_set = set(s1_lst)

s2_seg = '/'.join([x for x in jieba.cut(s2, cut_all=True) if x != ''])
s2_lst = [x for x in jieba.cut(s2, cut_all=True) if x != '']
s2_set = set(s2_lst)

word_dict = dict()
i = 0
for word in s1_set.union(s2_set):
    # if word in stop_words:
    #     continue
    word_dict[word] = i
    i += 1
print(word_dict)

# def word_to_vec(word_dict,s1_lst):
#     word_count1 = dict()
#     s1_vector = [0] * len(word_dict)
#     for word in s1_lst:
#         if word in stop_words:
#             continue
#         if word_count1.get(word, -1) == -1:
#             word_count1[word] = 1
#         else:
#             word_count1[word] += 1
#     # print(word_count1)
#
#     for word,freq in word_count1.items():
#         wid = word_dict[word]
#         s1_vector[wid] = freq
#     # print(s1_vector)
#     return s1_vector
#
# s1_vector = word_to_vec(word_dict,s1_lst)
# print(s1_vector)
# s2_vector = word_to_vec(word_dict,s2_lst)
# print(s2_vector)


# print(s1_seg)
# print(s2_seg)
