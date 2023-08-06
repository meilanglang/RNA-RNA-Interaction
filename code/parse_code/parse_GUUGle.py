# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/11 21:04
@Auth ： langmei
@File ：parse_GUUGle.py
@IDE ：PyCharm
@Motto: ugly but useful
"""
import os


def parse_GUUGle(result_path, rri_pair, len_seq1):
    """
    # index with 1
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

    predict_file = result_path + pdb + "_" + chain_1_name + chain_2_name + '.txt'
    # print("predicted file", predict_file)
    if os.path.exists(predict_file):
        chain_1_pair_l = []
        chain_2_pair_l = []
        with open(predict_file) as f:
            lines = f.readlines()
            if len(lines) > 5:
                loc = lines[5].split(" ")
                pair_num = int(loc[1])
                loc_chain_a = int(loc[4])
                loc_chain_b = int(loc[8])
                for i in range(0, pair_num):
                    chain_1_pair_l.append(loc_chain_a + i)
                    chain_2_pair_l.append(loc_chain_b + i)
        chain_2_pair_l.reverse()
        for i in range(0, len(chain_1_pair_l)):
            pair = [chain_1_pair_l[i], chain_2_pair_l[i]]
            predict_pair.append(pair)

        # print(predict_pair)
    else:
        print("no structure")
    rri_pair = []
    #print("l1,l2 len",predict_pair)
    for pair in predict_pair:
        rri_pair.append([pair[0] - 1, pair[1] -1 + len_seq1])
    #print(rri_pair)

    return rri_pair
