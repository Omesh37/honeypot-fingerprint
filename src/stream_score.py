import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# Input paths
fused_file = './data/processed/fused.csv'
labels_file = './models/cluster_labels.csv'

# Load data
df = pd.read_csv(fused_file)
labels_df = pd.read_csv(labels_file)

# Merge labels into fused dataset
df = pd.merge(df, labels_df, on=['timestamp','session'], how='inner')

# Features and labels
features = df[['command_length']].copy()
features['is_paste'] = df['is_paste'].astype(int)
labels = df['cluster']

# Scale features
scaler = StandardScaler()
X = scaler.fit_transform(features)

# Train a simple KNN classifier for real-time scoring
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, labels)

# Example: simulate a new attacker session
new_session = pd.DataFrame({'command_length':[15], 'is_paste':[0]})
new_X = scaler.transform(new_session)

predicted_cluster = knn.predict(new_X)[0]
print(f"New session classified into cluster {predicted_cluster}")
