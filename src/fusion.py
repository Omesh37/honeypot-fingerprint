import pandas as pd

# Input and output paths
timing_file = './data/processed/timing_only.csv'
ttp_file = './data/processed/ttp_only.csv'
output_file = './data/processed/fused.csv'

# Load both datasets
timing_df = pd.read_csv(timing_file)
ttp_df = pd.read_csv(ttp_file)

# Merge on session + timestamp
fused_df = pd.merge(timing_df, ttp_df, on=['timestamp','session'], how='outer')

# Fill missing values
fused_df = fused_df.fillna({'command_length':0, 'is_paste':False, 'category':'Unknown'})

# Save fused dataset
fused_df.to_csv(output_file, index=False)
print(f"Saved fused features to {output_file}")
