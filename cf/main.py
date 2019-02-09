import pandas as pd
import operator
from cf import use_base
from cf import item_base

# 处理训练数据 -> d
df = pd.read_csv('../jiebaHmm/data/u.data',
                 sep='\t',
                 # nrows=100,
                 names=['user_id', 'item_id', 'rating', 'timestamp'])
print(max(df['rating']))
d = dict()
for _, row in df.iterrows():
    user_id = str(row['user_id'])
    item_id = str(row['item_id'])
    rating = row['rating']
    if user_id not in d.keys():
        d[user_id] = {item_id: rating}
    else:
        d[user_id][item_id] = rating

# user base
C = use_base.user_sim(d)  # 建立item->users的倒排表
user = '196'
rank_u = use_base.recommend('196', d, C, 10)
print(len(rank_u))
print(user, '用户基于用户相似度推荐list：')
# 196用户基于用户相似度推荐list：[('100', 9.851188941720837), ('204', 8.791450922163456), ('211', 6.934643640329933), ('50', 6.703137256491896), ('56', 6.644745314666279), ('210', 6.343957775195162), ('514', 6.126770101477048), ('283', 6.097763471099605), ('216', 5.895079501083604), ('168', 5.732076556369226)]
print(sorted(rank_u.items(), key=operator.itemgetter(1), reverse=True)[0:10])

# item base
print(user, '用户基于物品相似度推荐list：')
C = item_base.item_sim(d)  # 物品与物品相似度矩阵
rank_i = item_base.recommendation(d, user, C, 10)
# 196用户基于物品相似度推荐list：[('50', 18442.285749027724), ('181', 14924.972817449705), ('100', 13655.322954207499), ('174', 10020.561164011922), ('204', 9950.711103961843), ('56', 9080.68076287219), ('172', 8735.814674945444), ('98', 7386.568845691629), ('210', 5869.079736128182), ('69', 4740.853142934972)]
print(sorted(rank_i.items(), key=lambda x: x[1], reverse=True)[0:10])
