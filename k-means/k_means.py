import os
import math
import random
import operator

K = 10  # 设定类别数量（簇）
WCSS = 0.0  # 初始化wcss(损失函数)
new_WCSS = 1  # 初始化
threshold = 1e-6  # 认为不变动的阈值
ITER_MAX = 20  # 设定最大迭代次数

file_path = './data'  # 数据路径

label_dict = {'business': 0, 'yule': 1, 'it': 2, 'sports': 3, 'auto': 4}

word_dict = dict()  # 对word进行编码


def load_data():
    '''
    加载新闻数据，并做词频统计（word count）
    :return: doc_dict{文档名：word_freq}, doc_list文档名列表
    '''
    doc_list = []
    doc_dict = dict()
    i = 0
    for filename in os.listdir(file_path):
        doc_name = filename.split('.')[0]
        doc_list.append(doc_name)
        if i % 100 == 0:
            print(i, 'files loaded!!')
        with open(file_path + '/' + filename, 'r', encoding='utf-8') as f:
            word_freq = dict()  # tf，统计逻辑word count，结果需要的字典结构
            for line in f.readlines():
                words = line.strip().split(' ')
                for word in words:
                    if len(word.strip()) < 1:
                        continue
                    # 对word进行编码
                    if word_dict.get(word, -1) == -1:
                        word_dict[word] = len(word_dict)
                    wid = word_dict.get(word, -1)
                    # word count统计逻辑
                    if word_freq.get(wid, -1) == -1:
                        word_freq[wid] = 1
                    else:
                        word_freq[wid] += 1

            doc_dict[doc_name] = word_freq
        i += 1
    return doc_dict, doc_list


def idf(doc_dict):
    '''
    统计每个单词的文档频率
    :param doc_dict: {文档名：word_freq}
    :return: word_idf {word：idf值}
    '''
    word_idf = {}
    # 统计doc freq  doc_dict {word：出现的doc数量}
    for doc in doc_dict.keys():  # doc_dict{文档名：word_freq}
        for word in doc_dict[doc].keys():
            if word_idf.get(word, -1) == -1:
                word_idf[word] = 1
            else:
                word_idf[word] += 1
    doc_num = len(doc_dict)
    # 计算idf
    for word in word_idf.keys():
        word_idf[word] = math.log(doc_num / (word_idf[word] + 1))
    return word_idf


def doc_tf_idf():
    '''
    实现tf*idf,计算每篇文章中对应每个单词的tf-idf值
    :return: doc_dict {文档名：{单词：tf-idf值}}, doc_list文档名列表
    '''
    doc_dict, doc_list = load_data()
    word_idf = idf(doc_dict=doc_dict)

    for doc in doc_list:
        for word in doc_dict[doc].keys():
            doc_dict[doc][word] = doc_dict[doc][word] * word_idf[word]
    return doc_dict, doc_list


def init_K(doc_dict, doc_list):
    '''
    初始化K个中心点，随机选择样本点为中心点
    :param doc_dict: 样本数据，每个doc是一条样本
    :param doc_list: 样本数据doc名
    :return:
    '''
    center_dict = dict()
    k_doc_list = random.sample(doc_list, K)
    i = 0
    for doc_name in k_doc_list:
        center_dict[i] = doc_dict[doc_name]
        i += 1
    return center_dict


def compute_dis(doc1, doc1_dict, doc2, doc2_dict):
    '''
    计算样本与样本之间的距离
    :param doc1: 一个样本
    :param doc1_dict: 样本数据
    :param doc2: 另一个样本
    :param doc2_dict: 另一个样本数据
    :return: sum两个样本的欧式距离
    '''
    sum = 0.0
    # 两个文档总共的去重单词数
    words = set(doc1_dict[doc1]).union(set(doc2_dict[doc2]))
    for wid in words:
        d = doc1_dict[doc1].get(wid, 0.0) - doc2_dict[doc2].get(wid, 0.0)
        sum += d * d
    return sum


def compute_center(doc_list, doc_dict):
    '''
    重新计算其中一个样本点的中心点
    :param doc_list: 属于第k个的所有样本
    :param doc_dict: 样本字典 {文档名：{单词wid：tf-idf值}}
    :return: 中心点（坐标），因为维度比较多存储到dict中
    '''
    tmp_center = dict()

    for doc in doc_list:
        for wid in doc_dict[doc].keys():
            if tmp_center.get(wid, -1) == -1:
                tmp_center[wid] = doc_dict[doc][wid]
            else:
                tmp_center[wid] += doc_dict[doc][wid]

    for wid in tmp_center.keys():
        tmp_center[wid] /= len(doc_list)
    return tmp_center


def all_k_dist(doc_list, doc_dict, k, k_dict):
    sum = 0.0
    for doc in doc_list:
        tmp_k_dict = {k: k_dict}
        sum += compute_dis(doc, doc_dict, k, tmp_k_dict)
    return sum


if __name__ == '__main__':
    doc_dict, doc_list = doc_tf_idf()
    center_dict = init_K(doc_dict, doc_list)
    doc_k = dict(zip(doc_list, [0 for i in range(len(doc_list))]))

    iter_num = 0
    Center_mv = 1
    print('start train!!')
    while new_WCSS - WCSS > threshold and iter_num < ITER_MAX and Center_mv > threshold:
        k_doc = dict()
        for doc in doc_list:
            tmp_select_k = dict()
            for k in center_dict.keys():
                tmp_select_k[k] = compute_dis(doc, doc_dict, k, center_dict)
            # (k, val) = sorted(tmp_select_k.items(), key=operator.itemgetter(1))[0]
            (k, val) = min(tmp_select_k.items(), key=operator.itemgetter(1))
            doc_k[doc] = k
            if k_doc.get(k, -1) == -1:
                k_doc[k] = [doc]
            else:
                k_doc[k].append(doc)

        # step 2:
        Center_mv = 0
        WCSS = new_WCSS
        new_WCSS = 0
        for k in k_doc.keys():
            tmp_k_center = compute_center(k_doc[k], doc_dict)
            tmp_new_k_center = {k: tmp_k_center}
            Center_mv += compute_dis(k, center_dict, k, tmp_new_k_center)
            new_WCSS += all_k_dist(doc_list, doc_dict, k, center_dict[k])
            center_dict[k] = tmp_k_center
        print(iter_num)
        iter_num += 1
