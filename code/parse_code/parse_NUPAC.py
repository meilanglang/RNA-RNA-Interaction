# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/13 15:08
@Auth ： langmei
@File ：parse_NUPAC.py
@IDE ：PyCharm
@Motto: ugly but useful
"""

def parse_NUPAC(result_path, rri_pair):
    """
    no linker between two chain
    Args:
        result_path:
        rri_pair:

    Returns:

    """
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    #print("pdb",pdb)
    with open(result_path + pdb + "_" + chain_1_name + chain_2_name + '.txt') as f:
        ss = f.readlines()[0].strip("\n")
        ss1 = ss.split("+")[0]

        ss2 = ss.split("+")[1]
        all_ss = ss1 + ss2
        #print("all ss", all_ss)
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
    return rri_pairs