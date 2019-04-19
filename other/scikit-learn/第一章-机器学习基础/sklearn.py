# encoding=utf-8
import numpy as np
import matplotlib.pyplot as plt

# X = np.array([[6], [8], [10], [14], [18]]).reshape(-1, -1)
# y = [7, 9, 17.5, 20, 29]
# plt.figure()
# plt.title('qeqwe')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.plot(X, y, 'k.')
# plt.axes([0, 25, 0, 25])
# plt.grid(True)
# plt.show()


# 月份
x1 = ['2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08',
      '2017-09', '2017-10', '2017-11', '2017-12']

# 体重
y1 = [86, 85, 84, 80, 75, 70, 70, 74, 78, 70, 74, 80]

# 设置画布大小
plt.figure(figsize=(16, 4))

# 标题
plt.title("my weight")

# 数据
plt.plot(x1, y1, label='weight changes', linewidth=3, color='r', marker='o',
         markerfacecolor='blue', markersize=20)

# 横坐标描述
plt.xlabel('month')

# 纵坐标描述
plt.ylabel('weight')

# 设置数字标签
for a, b in zip(x1, y1):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=20)

plt.legend()
plt.show()