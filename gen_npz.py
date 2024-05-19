import numpy as np
import pandas as pd

# Load data from the CSV file
csv_file = 'C:\\Users\\Lenovo\\Downloads\\file (1)\\morning_only.csv'  # Replace with your CSV file path
data = []

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Assuming the DataFrame has the same structure as created earlier
# Number of unique timesteps and locations
num_timesteps = df['timestep'].nunique()

num_locations = df['location'].nunique()
print(num_timesteps)
# Create an empty NumPy array to store the data
data = np.zeros((num_timesteps, num_locations, 3))  # Assuming 3 columns for flow, occupy, speed
counter=0
# Fill the NumPy array with data from the DataFrame
for index, row in df.iterrows():
    timestep = int(row['timestep']) % 300+counter*300
    location = int(row['location'])
    flow = row['flow']
    occupy = row['occupy']
    speed = row['speed']
    
    if(int(row['timestep']) % 300==0 and temp!=int(row['timestep'])):
        counter+=1
        timestep = int(row['timestep']) % 300+counter*300

    #print(int(row['timestep']))
    #print(timestep)
    data[timestep-1, location-1, 0] = occupy
    data[timestep-1, location-1, 1] = speed
    data[timestep-1, location-1, 2] = flow
    temp=int(row['timestep']) 

# Save the NumPy array as an NPZ filoutput_62day.csvoutput_62day.csve
np.savez("morning_only_dim.npz", data=data)