# encoding=utf-8
from __future__ import unicode_literals
import sys
from sklearn.feature_extraction.text import CountVectorizer
import token
import jieba
import jieba.posseg
import jieba.analyse

sys.path.append("../")

# ## 加载自定义字典
# 这个, 学生会, 打篮球, 么, 大, 数据
dict_file = 'myDict.text'
jieba.load_userdict(dict_file)
# 这个, 学生会, 打篮球, 么, 大数据

seg_list = jieba.cut("这个学生会打篮球么大数据", cut_all=False)
print(", ".join(seg_list))
s = '中国好声音'

# join相当于将数组中的字符拼成字符串，和scala中的mkString一样
print('/'.join(jieba.cut(s, cut_all=False)))

s_list = ['中文分词中文计算', '大数据中国好声音', '云计算中国好声音', '用结巴分词来做中文分词', '云计算大数据']
s_l = [' '.join(jieba.cut(x)) for x in s_list]

# 新词发现
#  ngram_range : tuple (min_n, max_n)
#        The lower and upper boundary of the range of n-values for different
#        n-grams to be extracted. All values of n such that min_n <= n <= max_n
#        will be used. 【中文，分词】，中文，计算
ngram_vec = CountVectorizer(ngram_range=(2, 3), token_pattern=r"\b\w+\b", min_df=0.3)
x1 = ngram_vec.fit_transform(s_l)
print(x1)
print(ngram_vec.vocabulary_)
print([x.replace(' ', '') for x in ngram_vec.vocabulary_.keys()])
