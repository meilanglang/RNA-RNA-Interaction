# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/12 14:12
@Auth ： langmei
@File ：parse_RNAplex.py
@IDE ：PyCharm
@Motto: ugly but useful
"""
import os

def parse_RNAplex(result_path, rri_pair,seq1_len):
    # dotresult
    #(((((((..((((((.(((((((&)))))))..)))))).)))))))   1,23  :   1,23  (-23.67 = -30.95 + 7.28)
    # index with 1
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    predict_file = result_path + pdb + "_" + chain_1_name + chain_2_name + '.txt'
    if os.path.exists(predict_file):
        with open(predict_file) as f:
            next(f)
            lines = f.readlines()
            #print(lines)
            ss = lines[0]
            ss = ss.split(" ")
            while '' in ss:
                ss.remove('')
            # print(first_line)
            ss1 = ss[0].split("&")[0]
            ss2 = ss[0].split("&")[1]
            ss1_start = int(ss[1].split(",")[0])
            ss2_start = int(ss[3].split(",")[0])
            chain_1 = []
            for index, item in enumerate(ss1, ss1_start):
                chain_1.append([index, item])
            chain_2 = []
            for index, item in enumerate(ss2, ss2_start):
                chain_2.append([index, item])
            for i in range(0, len(chain_2)):
                if chain_2[i][1] == ".":
                    continue
                if chain_2[i][1] == ")":
                    count = 0
                    tmp = chain_1.pop()
                    while tmp[1] == ".":
                        count = count + 1
                        tmp = chain_1.pop()
                    tmp = tmp
                    predict_pair.append([tmp[0], chain_2[i][0]])
    else:
        print("no structure")
    rri_pair = []
    for pair in predict_pair:
        rri_pair.append([pair[0] - 1, pair[1] - 1 + seq1_len])

    return rri_pair
