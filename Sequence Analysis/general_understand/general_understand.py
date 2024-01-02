import pandas as pd
import ast
from collections import Counter
import itertools
import matplotlib.pyplot as plt


df = pd.read_csv('../../step_analyze/step_list.csv')

df['step_list'] = df['step_list'].apply(ast.literal_eval)


# Flatten the list of lists
all_steps = list(itertools.chain.from_iterable(df['step_list']))

# Count occurrences
step_counts = Counter(all_steps)
print(step_counts)

counts_df = pd.DataFrame(step_counts.items(), columns=['Text_ID', 'Count']).sort_values(by='Count', ascending=False)

counts_df.to_csv('step_counts.csv', index=False)

# plot the counts
plt.figure(figsize=(16, 9))
plt.bar(counts_df['Text_ID'], counts_df['Count'])
plt.xticks(rotation=90)
plt.xlabel('Text_ID')
plt.ylabel('Count')
plt.title('Step Counts')
plt.tight_layout()
plt.savefig('step_counts.png')
plt.show()

# find the missing steps
all_steps = set(all_steps)
all_steps = sorted(all_steps)
print(all_steps)
print(len(all_steps))

missing_steps = []
for i in range(1, 172):
    if i not in all_steps:
        missing_steps.append(i)

print(missing_steps)
print(len(missing_steps))

# Histogram of step counts
plt.figure(figsize=(12, 6))
plt.hist(counts_df['Count'], bins=30, color='blue', alpha=0.7)
plt.title('Frequency Distribution of Step Counts')
plt.xlabel('Count')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()


def plot_step_counts(counts_df, bins=30, start_range=0, end_range=1000):
    plt.figure(figsize=(12, 6))
    plt.hist(counts_df['Count'], bins=bins, color='blue', alpha=0.7, range=(start_range, end_range))
    plt.title('Frequency Distribution of Step Counts (Range: {} - {})'.format(start_range, end_range))
    plt.xlabel('Count')
    plt.ylabel('Frequency')
    plt.grid(True)
    # save the plot
    plt.savefig('step_counts_range_{}_{}.png'.format(start_range, end_range))
    plt.show()


plot_step_counts(counts_df, start_range=0, end_range=1000)
plot_step_counts(counts_df, start_range=0, end_range=500)
plot_step_counts(counts_df, start_range=0, end_range=200)
plot_step_counts(counts_df, start_range=0, end_range=50, bins=50)