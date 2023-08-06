# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/11 20:06
@Auth ： langmei
@File ：parse_IntaRNA.py
@IDE ：PyCharm
@Motto: ugly but useful
"""


def parse_IntaRNA(result_path, rri_pair, seq1_len):
    predict_pair = []
    pdb_chain = rri_pair[1].split("_")[0] + "_" + rri_pair[0].split("_")[2] + rri_pair[1].split("_")[2]
    IntaRNA_res = result_path + pdb_chain + ".csv"
    # reader = pd.read_csv(IntaRNA_res, sep=";")
    # print(reader)
    # id1;id2;start1;end1;start2;end2;subseqDP;hybridDP
    # target;query;1;8;49;56;GGAUCUUC&GAAGAUUC;((((((((&))))))))
    # index with 1
    with open(IntaRNA_res) as f:
        next(f)
        for line in f.readlines():
            Interaction = line.strip("\n").split(";")
            if len(Interaction) >= 1:
                seq1 = Interaction[7].split("&")[0]
                seq2 = Interaction[7].split("&")[1]
                chain_1_index = Interaction[2]
                chain_2_index = Interaction[4]
                chain_1_list = []
                for index, item in enumerate(seq1, int(chain_1_index)):
                    chain_1_list.append([index, item])
                chain_2_list = []
                for index, item in enumerate(seq2, int(chain_2_index)):
                    chain_2_list.append([index, item])
                # print(chain_1_list, chain_2_list)
                for i in range(0, len(chain_2_list)):
                    chain_pair_tmp = []
                    if chain_2_list[i][1] == ".":
                        continue

                    if chain_2_list[i][1] == ")":
                        count = 0
                        tmp = chain_1_list.pop()
                        while tmp[1] == ".":
                            count = count + 1
                            tmp = chain_1_list.pop()
                        tmp = tmp
                        predict_pair.append([tmp[0], chain_2_list[i][0]])
            else:
                print("no interaction")
    # print("predict_pair", predict_pair)
    fin_pairs = []
    for pair in predict_pair:
        fin_pairs.append([pair[0] - 1, pair[1] - 1 + seq1_len])

    return fin_pairs
