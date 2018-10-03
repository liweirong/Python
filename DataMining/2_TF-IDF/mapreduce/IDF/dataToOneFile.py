import os
import sys

files_dir = '../../data'  # sys.argv[1]

for file_name in os.listdir(files_dir):
    file_path = files_dir + "/" + file_name
    file_in = open(file_path, 'r', encoding='utf8')

    # 需要吧句子首位相接，则需要定义临时数组
    tmp_list = []
    for line in file_in:
        tmp_list.append(line.strip())

    print('\t'.join([file_name, ' '.join(tmp_list)]))  # 每一行按空格拼接成一行后再把名字拼接
    break
# python dataToOneFile.py > merge_files.data
