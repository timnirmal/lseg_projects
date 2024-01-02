import pandas as pd
import ast
from collections import Counter
import itertools
import matplotlib.pyplot as plt
from nltk.util import bigrams, ngrams

df = pd.read_csv('../../step_analyze/step_list.csv')

df['step_list'] = df['step_list'].apply(ast.literal_eval)

# Convert step sequences into trigrams
trigram_sequences = [list(ngrams(step_sequence, 3)) for step_sequence in df['step_list'] if len(step_sequence) >= 3]

# Flatten the list of trigram lists
all_trigrams = list(itertools.chain.from_iterable(trigram_sequences))

# Count occurrences of each trigram
trigram_counts = Counter(all_trigrams)

# Convert to a DataFrame and sort
trigram_counts_df = pd.DataFrame(trigram_counts.items(), columns=['Trigram', 'Count'])
trigram_counts_df = trigram_counts_df.sort_values(by='Count', ascending=False)

# Display the top 10 most common trigrams
print(trigram_counts_df.head(10))

# Optionally, save to a CSV file
trigram_counts_df.to_csv('trigram_counts.csv', index=False)
