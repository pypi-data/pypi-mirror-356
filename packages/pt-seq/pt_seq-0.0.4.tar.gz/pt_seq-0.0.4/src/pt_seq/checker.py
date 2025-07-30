## check the error mutant info: chain, length, mutant aa seq
# coding = utf - 8
import re
import os
import shutil
import numpy as np
import pandas as pd
import requests
import logging
import h5py
import json
from tqdm import tqdm

from Bio import PDB, SeqIO
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import PPBuilder
from Bio.SeqUtils import seq1
#from Bio.Data.SCOPData import protein_letters_3to1 # deprecated after v1.78

from itertools import permutations
from itertools import chain
from collections import Counter

import matplotlib.pyplot as plt
import seaborn as sns
class error_check:
    def __init__(self, seq_results, ligand, receptor, mutations):
        self.seq_n = seq_results
        self.ligand = [l.strip().upper() for l in ligand.split(',')] if ',' in ligand else [ligand.strip()]
        self.receptor = [r.strip().upper() for r in receptor.split(',')] if ',' in receptor else [receptor.strip()]
        self.chain = self.ligand + self.receptor
        
        if pd.isna(mutations) or mutations in ['', None]: mutations = []  # 沒有 mutation
        elif isinstance(mutations, str):
            mutations = mutations.replace(" ", "").split(',')  # 移除空格

        self.mut_dict = {}
        for mut in mutations:
            parts = mut.split('_')
            
            if len(parts) != 2:
                raise ValueError(f"invalid format {mut}")
            chain = parts[0]
            mut_str = parts[1]

            if len(mut_str) >= 3 and mut_str[1:-1].isdigit():
                og_res = mut_str[0]
                pos = int(mut_str[1:-1])
                new_res = mut_str[-1]
                self.mut_dict[chain] = {'og_res': og_res, 'pos': pos, 'new_res': new_res}
            else:
                self.mut_dict[chain] = {}
                raise ValueError(f"invalid string format: {mut_str}")
        logging.info(self.mut_dict)
        
    def chain_check(self):
        logging.info(self.chain)
        if not all(c in self.seq_n for c in self.chain):
            missing = [c for c in self.chain if c not in self.seq_n]
            logging.info("not all chain")
            return False, f"Chain {','.join(missing)} not found in seq_results"
        return True, None
    
    def len_check(self):
        if not self.mut_dict:
            return True, None

        for chain, info in self.seq_n.items():
            for mut, res in self.mut_dict.items():
                if chain == mut:
                    if len(info['Seq']) < res['pos']:
                        logging.info("seq length < res[pos]")
                        return False, f"Sequence length too short for mutation at position {res['pos']} in chain {chain}"
        return True, None
    
    def aa_check(self):
        for chain, info in self.seq_n.items():
            if self.mut_dict:
                for mut, res in self.mut_dict.items():
                    if chain == mut:
                        if res['og_res'] != info['Seq'][res['pos']-1]:
                            logging.info("wrong res in specified position")
                            return False, f"Original residue {res['og_res']} does not match sequence at position {res['pos']} in chain {chain}"
        return True, None
                
    def chain_loop(self, seq_dict, group, mut_dict):
        seq = []
        for chain in group:
            if chain in mut_dict:
                s_list = list(seq_dict[chain]['Seq'])
                s_list[mut_dict[chain]['pos']-1] = mut_dict[chain]['new_res'] 
                s = ''.join(s_list)
                seq.append(s)
            else:
                s = seq_dict[chain]['Seq']
                seq.append(s)
        seq = ' '.join(seq)
        return seq
    
    def seq_group(self, data_dict):

        # Perform checks
        chain_pass, chain_error = self.chain_check()
        if not chain_pass:
            data_dict['Error'] = chain_error
            data_dict['Reason'] = 'Chain not found in seq_results'
            return pd.DataFrame([data_dict])

        len_pass, len_error = self.len_check()
        if not len_pass:
            data_dict['Error'] = len_error
            data_dict['Reason'] = 'Sequence length is too short'
            return pd.DataFrame([data_dict])

        aa_pass, aa_error = self.aa_check()
        if not aa_pass:
            data_dict['Error'] = aa_error
            data_dict['Reason'] = 'Wrong original residue to mutate'
            return pd.DataFrame([data_dict])

        # If all checks pass, process sequences
        group_1 = self.chain_loop(self.seq_n, self.ligand, self.mut_dict)
        group_2 = self.chain_loop(self.seq_n, self.receptor, self.mut_dict)
        group = '  '.join([group_1, group_2])
        data_dict['seq'] = group
        return pd.DataFrame([data_dict])

