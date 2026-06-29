import streamlit as st
import pandas as pd
import plotly.express as px

st.title("👥 Customer Segmentation Dashboard")

df = pd.read_csv("data/processed/rfm_clustered.csv")

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Customers",
    len(df)
)

col2.metric(
    "KMeans Segments",
    df["cluster"].nunique()
)

col3.metric(
    "DBSCAN Segments",
    df["dbscan_cluster"].nunique()
)

st.markdown("---")

# Segment Distribution
st.subheader("Customer Segment Distribution")

segment_counts = (
    df["customer_segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "customer_segment",
    "count"
]

fig = px.bar(
    segment_counts,
    x="customer_segment",
    y="count",
    title="Customers by Segment"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# RFM Scatter
st.subheader("RFM Cluster Analysis")

fig2 = px.scatter(
    df,
    x="frequency",
    y="monetary",
    color="customer_segment",
    size="recency",
    hover_data=[
        "recency",
        "frequency",
        "monetary"
    ],
    title="Customer Segments"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Cluster Summary
st.subheader("Cluster Summary")

summary = (
    df.groupby("customer_segment")
    [["recency","frequency","monetary"]]
    .mean()
    .round(2)
)

st.dataframe(summary)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Segmentation Report",
    csv,
    "customer_segments.csv",
    "text/csv"
)