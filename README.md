#  Deep learning models of RNA base-pairing structures generalize to unseen folds and make accurate zero-shot predictions of base-base interactions of RNA complexes

## Introduction

The intricate network of RNA-RNA interactions, crucial for orchestrating essential cellular processes like transcriptional and translational regulation, has been unveiling through high-throughput techniques and computational predictions. With the emergence of deep learning methodologies, the question arises: how do these cutting-edge techniques for base-pairing prediction compare to traditional free-energy-based approaches, particularly when applied to the challenging domain of interaction prediction via chain concatenation? In this study, we employ base pairs derived from three-dimensional RNA complex structures as the gold standard benchmark to assess the performance of 23 different methods, including recently developed deep learning models. Our results demonstrate that the deep-learning-based methods, SPOT-RNA can be generalized to previously unseen RNA structures and are capable of making accurate zero-shot predictions of RNA-RNA interactions.

## Results

![image text](https://github.com/meilanglang/RNA-RNA-Interaction/blob/master/analysis/Fig1.png  "SPOT-RNAc Performance Comparison")

## Pre-requisites

 [Python3](https://docs.python-guide.org/starting/install3/linux/)

[Biopython](https://biopython.org/wiki/Download)

[SPOT-RNA](https://github.com/jaswindersingh2/SPOT-RNA)

## Usage

cd SPOT-RNAc

python3  SPOT-RNAc.py --I1 inputs/seq_1/6XJQ_A.fasta --I2 inputs/seq_2/6XJQ_A.fasta --device cpu --ncpu 4  --output outputs

## DataSets

**The following data is 64 RNA-RNA interaction pairs:**

RNA-RNA-Interaction_DataSet_64.csv 

**The following data is 34 RNA-RNA interaction pairs that it`s Not Match Rfam family:**

RNA-RNA_Interaction_Not_Match_rfam_23.csv 

## Contact

langmei@szbl.ac.cn;zhouyq@szbl.ac.cn











