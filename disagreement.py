import pandas as pd

# Input paths
timing_file = '/home/omesh/honeypot-fingerprint/data/processed/timing_only.csv'
ttp_file = '/home/omesh/honeypot-fingerprint/data/processed/ttp_only.csv'

# Load datasets
timing_df = pd.read_csv(timing_file)
ttp_df = pd.read_csv(ttp_file)

# Merge on session + timestamp
merged = pd.merge(timing_df, ttp_df, on=['timestamp','session'], how='inner')

# Define disagreement: long paste but simple category, or short command but complex category
def detect_disagreement(row):
    if row['is_paste'] and row['category'] in ['Discovery','Other']:
        return True
    if not row['is_paste'] and row['category'] in ['Tool Transfer','Permission Change']:
        return True
    return False

merged['disagreement'] = merged.apply(detect_disagreement, axis=1)

# Save disagreements
output_file = '/home/omesh/honeypot-fingerprint/data/processed/disagreements.csv'
merged[merged['disagreement']].to_csv(output_file, index=False)

print(f"Saved disagreement cases to {output_file}")
