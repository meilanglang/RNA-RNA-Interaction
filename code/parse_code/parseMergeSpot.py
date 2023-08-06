# -*- coding: utf-8 -*-
"""
@Time ： 2023/5/23 11:00
@Auth ： langmei
@File ：parseMergeSpot.py
@IDE ：PyCharm
@Motto: ugly but useful
"""
import os
import numpy as np
import torch


def top_ss(pred_contacts_matrix, seq1_len):
    # print(pred_contacts_matrix.shape)
    L = pred_contacts_matrix.shape[0]
    # out_pred = pred_contacts_matrix[tri_inds]
    # get index of upper triangular matrix from predicted proability LxL matrix
    tri_inds = np.triu_indices(pred_contacts_matrix.shape[0], k=1)
    # get all possible base-pairs in upper triangular matrix
    all_pred_contacts = np.array([[i, j, pred_contacts_matrix[i, j]] for i, j in zip(tri_inds[0], tri_inds[1])])
    # sort all the base-pairs according to probability
    all_pred_contacts_sorted = all_pred_contacts[all_pred_contacts[:, 2].argsort()[::-1]]
    # get top L/2 base-pairs
    pred_pairs = [[int(i[0]), int(i[1])] for i in all_pred_contacts_sorted[0:int(L / 2)]]
    # print("top pair",pred_pairs)
    dbn = [0 for x in range(0, L)]
    for index, value in enumerate(dbn):
        dbn[index] = "."
    # print("ori", dbn)

    predict_pair = []
    for pair in pred_pairs:
        i, j = pair
        if dbn[i] != "(" and dbn[j] != ")":
            dbn[i] = "("
            dbn[j] = ")"
            # print(i, j)
            predict_pair.append(pair)
        else:
            pass
            # print("not the predict pair")

    fin_predict = []
    for pair in predict_pair:
        i, j = pair[0], pair[1]
        if i <= seq1_len and j >= seq1_len + 3:  # +3
            fin_predict.append([i, j])
    return fin_predict


def mergeSpot(f_path_spotrna, f_path_spotrna2, rri_pair, seq1_len):
    pdb = rri_pair[0].split("_")[0]
    chain_1_name = rri_pair[0].split("_")[2]
    chain_2_name = rri_pair[1].split("_")[2]
    fin_spotrna = f_path_spotrna + pdb + "_" + chain_1_name + chain_2_name + ".prob"
    fin_spotrna2 = f_path_spotrna2 + pdb + "_" + chain_1_name + chain_2_name + ".prob"
    # print("prob fin",fin)
    prob_matrix_spotrna = np.loadtxt(fin_spotrna)
    prob_matrix_spotrna2 = np.loadtxt(fin_spotrna2)
    prob_matrix = (prob_matrix_spotrna + prob_matrix_spotrna2) / 2.0
    #prob_matrix = torch.maximum(torch.tensor(prob_matrix_spotrna), torch.tensor(prob_matrix_spotrna2))
    #prob_matrix = prob_matrix.numpy()
    pred_pairs = top_ss(prob_matrix, seq1_len)

    return pred_pairs
