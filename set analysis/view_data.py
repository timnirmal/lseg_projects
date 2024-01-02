import pandas as pd

# show all columns
pd.set_option('display.max_columns', None)

df = pd.read_csv('refined_subsequences_trie_zero_removed_grouped.csv')

# keep only LCH_328 and LCH_327 (before keeping check if they are exists)
df = df[df['LCH_index'].apply(lambda x: 'LCH_328' in x or 'LCH_327' in x)]

print(df)
