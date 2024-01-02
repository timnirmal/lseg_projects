import pandas as pd
import ast
import dask.dataframe as dd
from dask.diagnostics import ProgressBar

def str_to_dict(s):
    if isinstance(s, str):
        try:
            return ast.literal_eval(s)
        except (ValueError, SyntaxError):
            return {}
    return s

def reduce_subsequence_counts(row, df):
    subseq = row['Subsequence']
    updated_count = str_to_dict(row['LCH_index_Count_List']).copy()

    for longer_index, longer_row in df.iterrows():
        longer_subseq = longer_row['Subsequence']
        if len(longer_subseq) > len(subseq) and all(item in longer_subseq for item in subseq):
            for LCH_index, count in updated_count.items():
                if LCH_index in longer_row['LCH_index_Count_List'] and count <= longer_row['LCH_index_Count_List'][LCH_index]:
                    updated_count[LCH_index] -= count

    total_count = sum(updated_count.values())
    return updated_count, total_count

# Load the DataFrame
subseq_df = pd.read_csv('subsequences_with_ids.csv')

# Convert string representations back to their original data types
subseq_df['Subsequence'] = subseq_df['Subsequence'].apply(ast.literal_eval)
subseq_df['LCH_index_Count_List'] = subseq_df['LCH_index_Count_List'].apply(str_to_dict)

# Convert to Dask DataFrame
dask_df = dd.from_pandas(subseq_df, npartitions=10)  # Adjust 'npartitions' based on your system's capabilities

# Define a meta structure for the result
meta = {'LCH_index_Count_List': 'object', 'Count': 'int'}

# Apply the function with Dask
with ProgressBar():
    result = dask_df.apply(lambda x: reduce_subsequence_counts(x, subseq_df), axis=1, result_type='expand', meta=meta).compute()

# Combine the result with the original DataFrame
subseq_df[['LCH_index_Count_List', 'Count']] = result

# Save the resulting DataFrame
subseq_df.to_csv('refined_subsequences_dask.csv', index=False)
