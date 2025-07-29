
import pickle
import numpy as np

# Load the pickle file
file_path = "./DIEF_B_Snippet50_3weeks.pkl"
with open(file_path, "rb") as f:
    data = pickle.load(f)

# Print shape and some content for the first few entries
for i, entry in enumerate(data[:5]):
    t = entry["t"]
    v = entry["v"]
    y = entry["y"]
    stream_id = entry["StreamID"]

    print(f"\nSeries {i+1}:")
    print(f"  Name      : {y}")
    print(f"  StreamID  : {stream_id}")
    print(f"  Timestamps shape: {t.shape}")
    print(f"  Values shape    : {v.shape}")
    print(f"  First 5 timestamps: {t[:5]}")
    print(f"  First 5 values    : {v[:5]}")

# Step 1: Determine the shortest length across all 'v' arrays
min_len = min(len(entry["v"]) for entry in data)

# Step 2: Truncate and collect values
truncated_matrix = np.stack([entry["v"][:min_len] for entry in data], axis=0).T  # shape (49, min_len)

# Step 3: Save to TXT with space as separator and newline per row
output_path = "./data/building.txt"
np.savetxt(output_path, truncated_matrix, delimiter=' ', fmt='%.6f')