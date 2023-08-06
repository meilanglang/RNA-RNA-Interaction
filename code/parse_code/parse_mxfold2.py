# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/16 16:25
@Auth ： langmei
@File ：parse_mxfold2.py
@IDE ：PyCharm
@Motto: ugly but useful
"""

def parse_MXfold2(result_path, rri_pair,len_seq1):
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    # print("pdb",pdb)
    f = open(result_path + pdb + "_" + chain_1_name + chain_2_name + '.out')
    for index, line in enumerate(f):
        if index == 2:
            line = line.split(" ")[0].strip("\n")
            line = list(line)
            #print(line)
            pred_pair = []
            tmp_list = []
            for index, dot in enumerate(line):
                if dot == "(":
                    tmp_list.append([index, dot])
                if dot == ")":
                    right_pair = tmp_list.pop()
                    pair = [right_pair[0], index]
                    pred_pair.append(pair)
            #print(pred_pair)
    rri_pairs = []
    # print(pairs)
    for pair in pred_pair:
        if pair[0] < len_seq1 and pair[1] >= len_seq1 + 3:
            rri_pairs.append(pair)

    return rri_pairs

def parse_MXfold2_intra(result_path, rri_pair,len_seq1):
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    # print("pdb",pdb)
    f = open(result_path + pdb + "_" + chain_1_name + chain_2_name + '.out')
    for index, line in enumerate(f):
        if index == 2:
            line = line.split(" ")[0].strip("\n")
            line = list(line)
            #print(line)
            pred_pair = []
            tmp_list = []
            for index, dot in enumerate(line):
                if dot == "(":
                    tmp_list.append([index, dot])
                if dot == ")":
                    right_pair = tmp_list.pop()
                    pair = [right_pair[0], index]
                    pred_pair.append(pair)
            #print(pred_pair)
    rri_pairs = []
    chain1_pair = []
    chain2_pair = []
    for pair in pred_pair:
        i, j = pair[0], pair[1]
        if i < len_seq1 and j >= len_seq1:
            rri_pairs.append(pair)
        if i < len_seq1 and j < len_seq1:
            chain1_pair.append([i, j])
        if i > len_seq1 and j > len_seq1:
            chain2_pair.append([i - len_seq1, j - len_seq1])
    return chain1_pair, chain2_pair