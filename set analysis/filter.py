import pandas as pd
import ast
from tqdm import tqdm  # Import tqdm

# Load the DataFrame
subseq_df = pd.read_csv('subsequences_with_ids.csv')

# Convert string representations back to their original data types
subseq_df['Subsequence'] = subseq_df['Subsequence'].apply(ast.literal_eval)
subseq_df['LCH_index_Count_List'] = subseq_df['LCH_index_Count_List'].apply(ast.literal_eval)

def reduce_subsequence_counts(df):
    # Dictionary to hold updated counts
    updated_counts = {row['Subsequence']: row['LCH_index_Count_List'].copy() for index, row in df.iterrows()}

    # Iterate through the DataFrame with tqdm for a progress bar
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing Rows"):
        subseq = row['Subsequence']
        for longer_index, longer_row in df.iterrows():
            longer_subseq = longer_row['Subsequence']
            if len(longer_subseq) > len(subseq) and all(item in longer_subseq for item in subseq):
                for LCH_index, count in updated_counts[subseq].items():
                    if LCH_index in longer_row['LCH_index_Count_List'] and count <= longer_row['LCH_index_Count_List'][LCH_index]:
                        updated_counts[subseq][LCH_index] -= count

    # Update the DataFrame
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Updating DataFrame"):
        subseq = row['Subsequence']
        df.at[index, 'LCH_index_Count_List'] = updated_counts[subseq]
        df.at[index, 'Count'] = sum(updated_counts[subseq].values())

    return df

# Apply the function to the DataFrame
refined_df = reduce_subsequence_counts(subseq_df)

# Save the resulting DataFrame
refined_df.to_csv('refined_subsequences.csv', index=False)
