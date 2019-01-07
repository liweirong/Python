from jieba_hmm.HMM import hmm_train

mod_path = '../data/model_file.txt'

# 1. 加载模型参数
# 1.1 初始化参数，用来存模型参数
# 其中S状态为:B,M,E,S  S状态大小M=4
STATUS_NUM = 4

pi = [0.0 for col in range(STATUS_NUM)]
A = [[0.0 for col in range(STATUS_NUM)] for row in range(STATUS_NUM)]
B = [dict() for col in range(STATUS_NUM)]

f = open(mod_path, 'r', encoding='utf-8')

# 1.2 读取模型文件第一行，加载到pi向量中
pi_tokens = f.readline().split()
for i in range(STATUS_NUM):
    pi[i] = float(pi_tokens[i])
# print(pi)
# 1.3 读取M行，即M*M的矩阵A
for i in range(STATUS_NUM):
    A_i_tokens = f.readline().split()
    for j in range(STATUS_NUM):
        A[i][j] = float(A_i_tokens[j])

# print(A)

# 1.4 读取矩阵B：S(BMES)->O(中文每个字)
for i in range(STATUS_NUM):
    B_i_tokens = f.readline().split()
    # 对应S状态中文字的个数
    token_num = len(B_i_tokens)
    j = 0
    while j < token_num - 1:
        B[i][B_i_tokens[j]] = float(B_i_tokens[j + 1])
        j += 2
print(B)
f.close()

# 2. 实现viterbi算法（预测最优路径）
ch = "我在八斗学习大数据和机器学习"


# ch = "蓝天、碧水、净土保卫战顺利推进，各项民生事业加快发展，人民生活持续改善。京津冀协同发展、长江经济带发"


def hmm_seg_func(ch=''):
    ch_lst = hmm_train.get_word_ch(ch)
    ch_num = len(ch_lst)

    # init
    # 【概率，状态】
    status_matrix = [[[0.0, 0] for col in range(ch_num)]  \
                     for st in range(STATUS_NUM)]

    for i in range(STATUS_NUM):
        if ch_lst[0] in B[i]:
            cur_B = B[i][ch_lst[0]]
        else:
            cur_B = -1000000.0  # 语料中未出现，给一个很小的值 -1000000.0
        if pi[i] == 0.0:
            cur_pi = -1000000.0
        else:
            cur_pi = pi[i]
        status_matrix[i][0][0] = cur_pi + cur_B  # pi*发射概率
        status_matrix[i][0][1] = i  # 状态
    # 从1开始  k跳转到j  复杂度=T*M*M
    for i in range(1, ch_num):  # i->T
        # print([i for i in range(1,ch_num)])
        for j in range(STATUS_NUM):  # i->后一层M
            max_p = None
            max_status = None
            for k in range(STATUS_NUM):  # i->前一层的M
                cur_A = A[k][j]
                if cur_A == 0.0: cur_A = -1000000.0
                cur_p = status_matrix[k][i - 1][0] + cur_A  # pi*发射概率*转移
                if max_p is None or max_p < cur_p:
                    max_p = cur_p
                    max_status = k

            if ch_lst[i] in B[j]:
                cur_B = B[j][ch_lst[i]]
            else:
                cur_B = -1000000.0  # 发射概率
            status_matrix[j][i][0] = max_p + cur_B
            status_matrix[j][i][1] = max_status

    # get max p path 最大概率路径
    max_end_p = None
    max_end_status = None
    for i in range(STATUS_NUM):
        if max_end_p is None or status_matrix[i][ch_num - 1][0] > max_end_p:
            max_end_p = status_matrix[i][ch_num - 1][0]
            max_end_status = i
    best_status_lst = [0 for ch in range(ch_num)]  # 最大路径
    best_status_lst[ch_num - 1] = max_end_status  # 最后一个概率最大的状态

    c = ch_num - 1
    cur_best_status = max_end_status
    while c > 0:
        pre_best_status = status_matrix[cur_best_status][c][1]  # 回溯
        best_status_lst[c - 1] = pre_best_status
        cur_best_status = pre_best_status
        c -= 1

    # d = {'0': 'B', '1': 'M', '2': 'E', '3': 'S'}
    # print(ch)
    # print([d.get(str(i)) for i in best_status_lst])

    # 4. 实现切词
    s = ""
    s += ch_lst[0]
    for i in range(1, ch_num):
        # i-1 是E，S 或者 i是B，S
        if best_status_lst[i - 1] in {2, 3} or best_status_lst[i] in {0, 3}:
            s += " "
        s += ch_lst[i]
    return s


# print(s)
# import jieba
# print('/'.join(jieba.cut(ch,cut_all=False)))

if __name__ == '__main__':
    write_path = './write_file.txt'  # 输入
    read_path = './read_file.txt'   # 输出 切完词后存储
    f_write = open(write_path, 'w', encoding='utf-8')
    f_seg = open(read_path, 'r', encoding='utf-8')
    import jieba

    for line in f_seg.readlines():
        line = line.strip()
        if len(line) < 1: continue
        s = hmm_seg_func(line)
        # s = ' '.join(jieba.cut(line, cut_all=False))
        f_write.write(s + '\n')

    f_seg.close()
    f_write.close()
    # import os
    # for filename in os.listdir('./'):
    #     print(filename)
