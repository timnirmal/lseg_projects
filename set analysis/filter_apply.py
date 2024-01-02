import pandas as pd
import ast
from tqdm import tqdm

# Load the DataFrame
subseq_df = pd.read_csv('subsequences_with_ids.csv')

# Convert string representations back to their original data types
subseq_df['Subsequence'] = subseq_df['Subsequence'].apply(ast.literal_eval)
subseq_df['LCH_index_Count_List'] = subseq_df['LCH_index_Count_List'].apply(ast.literal_eval)

def process_row(row, df):
    subseq = row['Subsequence']
    updated_count_list = row['LCH_index_Count_List'].copy()

    for longer_index, longer_row in df.iterrows():
        longer_subseq = longer_row['Subsequence']
        if len(longer_subseq) > len(subseq) and all(item in longer_subseq for item in subseq):
            for LCH_index, count in updated_count_list.items():
                if LCH_index in longer_row['LCH_index_Count_List'] and count <= longer_row['LCH_index_Count_List'][LCH_index]:
                    updated_count_list[LCH_index] -= count

    total_count = sum(updated_count_list.values())
    return pd.Series([updated_count_list, total_count], index=['LCH_index_Count_List', 'Count'])

# Apply the function to each row
tqdm.pandas(desc="Processing Rows")
subseq_df[['LCH_index_Count_List', 'Count']] = subseq_df.progress_apply(lambda row: process_row(row, subseq_df), axis=1)

# Save the resulting DataFrame
subseq_df.to_csv('refined_subsequences_2.csv', index=False)
