# process_row
import pt-seq
or_df = pd.read_csv('PPB-Affinity.csv')
for idx, row in tqdm(or_df.iterrows(), total=len(or_df), desc="Processing rows (get seq)"):
    result_df = process_row(row)

