from step_analyze.dataset import int_list, int_list_increased
import pandas as pd
from ast import literal_eval


df = pd.read_csv('../step_analyze/step_list.csv')

# df example
# LCH_index,step_list
# LCH_0,"[127, 127, 127]"
# LCH_1,"[128, 53, 128, 53, 128, 53]"


def generate_subsequences(lst):
    # Generate all contiguous subsequences of lst
    subsequences = []
    for start in range(len(lst)):
        for end in range(start + 1, len(lst) + 1):
            # Convert the sublist to a tuple
            subsequences.append(tuple(lst[start:end]))
    return subsequences


def generate_subsequences_with_counts(lst):
    # Dictionary to store subsequences and their counts
    subsequence_counts = {}

    # Generate all contiguous subsequences of lst and count them
    for start in range(len(lst)):
        for end in range(start + 1, len(lst) + 1):
            # Convert the sublist to a tuple
            subseq = tuple(lst[start:end])

            # Count the subsequence
            subsequence_counts[subseq] = subsequence_counts.get(subseq, 0) + 1

    return subsequence_counts


# Function to remove shorter subsequences contained in longer subsequences with equal or higher counts
def remove_redundant_subsequences(subsequences):
    subsequences_to_remove = set()

    # Iterate through each subsequence
    for subseq, count in subsequences.items():
        # Check for all possible shorter subsequences
        for i in range(1, len(subseq)):
            for j in range(len(subseq) - i + 1):
                shorter_subseq = subseq[j:j + i]
                # If the shorter subsequence exists with a lower or equal count, mark it for removal
                if shorter_subseq in subsequences and subsequences[shorter_subseq] <= count:
                    subsequences_to_remove.add(shorter_subseq)

    # Remove the marked subsequences
    for subseq in subsequences_to_remove:
        subsequences.pop(subseq)

    return subsequences


# int_list_increased = int_list_increased[0:10]

# # Large set to store all subsequences across lists
# all_subsequences = {}
#
# for lst in int_list_increased:
#     subseq_counts = generate_subsequences_with_counts(lst)
#
#     # Sorting each list's subsequences by their lengths
#     sorted_subseq_counts = {k: v for k, v in sorted(subseq_counts.items(), key=lambda item: len(item[0]))}
#
#     # Merge with the large set
#     for subseq, count in sorted_subseq_counts.items():
#         all_subsequences[subseq] = all_subsequences.get(subseq, 0) + count
#
# # The large set of all subsequences across lists with counts
# print(all_subsequences)
# print(len(all_subsequences))
#
# def create_dataframe(dictionary, column_names, save_to_csv=False, file_name='subsequences.csv'):
#     # Create a DataFrame from a dictionary
#     df = pd.DataFrame.from_dict(dictionary, orient='index', columns=column_names)
#     if save_to_csv:
#         df.to_csv(file_name)
#         print(f"DataFrame saved to {file_name}")
#     return df



def generate_subsequences_with_counts_for_df(row):
    lst = eval(row['step_list'])  # Convert string representation of list back to list
    subseq_counts = generate_subsequences_with_counts(lst)
    return subseq_counts

# Apply the function to each row and store the result in a new column
df['subsequences'] = df.apply(generate_subsequences_with_counts_for_df, axis=1)

# save to csv
df.to_csv('subsequences.csv')


from collections import defaultdict

# Dictionary to store subsequences, their associated LCH_index IDs, and counts
subsequences_with_ids_and_counts = defaultdict(lambda: defaultdict(int))

for index, row in df.iterrows():
    LCH_index = row['LCH_index']
    subseq_counts = row['subsequences']
    for subseq, count in subseq_counts.items():
        subsequences_with_ids_and_counts[subseq][LCH_index] += count

# Convert to a DataFrame
subseq_list = []
for subseq, LCH_counts in subsequences_with_ids_and_counts.items():
    LCH_index_list = list(LCH_counts.keys())
    total_count = sum(LCH_counts.values())
    subseq_list.append({'Subsequence': subseq, 'LCH_index_List': LCH_index_list,
                        'LCH_index_Count_List': dict(LCH_counts), 'Count': total_count})

subseq_df = pd.DataFrame(subseq_list)

# Sorting the DataFrame by count (optional)
subseq_df = subseq_df.sort_values(by='Count', ascending=False)

# Save to CSV
subseq_df.to_csv('subsequences_with_ids.csv')
