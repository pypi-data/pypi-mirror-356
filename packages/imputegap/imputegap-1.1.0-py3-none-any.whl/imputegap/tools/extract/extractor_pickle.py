import numpy as np
import pandas as pd
import os
import pickle

# Load the pickle file
input_file = "./000.pickle"
with open(input_file, "rb") as f:
    data = pickle.load(f)

# Print the raw type and structure
print(f"type = {type(data)}")
print("data =", data)

# Unpack and print shapes
if isinstance(data, list):


    filename = data[0]
    timestamps = data[1]
    values = data[2]


    print(filename)

    # Print shapes
    print("timestamps shape:", timestamps.shape)
    print("values shape:", values.shape)

    # Print subset of data
    np.set_printoptions(threshold=np.inf)
    print(timestamps[100])
    print(values[100])

import pandas as pd

df = pd.DataFrame(data=values.reshape(1, -1), columns=timestamps)
print(df.shape)  # (1, T)


print("\n\n\n")


