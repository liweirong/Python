import operator


def item_sim(d):
    # 1. 计算物品与物品相似度矩阵
    C = dict()
    N = dict()  # item拥有的user数据量
    for u, items in d.items():
        for i in items:
            # item拥有的user数据量
            if N.get(i, -1) == -1:
                N[i] = 0
            N[i] += 1
            if C.get(i, -1) == -1:
                C[i] = dict()
            for j in items:
                if i == j:  # 笛卡儿积不能去掉，1和2相似，2和你也相似
                    continue
                elif C[i].get(j, -1) == -1:
                    C[i][j] = 0
                C[i][j] += 1
                # break

    # print(C)
    # 计算最终相似度矩阵
    for i, related_items in C.items():
        for j, cij in related_items.items():
            C[i][j] += 2 * cij / ((N[i] + N[j]) * 1.0)
    return C


def recommendation(d, user_id, C, k):
    rank = dict()
    Ru = d[user_id]  # Ru：喜欢的物品的集合R(u)
    # print('196用户打分过的物品：',Ru)
    for i, rating in Ru.items():
        # print(i,'相似的物品集合top10：', sorted(C[i].items(), key=lambda x:x[1],reverse=True)[0:10])
        # break
        for j, sim in sorted(C[i].items(), key=operator.itemgetter(1), reverse=True)[0:k]:
            # 过滤这个user已经打分过的item。。为什么要过滤？数据会重复
            if j in Ru:
                continue
            elif rank.get(j, -1) == -1:
                rank[j] = 0
            rank[j] += sim * rating  # 相似度*物品打分
    return rank
