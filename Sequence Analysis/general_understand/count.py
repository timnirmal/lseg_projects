import pandas as pd

df = pd.read_csv("step_counts.csv")

# Text_ID,Count -> count all the count
count = 0

for i in range(len(df)):
    count += df['Count'][i]
    print(df['Count'][i])

print(count)
