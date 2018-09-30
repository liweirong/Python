import sys

cur_word = None
sum = 0
for line in sys.stdin:
    word, val = line.strip().split('\t')
    if cur_word == None:
        cur_word = word
    if cur_word != word:
        print('%s\t%s' % (cur_word, sum))
        cur_word = word
        sum = 0
    sum += int(val)
print('%s\t%s' % (cur_word, sum))
