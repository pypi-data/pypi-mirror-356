import pandas as pd
import os

# Load the CSV file
input_file = "./pollutionData158324.csv"
df = pd.read_csv(input_file)

# Select the desired columns by position (columns 0 to 4)
selected_df = df.iloc[:, 0:5]

# Define output path
output_dir = "./data"
output_file = os.path.join(output_dir, "pollution.txt")

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Export to TXT file with space-separated values and newline-separated rows
selected_df.to_csv(output_file, sep=' ', index=False, header=False, lineterminator='\n')
