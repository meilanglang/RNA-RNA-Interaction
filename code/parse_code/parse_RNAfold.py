# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/14 0:08
@Auth ： langmei
@File ：parse_RNAfold.py
@IDE ：PyCharm
@Motto: ugly but useful
"""
def parse_RNAfold(result_path, rri_pair,len_seq1):
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    # print("pdb",pdb)
    with open(result_path + pdb + "_" + chain_1_name + chain_2_name + '.fold') as f:
        all_ss = f.readlines()[2].strip("\n")
        # print("all ss", all_ss)
        stack = []
        pairs = []
        for idx, v in enumerate(all_ss):
            if v == ".":
                pass
            if v == "(":
                stack.append(idx)
                continue
            if v == ")":
                i = stack.pop()
                j = idx
                pairs.append([i, j])
    rri_pairs = []
    # print(pairs)
    for pair in pairs:
        if pair[0] < len_seq1 and pair[1] >= len_seq1 + 3:
            rri_pairs.append(pair)
    return rri_pairs

def parse_RNAfold_intra(result_path, rri_pair,len_seq1):
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    # print("pdb",pdb)
    with open(result_path + pdb + "_" + chain_1_name + chain_2_name + '.fold') as f:
        all_ss = f.readlines()[2].strip("\n")
        # print("all ss", all_ss)
        stack = []
        pairs = []
        for idx, v in enumerate(all_ss):
            if v == ".":
                pass
            if v == "(":
                stack.append(idx)
                continue
            if v == ")":
                i = stack.pop()
                j = idx
                pairs.append([i, j])
    rri_pairs = []
    # print(pairs)
    chain1_pair = []
    chain2_pair = []
    for pair in pairs:
        i,j = pair[0], pair[1]
        if i < len_seq1 and j>= len_seq1:
            rri_pairs.append(pair)
        if i < len_seq1 and j < len_seq1:
            chain1_pair.append([i, j])
        if i > len_seq1 and j > len_seq1:
            chain2_pair.append([i - len_seq1, j - len_seq1])
    return chain1_pair, chain2_pair

