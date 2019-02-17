from numpy import *
import matplotlib.pyplot as plt

# 数据形式
'''
    x1          x2      y
-0.017612   14.053064	0
-1.395634	4.662541	1
-0.752157	6.538620	0
-1.322371	7.152853	0
0.423363	11.054677	0
'''
data = []
label = []
fr = open('data/testSet.txt')
for line in fr.readlines():
    line = line.strip().split()  # ['-0.017612', '14.053064', '0']
    data.append([1.0, float(line[0]), float(line[1])])  # 多元线性回归，对数据进行处理，统一多加一
    label.append(int(line[2]))


# print(data)  # [[1.0, -0.017612, 14.053064], [1.0, -1.395634, 4.662541]..]
# print(label)  # [0, 1, 0, 0, 0, 1, 0, 1, 0, 0...]


def plot_function(data, label, weights=None):
    n = shape(data)[0]  # shape(100,3)
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for i in range(n):
        if int(label[i]) == 1:
            x1.append(data[i][1])
            y1.append(data[i][2])
        else:
            x2.append(data[i][1])
            y2.append(data[i][2])
    fig = plt.figure()
    ax = fig.add_subplot(111)  # 随便写
    # 画散点图
    ax.scatter(x1, y1, s=100, c='red', marker='s')
    ax.scatter(x2, y2, s=100, c='black')

    if weights != None:
        x = arange(-3.0, 3.0, 0.1)  # 按照间隔0.1去取
        y = -(weights[0] + weights[1] * x) / weights[2]  # x2=-(w1x1+w[0])/w2
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()


# 调用sigmoid函数
def sigmoid(t):
    return 1.0 / (1 + exp(-t))


data = mat(data)  # matrix 100*3
label = mat(label).transpose()  # 或者 .T  转置
m, n = shape(data)  # m=100 n=3
alpha = 0.015  # 步长
maxIter = 10000  # 最大迭代次数
weights = ones((n, 1))  # 3 * 1的向量,w1 <=> b  | W  3行1列
# print('-label.T  ',-label)
print(ones((m, 1)).T - label.T)
i = 0
loss = None
# for k in range(maxIter):
# 损失函数是为了选择最好的参数
while i < maxIter:
    y = sigmoid(data * weights)  # 100*1  yi 1-yi
    l_wx = -label.T * log(y) - (ones((m, 1)).T - label.T) * log(1 - y)
    # 终止条件2
    if loss is None:
        loss = l_wx
    elif abs(loss - l_wx) < 1e-5:
        break
    else:
        loss = l_wx

    print('step ', i, ',loss: ', l_wx)
    error = label - y  # 误差，损失
    grad = -data.T * error  # 梯度
    weights -= alpha * grad
    i += 1
    # alpha = alpha*0.5
print(weights.T.tolist()[0])  # [15.932379562867153, 1.332665263838787, -2.1623852453459946]
plot_function(data.tolist(), label, weights.T.tolist()[0])

print(1e-3)
