import pandas as pd
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler

# Input paths
fused_file = '/home/omesh/honeypot-fingerprint/data/processed/fused.csv'
labels_file = '/home/omesh/honeypot-fingerprint/models/cluster_labels.csv'

# Load data
df = pd.read_csv(fused_file)
labels_df = pd.read_csv(labels_file)

# Merge labels back into fused dataset
df = pd.merge(df, labels_df, on=['timestamp','session'], how='inner')

# Select numeric features
features = df[['command_length']].copy()
features['is_paste'] = df['is_paste'].astype(int)

# Scale features
scaler = StandardScaler()
X = scaler.fit_transform(features)

# Extract cluster labels
labels = df['cluster']

# Compute evaluation metrics
silhouette = silhouette_score(X, labels)
calinski = calinski_harabasz_score(X, labels)
davies = davies_bouldin_score(X, labels)

print("Cluster Evaluation Results:")
print(f"Silhouette Score: {silhouette:.3f}")
print(f"Calinski-Harabasz Index: {calinski:.3f}")
print(f"Davies-Bouldin Score: {davies:.3f}")
