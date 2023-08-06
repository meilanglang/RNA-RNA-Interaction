# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/30 15:32
@Auth ： langmei
@File ：parseSpotProb.py
@IDE ：PyCharm
@Motto: ugly but useful
"""
import os
import numpy as np

def parseSpotProb(result_path, rri_pair,seq1_len):
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    predict_pair = []
    seqs = []
    predict_file = result_path + pdb + "_" + chain_1_name + chain_2_name + ".prob"
    prob_matrix = np.loadtxt(predict_file)
    return prob_matrix