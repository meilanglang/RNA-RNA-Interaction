# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/11 21:24
@Auth ： langmei
@File ：parse_RIsearch.py
@IDE ：PyCharm
@Motto: ugly but useful
"""
import os

def parse_RIsearch(result_path, rri_pair, len_seq1):
    """
    index begin with 1
    Args:
        result_path:
        rri_pair:
        len_seq1:

    Returns:

    """
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    RIsearch_res = result_path + pdb + "_" + chain_1_name + chain_2_name + '.out'
    #RIsearch_res = result_path + "risearch_" + chain + ".out"
    if os.path.exists(RIsearch_res):
        with open(RIsearch_res, "r") as f:
            lines = f.readlines()
            if lines == []:
                pass
            else:
                #print(lines)
                ss_n = len(lines) // 4
                print(ss_n)
                min_energe = 0
                min_index = 0
                for i in range(0,ss_n):
                    energe = float(lines[(i+1)*4-1].split("\t")[7])
                    if energe < min_energe:
                        min_energe = energe
                        min_index = (i+1) * 4 - 1

                loc_line = lines[min_index].split("\t")
                ss = lines[min_index-2].strip("\n")
                ss1_seq = lines[min_index-3].strip("\n")
                ss2_seq = lines[min_index - 1].strip("\n")
                R1_start, R1_end = loc_line[1], loc_line[2]
                R2_start, R2_end = loc_line[4], loc_line[5]
                ss1_pred_idx = []
                ss1_insert = 0

                for index, value in enumerate(ss):
                    if value == " ":
                        if ss1_seq[index] == "-":
                            ss1_insert += 1
                            continue
                    if value == "|" or value == ":":
                        ss1_pred_idx.append(index - ss1_insert)

                ss2_insert = 0
                ss2_pred_idx = []
                for index, value in enumerate(ss):
                    if value == " ":
                        if ss2_seq[index] == "-":
                            ss2_insert += 1
                            continue
                    if value == "|" or value == ":":
                        ss2_pred_idx.append(index - ss2_insert)

                R1_predict = [p + int(R1_start) for p in ss1_pred_idx]
                R2_predict = [p + int(R2_start) for p in ss2_pred_idx]
                R2_predict = [i for i in reversed(R2_predict)]
                for i in range(len(R1_predict)):
                    R1 = R1_predict[i]
                    R2 = R2_predict[i]
                    predict_pair.append([R1, R2])
    rri_pair = []
    for pair in predict_pair:
        rri_pair.append([pair[0] - 1, pair[1] - 1 + len_seq1])
    # print("predict_pair", predict_pair)
    return rri_pair
