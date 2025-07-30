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
from .processor import ProteinNSeq
from .checker import error_check

def process_row(row):
    print(f"This is row {row.name}")
    pdb_id = row['PDB']
    source = row['Source Data Set']
    ppb_file = f'PPB Affinity/PDB/{source}/{pdb_id}.pdb'
    ligand = row['Ligand Chains']
    receptor = row['Receptor Chains']
    method = row['Affinity Method']
    subgroup = row['Subgroup']

    # Initialize error dictionary for this row
    data_dict = {
        'source': source, 
        'PDB': pdb_id,
        "Subgroup": subgroup,
        "Affinity": None,
        "Temperature(K)": None,
        "Method": method,
        'Complex group name': None,
        'Error': None,
        'Reason': None,
        "seq": None
    }

    # Validate PDB file existence
    if not os.path.exists(ppb_file):
        print(f"PDB file not found: {ppb_file}")
        data_dict['Error'] = f"PDB file not found: {ppb_file}"
        data_dict['Reason'] = 'Missing base PDB file'
        return pd.DataFrame([data_dict])

    # Process mutation
    mutation = row['Mutations']
    mut = 'wt' if pd.isna(mutation) or mutation in ['', 'nan'] else 'mut'

    # Process temperature
    temp = row['Temperature(K)']
    try:
        temp = float(298.0) if pd.isna(temp) or str(temp).strip() == '298(assumed)' else float(re.sub(r'[^\d.]', '', str(temp)))
        data_dict['Temperature(K)'] = temp
    except ValueError:
        print(f"Invalid temperature value: {temp}")
        data_dict['Error'] = f"Invalid temperature value type: {temp}"
        data_dict['Reason'] = 'Wrong type(temp)'
        return pd.DataFrame([data_dict])
    
    # Process affinity (KD)
    kd = row['KD(M)']
    if pd.isna(kd) or kd <= 0:
        print(f"Invalid KD value: {kd}")
        data_dict['Error'] = f"Invalid KD value: {kd}"
        data_dict['Reason'] = 'Invalid KD value'
        return pd.DataFrame([data_dict])
    bind = np.log(kd) * 8.314 * temp / 1000 / 4.18  # Calculate binding energy in kcal/mol
    data_dict['Affinity'] = bind  # Update affinity in error_dict

    # Process sequence data
    try:
        processor = ProteinNSeq(mut, pdb_id, pdb_file=ppb_file, d_dir=f'PPB Affinity/PDB/{source}/seq')
        results = processor.main_n_s(name='T', pdb='F')
        if not results:
            print(f"Failed to get sequence dictionary for PDB: {pdb_id}")
            data_dict['Error'] = f"Failed to get sequence dictionary for PDB: {pdb_id}"
            data_dict['Reason'] = 'Failed to get the dict (PDB name may change)'
            return pd.DataFrame([data_dict])
        
    except Exception as e:
        print(f"ProteinNSeq processing failed for PDB {pdb_id}: {str(e)}")
        data_dict['Error'] = f"ProteinNSeq processing failed: {str(e)}"
        data_dict['Reason'] = 'Wrong in Processing seq dict'
        return pd.DataFrame([data_dict])

    # Generate sequence and complex group
    check = error_check(results, ligand, receptor, mutation)
    seq_df = check.seq_group(data_dict)  # Pass the entire row to seq_group
    if seq_df['Error'].iloc[0] is not None:
        return seq_df  # Return error DataFrame
    return seq_df