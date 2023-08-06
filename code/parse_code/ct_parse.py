# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/11 19:42
@Auth ： langmei
@File ：ct_parse.py
@IDE ：PyCharm
@Motto: ugly but useful
"""
import os


def parse_ct(result_path, rri_pair,seq1_len):
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    seqs = []
    predict_file = result_path + pdb + "_" + chain_1_name + chain_2_name + ".ct"
    if os.path.exists(predict_file):
        with open(predict_file) as f:
            for line in f:
                next(f)
                for lines in f:
                    line_list = lines.split(" ")
                    line_list = list(filter(None, line_list))
                    # print(line_list)
                    base_pair = int(line_list[4])
                    if base_pair == 0:
                        continue
                    else:
                        tmp = []
                        seq_num = int(line_list[0])
                        # print(seq_num)
                        if seq_num > base_pair:
                            pass
                        else:
                            predict_pair.append([seq_num-1, int(base_pair-1)])
    fin_predict = []
    for pair in predict_pair:
        i, j = pair[0], pair[1]
        if i <= seq1_len and j >= seq1_len + 3:  # +3
            fin_predict.append([i, j])
    return fin_predict
