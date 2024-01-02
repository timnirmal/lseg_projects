import pandas as pd
import ast
from tqdm import tqdm


class TrieNode:
    def __init__(self):
        self.children = {}
        self.counts = {}
        self.reduced = False

    def insert(self, subsequence, lch_counts):
        # Skip insertion if 'LCH_328' is in the lch_counts
        if 'LCH_328' in lch_counts:
            return

        node = self
        for item in subsequence:
            if item not in node.children:
                node.children[item] = TrieNode()
            node = node.children[item]

        node.counts = {lch: max(node.counts.get(lch, 0), count) for lch, count in lch_counts.items()}

    def reduce_counts(self, subsequence, lch_counts):
        if self.reduced:
            return

        for lch, count in lch_counts.items():
            if lch in self.counts:
                self.counts[lch] = max(self.counts[lch] - count, 0)

        self.reduced = True

        # Reduce counts for longer subsequences
        node = self
        for item in subsequence:
            if item in node.children:
                node = node.children[item]
                node.reduce_counts(subsequence, lch_counts)

    def export_to_file(self, file_path):
        with open(file_path, 'w') as file:
            self._export_node(file)

    def _export_node(self, file, depth=0, path=[]):
        indent = ' ' * depth
        for item, node in self.children.items():
            file.write(f"{indent}{item}: {node.counts}\n")
            node._export_node(file, depth + 4, path + [item])


def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    df['Subsequence'] = df['Subsequence'].apply(ast.literal_eval)
    df['LCH_index_Count_List'] = df['LCH_index_Count_List'].apply(ast.literal_eval)
    return df


def build_and_reduce_trie(df):
    trie = TrieNode()
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc="Building Trie"):
        trie.insert(row['Subsequence'], row['LCH_index_Count_List'])

    # Sort subsequences by length and then reduce counts
    sorted_df = df.sort_values(by='Subsequence', key=lambda x: x.map(len))
    for _, row in tqdm(sorted_df.iterrows(), total=sorted_df.shape[0], desc="Reducing Counts"):
        trie.reduce_counts(row['Subsequence'], row['LCH_index_Count_List'])

    return trie

# if there is 'LCH_328' in any row of LCH_index_Count_List remove that

def trie_to_dataframe(trie):
    data = []

    def traverse(node, path):
        if node.counts:
            data.append((','.join(map(str, path)), node.counts, sum(node.counts.values())))

        for child, next_node in node.children.items():
            traverse(next_node, path + [child])

    traverse(trie, [])
    return pd.DataFrame(data, columns=['Subsequence', 'LCH_index_Count_List', 'Count'])


# Example Usage
file_path = 'subsequences_with_ids.csv'
# Load and prepare data
df = load_and_prepare_data(file_path)



# Build and reduce the trie
trie = build_and_reduce_trie(df)

# Example usage to export the Trie to a text file
trie.export_to_file('trie_structure.txt')

# Convert trie to DataFrame
result_df = trie_to_dataframe(trie)

print(result_df)

# save to csv
result_df.to_csv('refined_subsequences_trie.csv', index=False)

# Filter out rows where all counts are zero
filtered_df = result_df[result_df['Count'] > 0]

# Save the filtered DataFrame to CSV
filtered_df.to_csv('refined_subsequences_trie_zero_removed.csv', index=False)

filtered_df = pd.read_csv('refined_subsequences_trie_zero_removed.csv')

# Convert string representation back to dictionary
filtered_df['LCH_index_Count_List'] = filtered_df['LCH_index_Count_List'].apply(ast.literal_eval)

# Unpack LCH_index_Count_List into separate rows
rows = []
for _, row in tqdm(filtered_df.iterrows(), total=filtered_df.shape[0], desc="Processing Rows"):
    for lch_index, count in row['LCH_index_Count_List'].items():
        # Convert subsequence string to tuple for set representation
        subsequence_set = tuple(map(int, row['Subsequence'].split(',')))
        rows.append({'LCH_index': lch_index, 'Subsequence': subsequence_set, 'Count': count})

expanded_df = pd.DataFrame(rows)

# Group by LCH_index and aggregate subsequences and their counts
grouped_df = expanded_df.groupby('LCH_index').agg({'Subsequence': lambda x: {seq: count for seq, count in zip(x, expanded_df['Count'])}}).reset_index()

# count the number of subsequences
grouped_df['Subsequence_Count'] = grouped_df['Subsequence'].apply(len)

print(grouped_df)

# save to csv
grouped_df.to_csv('refined_subsequences_trie_zero_removed_grouped.csv', index=False)




# graph network, we can get next node from that,
# but we need a method to insert ac data like positional embedding in trnasformaer

# markov, lstm, graph netwrok, transformer