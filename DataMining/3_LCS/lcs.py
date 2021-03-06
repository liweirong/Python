# ?a?b??????
a = "ABCBDAB"
b = "BDCABA"


def lcs(a, b):
    n = len(a)
    m = len(b)
    l = [[0] * (m + 1) for i in range(n + 1)]
    for i in l:
        print(i)

    for i in range(n + 1)[1:]:
        for j in range(m + 1)[1:]:
            if a[i - 1] == b[j - 1]:
                l[i][j] = l[i - 1][j - 1] + 1
            else:
                l[i][j] = max(l[i - 1][j], l[i][j - 1])
    return l[-1][-1]


l = lcs(a, b)
print("*" * 20)
print(a + "和" + b + "最长字串的长度是: " + str(l))
