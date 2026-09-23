import pandas as pd

# Input and output paths
input_file = '/home/omesh/honeypot-fingerprint/data/processed/sessions.csv'
output_file = '/home/omesh/honeypot-fingerprint/data/processed/ttp_only.csv'

# Load parsed sessions
df = pd.read_csv(input_file)

# Clean up message column
df['message'] = df['message'].fillna("").astype(str)

# Simple MITRE ATT&CK style categorization
def categorize(cmd):
    cmd = cmd.lower()
    if 'wget' in cmd or 'curl' in cmd:
        return 'Tool Transfer'
    elif 'chmod' in cmd or 'chown' in cmd:
        return 'Permission Change'
    elif 'ls' in cmd or 'whoami' in cmd or 'uname' in cmd:
        return 'Discovery'
    elif 'cat' in cmd or 'echo' in cmd:
        return 'Execution'
    else:
        return 'Other'

df['category'] = df['message'].apply(categorize)

# Save TTP features
df[['timestamp','session','category']].to_csv(output_file, index=False)
print(f"Saved TTP features to {output_file}")
