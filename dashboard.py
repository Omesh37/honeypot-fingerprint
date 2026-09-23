import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Attacker Fingerprint Dashboard", layout="wide")
st.title("🧠 Attacker Fingerprint Dashboard")

# Load datasets
sessions = pd.read_csv('/home/omesh/honeypot-fingerprint/data/processed/sessions.csv')
timing = pd.read_csv('/home/omesh/honeypot-fingerprint/data/processed/timing_only.csv')
ttp = pd.read_csv('/home/omesh/honeypot-fingerprint/data/processed/ttp_only.csv')
fused = pd.read_csv('/home/omesh/honeypot-fingerprint/data/processed/fused.csv')
clusters = pd.read_csv('/home/omesh/honeypot-fingerprint/models/cluster_labels.csv')
disagreements = pd.read_csv('/home/omesh/honeypot-fingerprint/data/processed/disagreements.csv')

# --- Summary metrics ---
st.subheader("📊 Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sessions", len(sessions['session'].unique()))
col2.metric("Total Commands", len(sessions))
col3.metric("Disagreements Detected", len(disagreements))

# --- Cluster distribution ---
st.subheader("🎯 Cluster Distribution")
cluster_counts = clusters['cluster'].value_counts().sort_index()
fig, ax = plt.subplots()
sns.barplot(x=cluster_counts.index, y=cluster_counts.values, palette="viridis", ax=ax)
ax.set_xlabel("Cluster ID")
ax.set_ylabel("Number of Sessions")
ax.set_title("Attacker Cluster Distribution")
st.pyplot(fig)

# --- Timing vs Category heatmap ---
st.subheader("⌛ Timing vs TTP Category")
merged = pd.merge(timing, ttp, on=['timestamp','session'], how='inner')
pivot = merged.pivot_table(index='category', values='command_length', aggfunc='mean')
fig2, ax2 = plt.subplots()
sns.heatmap(pivot, annot=True, cmap="mako", ax=ax2)
ax2.set_title("Average Command Length per TTP Category")
st.pyplot(fig2)

# --- Disagreement timeline ---
st.subheader("⚠️ Disagreement Timeline")
disagreements['timestamp'] = pd.to_datetime(disagreements['timestamp'], errors='coerce')
fig3, ax3 = plt.subplots()
sns.histplot(disagreements['timestamp'], bins=10, kde=True, color='red', ax=ax3)
ax3.set_title("Disagreement Events Over Time")
ax3.set_xlabel("Timestamp")
st.pyplot(fig3)

# --- Data previews ---
st.subheader("🧩 Data Previews")
st.write("Parsed Sessions", sessions.head())
st.write("Timing Features", timing.head())
st.write("TTP Features", ttp.head())
st.write("Fused Dataset", fused.head())
st.write("Cluster Labels", clusters.head())
st.write("Disagreements", disagreements.head())
