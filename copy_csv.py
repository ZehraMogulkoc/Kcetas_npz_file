import pandas as pd
import random


original_df = pd.read_csv('C:\\Users\\Lenovo\\Downloads\\file (1)\\morning_occupy_V2.csv', delimiter=',')

#4000 çalıştı v12
num_duplicates = 4000
increment_timestep = 301
max_timestep = original_df['timestep'].max()


duplicated_df = pd.DataFrame()
original_df['location'] -= 1
#original_df['timestep'] += 66521
original_df.to_csv('morning_occupy.csv', index=False, sep=',')
#33712 66521
duplicated_df = pd.concat([duplicated_df, original_df])
'''
for i in range(0, num_duplicates):
    sampled_row = original_df.sample(n=20)
    max_timestep = duplicated_df['timestep'].max()
    sampled_row['timestep'] = max_timestep + (increment_timestep )
    
    # Append the modified row to the duplicated DataFrame
    duplicated_df = pd.concat([duplicated_df, sampled_row])

# Save the duplicated data to a new CSV file
duplicated_df.to_csv('traffic_last.csv', index=False, sep=',')
'''