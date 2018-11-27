# -*- coding: utf-8 -*-

readFileName = "./fff"
writeFileName = "./flume_exec_test.txt"
with open(writeFileName, 'a+')as wf:
    with open(readFileName, 'rb') as f:
        for line in f.readlines():
            for word in line.split(" "):
                print(word)
                ss = line.strip()
                if len(ss) < 1:
                    continue
                wf.write(ss+'\n')
