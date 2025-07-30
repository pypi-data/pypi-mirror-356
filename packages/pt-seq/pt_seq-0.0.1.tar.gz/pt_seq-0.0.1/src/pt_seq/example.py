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

## check the error mutant info: chain, length, mutant aa seq
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