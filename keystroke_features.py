import pandas as pd
import numpy as np

# Input and output paths
input_file = '/home/omesh/honeypot-fingerprint/data/processed/sessions.csv'
output_file = '/home/omesh/honeypot-fingerprint/data/processed/timing_only.csv'

# Load parsed sessions
df = pd.read_csv(input_file)

# Clean up message column: replace NaN with empty string
df['message'] = df['message'].fillna("").astype(str)

# Example keystroke features
df['command_length'] = df['message'].apply(len)
df['is_paste'] = df['command_length'] > 20   # crude paste detection

# Save timing features
df[['timestamp','session','command_length','is_paste']].to_csv(output_file, index=False)
print(f"Saved keystroke features to {output_file}")
