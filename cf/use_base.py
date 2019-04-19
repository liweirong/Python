import pandas as pd
import math
import operator

df = pd.read_csv('../jiebaHmm/data/u.data',
                 sep='\t',
                 # nrows=100, # 取一百个
                 names=['user_id', 'item_id', 'rating', 'timestamp'])
# print("打分最大值" + str(max(df['rating'])))  # 打分最大值5
# 加载整个字典
d = dict()
# _, row 其中'_'对应前面的编号0、1、2、3、4....
for _, row in df.iterrows():
    user_id = str(row['user_id'])
    item_id = str(row['item_id'])
    rating = row['rating']
    if user_id not in d.keys():
        d[user_id] = {item_id: rating}
    else:
        d[user_id][item_id] = rating


# print(d)

# 1 获得用户和用户之间的相似度
# 1.1 正常逻辑的用户相似度计算
def user_normal_similarity(d):
    w = dict()  # 相似矩阵
    for u in d.keys():
        if u not in w:
            w[u] = dict()
        for v in d.keys():
            if u == v:
                continue
            union = len(set(d[u]) & set(d[v]))  # 两个用户交集的数量
            w[u][v] = 2.0 * union / (len(d[u]) + len(d[v]))  # 相似度计算求平均
    print(w['196'])  # '196': {'242': 3, '393': 4}
    print('all user cnt : ', len(w.keys()))
    print('user_196 sim user cnt: ', len(w['196']))
    return w


# 1.2 优化计算用户与用户之间的相似度 user->item => item->user
# 大数据情况下效率会高很多
def user_sim(d):
    # 建立item->users的倒排表
    item_users = dict()
    for u, items in d.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)
    # print("item_users['257']:", item_users['257']) # tem_users['257']: {'330', '668', '880', '210', '161', '701',...}
    # print(len(item_users['257']))  #  303

    # 计算用户共同items的数量
    C = dict()  # 存放统计用户与用户共同item数量
    N = dict()  # 存放用户对应的item数量
    for i, users in item_users.items():
        for u in users:
            if N.get(u, -1) == -1:  # 初始化1
                N[u] = 0
            N[u] += 1
            if C.get(u, -1) == -1:  # 获取不到
                C[u] = dict()
            for v in users:
                if u == v:
                    continue
                if C[u].get(v, -1) == -1:  # 初始化2
                    C[u][v] = 0
                C[u][v] += 1
                # 业内常用！！！！这是解决热度问题！！热度较高权重会变低
                # ######      物品热度      ######
                # i_pop = 1/math.log(1+len(item_users[i]))
                # 如果一个用户买的东西特别多，或者商品热门，对总的价值不大，权重需要降低
                # 优化点：C[u][v] += i_pop   ## 业内常用！！！！这是解决热度问题！！
    del item_users  # 把数据从内存中清理掉 item_users
    # max_cuv = 0.0

    # 计算最终的相似度
    for u, sim_users in C.items():
        for v, cuv in sim_users.items():
            C[u][v] = 2.0 * cuv / (N[u] + N[v])  # 相同的数量/两个的平均值
            # if max_cuv < 2*cuv / ((N[u]+N[v])*1.0):
            #     max_cuv = 2*cuv / ((N[u]+N[v])*1.0)
    print("C['244']", C['244'])
    print('all user cnt : ', len(C.keys()))  # 943
    print('user sim user cnt: ', len(C['244']))
    # print('max_cuv:',max_cuv)  # 0.91228
    return C


C = user_sim(d)

'''
user    :   用户id user = '196'
d       :   d[user_id][item_id] = rating(打分)   {用户1：{商品1:3,商品2:2...}...}
C       :   建立item->users的倒排表(相似度) {用户1:{用户2:0.50097,...}...}
k       :   取相似用户的个数
 return :其他k个用户中的物品，带分数的字典
'''


def recommend(user, d, C, k):
    rank = dict()
    # 用户评论过的电影
    interacted_items = d[user].keys()
    # v:电影商品、cuv:分值                        (1) = 相似度的分值，取倒序            取k个
    for v, cuv in sorted(C[user].items(), key=operator.itemgetter(1), reverse=True)[0:k]:
        # 相似的k个用户全部拿出来
        for i, rating in d[v].items():  # rating 打分
            if i in interacted_items:
                # 过滤掉已经评论过的电影（购买过的商品）
                continue
            elif rank.get(i, -1) == -1:
                rank[i] = 0
            rank[i] += cuv * rating  # 相似度 * 打分

    return rank  # 物品集合含打分


rank = recommend('196', d, C, 10)
print("------------------", C)
print("rank length:", len(rank))
print("前十个用户:")
print(rank)  # 前十个用户
print(sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[0:10])  # rank排序后的前十
# [('100', 9.851188941720837), ('204', 8.791450922163456), ('211', 6.934643640329933), ('50', 6.703137256491896), ('56', 6.644745314666279), ('210', 6.343957775195162), ('514', 6.126770101477048), ('283', 6.097763471099605), ('216', 5.895079501083604), ('168', 5.732076556369226)]
