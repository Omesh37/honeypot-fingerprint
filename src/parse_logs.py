import pandas as pd
import json

input_file = '/home/omesh/cowrie-proto/cowrie-logs/cowrie.json'
output_file = './data/processed/sessions.csv'

data = []
with open(input_file, 'r') as f:
    for line in f:
        try:
            entry = json.loads(line)
            data.append({
                'timestamp': entry.get('timestamp'),
                'session': entry.get('session'),
                'src_ip': entry.get('src_ip'),
                'dst_ip': entry.get('dst_ip'),
                'message': entry.get('message')
            })
        except json.JSONDecodeError:
            continue

df = pd.DataFrame(data)
df.to_csv(output_file, index=False)
print(f"Saved parsed sessions to {output_file}")
