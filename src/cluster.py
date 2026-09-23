import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Input and output paths
input_file = '/home/omesh/honeypot-fingerprint/data/processed/fused.csv'
output_model = '/home/omesh/honeypot-fingerprint/models/cluster_labels.csv'

# Load fused dataset
df = pd.read_csv(input_file)

# Select numeric features for clustering
features = df[['command_length']].copy()
features['is_paste'] = df['is_paste'].astype(int)

# Scale features
scaler = StandardScaler()
X = scaler.fit_transform(features)

# Perform hierarchical clustering
clustering = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels = clustering.fit_predict(X)

# Add cluster labels to dataframe
df['cluster'] = labels

# Save cluster labels
df[['timestamp','session','cluster']].to_csv(output_model, index=False)
print(f"Saved cluster labels to {output_model}")

# Optional: visualize dendrogram-like scatter
plt.scatter(X[:,0], X[:,1], c=labels, cmap='rainbow')
plt.title("Attacker Clusters")
plt.xlabel("Command Length (scaled)")
plt.ylabel("Paste Indicator (scaled)")
plt.savefig('/home/omesh/honeypot-fingerprint/models/cluster_plot.png')
print("Cluster plot saved to models/cluster_plot.png")
