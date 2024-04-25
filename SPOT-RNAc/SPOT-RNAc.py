# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/7 15:37
@Auth ： langmei
@File ：predict.py
@IDE ：PyCharm
@Motto: ugly but useful
"""
import os
import sys
import argparse
from Bio import SeqIO
import numpy as np


def read_fasta(f_fasta):
    for r in SeqIO.parse(f_fasta, "fasta"):
        seq = str(r.seq)
        id = r.id
    return id, seq


def write_fasta(path, id, seq):
    with open(os.path.join(path, id + ".fasta"), "w") as f:
        f.write(">" + id + "\n")
        f.write(seq + "\n")


def check_file_exist(path):
    if os.path.exists(path):
        print("the path exists")
    else:
        os.makedirs(path)


def concatenate_seq(f_fasta_1, f_fasta_2):
    id1, seq1 = read_fasta(f_fasta_1)
    id2, seq2 = read_fasta(f_fasta_2)

    rri_id = id1 + ":" + id2
    seq_AB = seq1 + seq2
    seq_BA = seq2 + seq1

    ab_path = os.path.join(spot_rna_input, "AB")
    ba_path = os.path.join(spot_rna_input, "BA")

    check_file_exist(ab_path)
    check_file_exist(ba_path)

    write_fasta(ab_path, rri_id, seq_AB)
    write_fasta(ba_path, rri_id, seq_BA)

    return seq1, seq2, rri_id


def check_spotrna_input(path):
    if os.path.exists(path):
        print("the concatenate file {} exists".format(path))
    else:
        print("the concatenate file {} not exist please check".format(path))


def check_spotrna_output(path):
    if os.path.exists(path):
        print("SPOT-RNA  output {} success !!!".format(path))
    else:
        print("SPOT-RNA failed, please check".format(path))


def run_spotrna(input_fa, out_path, device, ncpu):
    # SPOT-RNA Usage:
    # python3 SPOT-RNA.py  --inputs sample_inputs/single_seq.fasta  --outputs 'outputs/'  --cpu 32
    # python3 SPOT-RNA.py  --inputs sample_inputs/batch_seq.fasta  --outputs 'outputs/' --gpu 0
    if os.path.exists(out_path):
        pass
    else:
        os.makedirs(out_path)
    if os.path.exists(input_fa):
        cmd = f"python3 SPOT-RNA.py  --inputs {input_fa}  --outputs {out_path}  --{device} {ncpu}"
        os.system(cmd)
    else:
        print("the input not exists, please check the spot-rna input")


def parse_spotrna(result_path, rri_id, seq1_len):
    predict_pair = []
    seqs = []
    predict_file = result_path + rri_id + ".ct"
    print(predict_file)
    # if os.path.exists(predict_file):
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
                        predict_pair.append([seq_num - 1, int(base_pair - 1)])
    rri_predict = []
    for pair in predict_pair:
        i, j = pair[0], pair[1]
        if i < seq1_len and j >= seq1_len:  # +3
            rri_predict.append([i, j])
    return rri_predict


def transBA2AB(predictBA, len_seq1, len_seq2):
    predict_pair = []
    for pair in predictBA:
        i, j = pair[0], pair[1]
        new_j = i + len_seq1
        new_i = j - len_seq2
        predict_pair.append([new_i, new_j])
    return predict_pair
    # print("trains_predict_BA:", predict_pair)


def MergeAB(predictAB, predictBA, len_seq1, len_seq2):
    trains_predict_BA = transBA2AB(predictBA, len_seq1, len_seq2)
    predictAB.extend(trains_predict_BA)
    predict_pair = []
    for i in predictAB:
        if predictAB.count(i) >= 1:
            if i not in predict_pair:
                predict_pair.append(i)
    return predict_pair


def pair2dbn(predict_pair, seq1, seq2, rri_outputs):
    seq1_len = len(seq1)
    seq2_len = len(seq2)

    dbn = ['.'] * (seq1_len + seq2_len)
    for pair in predict_pair:
        if dbn[pair[0]] == "." and dbn[pair[1]] == ".":
            dbn[pair[0]] = '('
            dbn[pair[1]] = ')'
    dbn.insert(seq1_len, "&")

    seq = []
    for s in seq1:
        seq.append(s)
    for s in seq2:
        seq.append(s)
    seq.insert(seq1_len, "&")

    row1 = np.array(seq)
    row2 = np.array(dbn)
    print(row1)
    print(row2)
    temp = np.vstack((row1, row2))

    np.savetxt(os.path.join(rri_outputs, rri_id + '.dbn'), temp, delimiter='', fmt="%s",
               header='>' + 'SPOT-RNAc RNA-RNA-Interaction', comments='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--I1', default='inputs/seq_1/6XJQ_A.fasta', type=str, metavar='')
    parser.add_argument('--I2', default='inputs/seq_2/6XJQ_A.fasta', type=str, metavar='')
    parser.add_argument("--device", type=str,default="cpu", metavar='')
    parser.add_argument("--ncpu", type=int, metavar='')
    parser.add_argument('--outputs', default='outputs/', type=str,
                        help='Path to output files; SPOT-RNAc outputs at least three files .ct, .bpseq, and .prob files; default = ''outputs/\n',
                        metavar='')
    args = parser.parse_args()

    spot_rna_input = os.path.join(args.outputs, "spotrna_input")
    spot_rna_output = os.path.join(args.outputs, "spotrna_ouput")
    rri_output = os.path.join(args.outputs, "rri_output")

    seq1, seq2, rri_id = concatenate_seq(args.I1, args.I2)
    ab_input_fa = os.path.join(spot_rna_input, "AB/{}.fasta".format(rri_id))
    ba_input_fa = os.path.join(spot_rna_input, "BA/{}.fasta".format(rri_id))

    print("the concatenate file of AB is {}".format(ab_input_fa))
    print("the concatenate file of BA is {}".format(ba_input_fa))

    check_spotrna_input(ab_input_fa)
    check_spotrna_input(ba_input_fa)

    check_file_exist(ab_input_fa)
    check_file_exist(ba_input_fa)

    ab_output_fa = os.path.join(spot_rna_output, "AB/{}/".format(rri_id))
    ba_output_fa = os.path.join(spot_rna_output, "BA/{}/".format(rri_id))

    print(ab_output_fa)
    print(ba_output_fa)

    check_file_exist(ab_output_fa)
    check_file_exist(ba_output_fa)

    run_spotrna(ab_input_fa,ab_output_fa,args.job_name,args.ncpu)
    run_spotrna(ba_input_fa, ba_output_fa, args.job_name, args.ncpu)
    print(os.path.join(ab_output_fa, "{}.ct".format(rri_id)))

    # if os.path.exists(os.path.join(ab_output_fa,"/{}.ct".format(rri_id))) and os.path.exists(os.path.join(ba_output_fa,"/{}.ct".format(rri_id))):

    pred_AB = parse_spotrna(ab_output_fa, rri_id, len(seq1))
    pred_BA = parse_spotrna(ba_output_fa, rri_id, len(seq2))
    print(pred_AB)
    print(pred_BA)
    predict_pair = MergeAB(pred_AB, pred_BA, len(seq1), len(seq2))
    print(predict_pair)

    check_file_exist(rri_output)
    pair2dbn(predict_pair, seq1, seq2, rri_output)



