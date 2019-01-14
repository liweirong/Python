import pandas as pd
import math
import operator

df = pd.read_csv('../jieba_hmm/data/u.data',
                 sep='\t',
                 # nrows=100,
                 names=['user_id', 'item_id', 'rating', 'timestamp'])
print("打分最大值" + max(df['rating']))
d = dict()
for _, row in df.iterrows():
    user_id = str(row['user_id'])
    item_id = str(row['item_id'])
    rating = row['rating']
    if user_id not in d.keys():
        d[user_id] = {item_id: rating}
    else:
        d[user_id][item_id] = rating


# print(d)

# 1. 获得用户和用户之间的相似度
# 1.1正常逻辑的用户相似度计算
def user_normal_simmilarity(d):
    w = dict()
    for u in d.keys():
        if u not in w:
            w[u] = dict()
        for v in d.keys():
            if u == v: continue
            w[u][v] = len(set(d[u]) & set(d[v]))
            w[u][v] = 2 * w[u][v] / (len(d[u]) + len(d[v])) * 1.0
    print(w['196'])
    print('all user cnt : ', len(w.keys()))
    print('user_196 sim user cnt: ', len(w['196']))
    return w


# 1.2 优化计算用户与用户之间的相似度 user->item => item->user
def user_sim(d):
    # 建立item->users的倒排表
    item_users = dict()
    for u, items in d.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)
    # 物品热度
    # i_pop = 1/math.log(1+len(item_users[i]))
    # print(item_users['257'])
    # print(len(item_users['257']))

    # 计算用户共同items的数量
    C = dict()  # 存放统计用户与用户共同item数量
    N = dict()  # 存放用户对应的item数量
    for i, users in item_users.items():
        for u in users:
            if N.get(u, -1) == -1: N[u] = 0
            N[u] += 1
            if C.get(u, -1) == -1:
                C[u] = dict()
            for v in users:
                if u == v: continue
                if C[u].get(v, -1) == -1: C[u][v] = 0
                C[u][v] += 1
                # C[u][v] += 1/math.log(1+len(item_users[i]))   ## 这是解决热度问题
    del item_users
    # max_cuv = 0.0
    # 计算最终的相似度
    for u, sim_users in C.items():
        for v, cuv in sim_users.items():
            C[u][v] = 2 * cuv / ((N[u] + N[v]) * 1.0)  # 相同的数量/两个的平均值
            # if max_cuv<2*cuv / ((N[u]+N[v])*1.0):
            #     max_cuv = 2*cuv / ((N[u]+N[v])*1.0)
    print(C['244'])
    print('all user cnt : ', len(C.keys()))
    print('user sim user cnt: ', len(C['244']))
    # print('max_cuv:',max_cuv)
    return C


C = user_sim(d)
user = '196'


def recommend(user, d, C, k):
    items = list()
    rank = dict()
    # 用户评论过的电影
    interacted_items = d[user].keys()
    for v, cuv in sorted(C[user].items(), key=operator.itemgetter(1),
                         reverse=True)[0:k]:
        for i, rating in d[v].items():  # rating 打分
            if i in interacted_items:
                # 过滤掉已经评论过的电影（购买过的商品）
                continue
            elif rank.get(i, -1) == -1:
                rank[i] = 0
            rank[i] += cuv * rating
    return rank  # 物品集合含打分


rank = recommend('196', d, C, 10)
print(len(rank))
print(rank)  # 前十个用户
print(sorted(rank.items(), key=operator.itemgetter(1),
             reverse=True)[0:10])  # rank排序后的前十
