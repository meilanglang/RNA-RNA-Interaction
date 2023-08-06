# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/11 20:18
@Auth ： langmei
@File ：parse_PairFold.py
@IDE ：PyCharm
@Motto: ugly but useful
"""

def parse_PairFold(result_path,rri_pair):
    """

    Args:
        result_path:
        rri_pair:

    Returns:
        No linker

    """
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    seqs = []
    f = result_path + pdb + "_" + chain_1_name + chain_2_name + ".txt"
    #f = result_path + pdb_chain + ".txt"

    with open(f, "r") as f:
        lines = f.readlines()
        seq = lines[0]
        ss = lines[1].split(":")[1].split(" ")
        ss1 = ss[1]
        ss2 = ss[2]
        all_ss = ss1 + ss2
        #print("all ss",all_ss)
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
        if pair[0] < len(ss1) and pair[1] >= len(ss1):
            rri_pairs.append(pair)
    # print(rri_pairs)
    return rri_pairs


def parse_PairFold_intra(result_path,rri_pair):
    """

    Args:
        result_path:
        rri_pair:

    Returns:
        No linker

    """
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    seqs = []
    f = result_path + pdb + "_" + chain_1_name + chain_2_name + ".txt"
    #f = result_path + pdb_chain + ".txt"

    with open(f, "r") as f:
        lines = f.readlines()
        seq = lines[0]
        ss = lines[1].split(":")[1].split(" ")
        ss1 = ss[1]
        ss2 = ss[2]
        all_ss = ss1 + ss2
        #print("all ss",all_ss)
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
    chain1_pair = []
    chain2_pair = []
    # print(pairs)
    for pair in pairs:
        if pair[0] < len(ss1) and pair[1] >= len(ss1):
            rri_pairs.append(pair)
        if pair[0] < len(ss1) and pair[1] < len(ss1):
            chain1_pair.append(pair)

        if pair[0] > len(ss1) and pair[1] > len(ss1):
            chain2_pair.append(pair)
    # print(rri_pairs)
    chain2_pair = [[i-len(ss1),j-len(ss1)] for i,j in chain2_pair]
    return chain1_pair, chain2_pair
