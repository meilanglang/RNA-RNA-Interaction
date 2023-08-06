# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/16 16:38
@Auth ： langmei
@File ：parse_ufold.py
@IDE ：PyCharm
@Motto: ugly but useful
"""


def parse_UFold(result_path, rri_pair,len_seq1):
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    # print("pdb",pdb)
    path = result_path + pdb + "_" + chain_1_name + chain_2_name + '.ct'
    pairs = []
    with open(path) as f:
        next(f)
        for lines in f:
            #print(lines)
            line_list = lines.split("\t")

            line_list = list(filter(None, line_list))
            base_pair = int(line_list[4]) -1
            if base_pair == 0:
                continue
            else:
                tmp = []
                seq_num = int(line_list[2])
                # print(seq_num)
                if seq_num > base_pair:
                    pass
                else:
                    tmp.append(seq_num)
                    tmp.append(base_pair)
                    pairs.append(tmp)

    rri_pairs = []
    # print(pairs)
    for pair in pairs:
        if pair[0] < len_seq1 and pair[1] >= len_seq1 + 3:
            rri_pairs.append(pair)
    return rri_pairs

def parse_UFold_intra(result_path, rri_pair,len_seq1):
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    # print("pdb",pdb)
    path = result_path + pdb + "_" + chain_1_name + chain_2_name + '.ct'
    pairs = []
    with open(path) as f:
        next(f)
        for lines in f:
            #print(lines)
            line_list = lines.split("\t")

            line_list = list(filter(None, line_list))
            base_pair = int(line_list[4]) -1
            if base_pair == 0:
                continue
            else:
                tmp = []
                seq_num = int(line_list[2])
                # print(seq_num)
                if seq_num > base_pair:
                    pass
                else:
                    tmp.append(seq_num)
                    tmp.append(base_pair)
                    pairs.append(tmp)

    rri_pairs = []
    chain1_pair = []
    chain2_pair = []
    for pair in pairs:
        i, j = pair[0], pair[1]
        if i < len_seq1 and j >= len_seq1:
            rri_pairs.append(pair)
        if i < len_seq1 and j < len_seq1:
            chain1_pair.append([i, j])
        if i > len_seq1 and j > len_seq1:
            chain2_pair.append([i - len_seq1, j - len_seq1])
    return chain1_pair, chain2_pair

