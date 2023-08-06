# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/12 10:57
@Auth ： langmei
@File ：parse_spotrna.py
@IDE ：PyCharm
@Motto: ugly but useful
"""
import os
import numpy as np

def parse_SPOT_RNA(result_path, rri_pair,seq1_len):
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
                    line_list = lines.split("\t")

                    line_list = list(filter(None, line_list))
                    # print(line_list)
                    base_pair = int(line_list[4])
                    if base_pair == 0:
                        continue
                    else:
                        seq_num = int(line_list[0])
                        if seq_num > base_pair:
                            pass
                        else:
                            predict_pair.append([seq_num-1, int(base_pair-1)])
    rri_predict = []
    chain1_intra = []
    chain_2_intra = []
    for pair in predict_pair:
        i, j = pair[0], pair[1]
        if i < seq1_len and j >= seq1_len:  # +3
            rri_predict.append([i, j])
        if i< seq1_len and j<seq1_len:
            chain1_intra.append([i,j])
        if i > seq1_len and j > seq1_len:
            chain_2_intra.append([i,j])
    #rri_predict.extend()
    return rri_predict

