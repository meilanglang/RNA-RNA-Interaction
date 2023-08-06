# -*- coding: utf-8 -*-
"""
@Time ： 2023/5/5 16:04
@Auth ： langmei
@File ：parse_PETcoFold.py
@IDE ：PyCharm
@Motto: ugly but useful
"""


# Intermolecular RNA structure

def parse_PETcoFold(result_path, rri_pair):
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
    stack = []
    pairs = []
    with open(result_path + pdb + "_" + chain_1_name + chain_2_name + '.txt') as f:
        lines = f.readlines()
        if len(lines) <= 1:
            print("no structure")
        else:
            for line in lines:
                if "Intermolecular RNA structure" in line:
                    #line = line.replace(" ","")
                    ss = line.split(":")[1].lstrip()
                    print(ss)
                    ss1 = ss.split("&")[0]

                    ss2 = ss.split("&")[1]
                    all_ss = ss1 + ss2
                    # print("all ss", all_ss)
                    print(len(ss1), len(ss2))

                    for idx, v in enumerate(all_ss):
                        if v == "." or v == "-":
                            pass
                        if v == "[":
                            stack.append(idx)
                            continue
                        if v == "]":
                            i = stack.pop()
                            j = idx
                            pairs.append([i, j])
    rri_pairs = []
    # print(pairs)
    for pair in pairs:
        if pair[0] < len(ss1) and pair[1] >= len(ss1):
            rri_pairs.append(pair)
    return rri_pairs

def parse_PETcoFold_intra(result_path, rri_pair):
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
    brace_stack = []
    roundBro_stack= []
    pairs = []
    with open(result_path + pdb + "_" + chain_1_name + chain_2_name + '.txt') as f:
        lines = f.readlines()
        if len(lines) <= 1:
            print("no structure")
        else:
            for line in lines:
                if "PETcofold RNA structure:" in line:
                    #line = line.replace(" ","")
                    ss = line.split(":")[1].lstrip()
                    print(ss)
                    ss1 = ss.split("&")[0]

                    ss2 = ss.split("&")[1]
                    all_ss = ss1 + ss2
                    # print("all ss", all_ss)
                    print(len(ss1), len(ss2))
                    #left = ["{","["]
                    #right = [""]
                    pass_dot = [".","-","[","]"]
                    for idx, v in enumerate(all_ss):
                        if v in pass_dot:
                            continue
                        if v == "{":
                            brace_stack.append(idx)
                            continue
                        if v == "(":
                            roundBro_stack.append(idx)
                        if v == "}":
                            i = brace_stack.pop()
                            j = idx
                            pairs.append([i, j])

                        if v == ")":
                            i = roundBro_stack.pop()
                            j = idx
                            pairs.append([i, j])

    rri_pairs = []
    # print(pairs)
    for pair in pairs:
        if pair[0] < len(ss1) and pair[1] >= len(ss1):
            rri_pairs.append(pair)
    chain1_pair = [pair for pair in pairs if pair[0] < len(ss1) and pair[1] < len(ss1)]
    chain2_pair = [pair for pair in pairs if pair[0] >= len(ss1) and pair[1] >= len(ss1)]
    chain2_pair = [[i - len(ss1), j - len(ss1)] for i, j in chain2_pair]
    print(chain2_pair)
    return chain1_pair, chain2_pair
