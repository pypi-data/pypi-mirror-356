# process_row
from pt_seq.utils import process_row
import pandas as pd
import logging
import tqdm

# Configure logging
logging.basicConfig(
    filename='0620HW.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

or_df = pd.read_csv('test.csv')
for idx, row in tqdm(or_df.iterrows(), total=len(or_df), desc="Processing rows (get seq)"):
    result_df = process_row(row)

