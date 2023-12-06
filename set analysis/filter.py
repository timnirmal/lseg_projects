import pandas as pd

subseq_df = pd.read_csv('subsequences_with_ids.csv')

# Convert string representation of tuples back to actual tuples
subseq_df['Subsequence'] = subseq_df['Subsequence'].apply(eval)

# Function to check if subsequence is part of any larger subsequence
def is_subsequence_in_larger(subseq, larger_subseqs, lch_indices):
    for larger_subseq in larger_subseqs:
        if set(subseq).issubset(set(larger_subseq)) and set(lch_indices).issubset(set(subseq_df[subseq_df['Subsequence'] == larger_subseq]['LCH_index_List'].iloc[0])):
            return True
    return False

# Filtering the DataFrame
filtered_subsequences = []
for index, row in subseq_df.iterrows():
    subseq = row['Subsequence']
    lch_indices = row['LCH_index_List']
    larger_subseqs = subseq_df[subseq_df['Count'] >= row['Count']]['Subsequence']

    if not is_subsequence_in_larger(subseq, larger_subseqs, lch_indices):
        filtered_subsequences.append(row)

# Creating a new DataFrame from the filtered list
filtered_subseq_df = pd.DataFrame(filtered_subsequences)

# Save the resulting DataFrame
filtered_subseq_df.to_csv('filtered_subsequences.csv', index=False)