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
def add_one(number):
    return number + 1

class ProteinNSeq:
    """用於處理 PDB 文件的類，提供提取蛋白質名稱、序列和比較功能。"""
    
    def __init__(self, mut, pdb_id, pdb_file=None, d_dir="pdb_files"):
        """
        pdb_file: base pdb file
        d_dir: saving dir for download file
        """
        self.mut = mut
        self.pdb_id = pdb_id
        self.pdb_file = pdb_file 
        self.d_dir = d_dir
        self.rcsb_pdb = os.path.join(d_dir, f"{self.pdb_id}.pdb")
        self.pdbe_file = os.path.join(self.d_dir, f"pdbe_{self.pdb_id}.fasta")
        self.pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        self.pdbe_url = f"https://www.ebi.ac.uk/pdbe/entry/pdb/{pdb_id.lower()}/fasta"

    def d_s_pdb(self):
        
        # check if including SEQRES inside pdb ifle
        if os.path.exists(self.pdb_file):
            with open(self.pdb_file, 'r') as f:
                pdb_content = f.read()
            if "SEQRES" in pdb_content:
                #print(f"PDB file {self.pdb_file} already exists and contains SEQRES.")
                return self.pdb_file
            else:
                if os.path.exists(self.rcsb_pdb):
                    return self.rcsb_pdb
                logging.info(f"Existing file {self.rcsb_pdb} is missing SEQRES, re-downloading...")

        # download pdb file
        try:
            response = requests.get(self.pdb_url) 
            if response.status_code != 200:
                logging.info(f"Cannot download pdb file: {self.pdb_id} (status: {response.status_code})")
                return None
            
            if not os.path.exists(self.d_dir):
                os.makedirs(self.d_dir)
            pdb_content = response.text
            
            # save file
            rcsb_pdb = os.path.join(self.d_dir, f"{self.pdb_id}.pdb")
            with open(rcsb_pdb, 'w') as f: 
                f.write(pdb_content)
            
            logging.info(f"PDB has been downloaded and saved to {rcsb_pdb}")
            return rcsb_pdb

        except requests.RequestException as e:
            logging.info(f"\033[91mDownload failed for {self.pdb_id}: {e}\033[0m")
            return None

    def d_s_pdbe(self):
        if os.path.exists(self.pdbe_file):
            return self.pdbe_file        
        
        # download pdbe file
        try:
            response = requests.get(self.pdbe_url)  
            if response.status_code != 200:
                logging.info(f"Cannot download pdb file: {self.pdb_id} (status: {response.status_code})")
                return None
                
            if not os.path.exists(self.d_dir):
                os.makedirs(self.d_dir)        
            
            seq_content = response.text
            
            with open(self.pdbe_file, 'w') as f:
                f.write(seq_content)
            logging.info(f"PDBe fasta file has been downloaded and saved to {self.pdbe_file}")
        
        except requests.RequestException as e:
            logging.info(f"\033[91mDownload failed for {self.pdb_id}: {e}\033[0m")
            return None
        return self.pdbe_file

    def get_s(self, mut, pdb):
        seq_results = {}  # seq_results[chain] = {'Seq': None, 'Name': 'Unknown'}

        if mut == 'wt':
            if pdb =='F':
                try:
                    pdbe = self.d_s_pdbe()
                    logging.info('using pdbe_file')
                    with open(pdbe, "r") as handle:
                        for record in SeqIO.parse(handle, "fasta"):
                            # 假設描述行格式為 >pdb|1a22|A
                            if record.description.startswith('pdb|'):
                                parts = record.description.split('|')
                                if len(parts) >= 3:
                                    chains = parts[2].strip().split()
                                    seq = str(record.seq)
                                    for chain in chains:
                                        seq_results[chain] = {'Seq': seq, 'Name': 'Unknown'}
                                else:
                                    logging.info(f"Invalid FASTA header format: {record.description}")
                except Exception as e:
                    logging.info(f"\033[91mError parsing seq from {pdbe}: {e}\033[0m")
            
            else:
                try:
                    logging.info('using rcsb file')
                    rcsb_file = self.d_s_pdb()
                    with open(rcsb_file, "r") as handle:
                        for record in SeqIO.parse(handle, "pdb-seqres"):
                            chain_id = record.annotations["chain"]
                            seq_results[chain_id] = {'Seq': str(record.seq), 'Name': 'Unknown'}
                except Exception as e:
                    logging.info(f"\033[91mError parsing SEQRES from {rcsb_file}: {e}\033[0m")         
                    
        else:                
            try:
                logging.info('using base pdb file')
                parser = PDBParser(QUIET=True)
                structure = parser.get_structure('protein', self.pdb_file)
                for chain in structure[0]:  # Use first model
                    chain_id = chain.id
                    sequence = ''
                    for residue in chain:
                        resname = residue.get_resname()
                        try:
                            sequence += seq1(resname)
                        except KeyError:
                            continue  # 忽略非標準胺基酸
                    seq_results[chain_id] = {'Seq': sequence, 'Name': 'Unknown'}
                    
            except Exception as e:
                logging.info(f"\033[91mError parsing ATOM from {self.pdb_file}: {e}\033[0m")
        return seq_results


    def get_n(self, seq_results):
        """Extract molecule names for specified chains from PDB file."""

        try:
            rcsb_file = self.d_s_pdb()            
            parser = PDBParser(QUIET=True)
            structure = parser.get_structure(self.pdb_id, rcsb_file)
            compound = structure.header.get("compound", {})
            
            for chain_id in seq_results:
                for mol_id, info in compound.items():
                    chains = [c.strip().upper() for c in info.get("chain", "").split(",") if c.strip()]
                    if chain_id in chains:
                        seq_results[chain_id]['Name'] = info.get("molecule", "Unknown")
                        break  # Stop after first match
        except Exception as e:
            logging.info(f"\033[91mError extracting molecule names from {rcsb_file}: {e}\033[0m")
        
        return seq_results

    def main_n_s(self, name='T', pdb='T'):
        """Main method to extract sequences and names from PDB file."""
        seq_results = {}  # Initialize empty result dictionary
        
        try:
            if not os.path.exists(self.pdb_file):
                logging.info(f"\033[91mError: PDB file {self.pdb_file} does not exist\033[0m")
                return seq_results

            seq_results = self.get_s(self.mut, pdb)
            
            if name == 'T':
                seq_results = self.get_n(seq_results)
            
            logging.info(self.pdb_id)
            logging.info(seq_results)
            return seq_results
        
        except AttributeError as e:
            logging.info(f"\033[91mError: Missing attribute (e.g., pdb_id, mut, or mut_file): {e}\033[0m")
        
        except Exception as e:
            logging.info(f"\033[91mFailed to process PDB file: {e}\033[0m")
        
        return seq_results   

