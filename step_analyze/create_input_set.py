import pandas as pd

from step_analyze.dataset import int_list, int_list_increased

# Creating a DataFrame with modified LCH_index
df = pd.DataFrame({'LCH_index': ['LCH_' + str(i) for i in range(len(int_list))], 'step_list': int_list})

# save
df.to_csv('step_list.csv', index=False)