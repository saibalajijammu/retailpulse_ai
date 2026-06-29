import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚠️ Churn Prediction Dashboard")

churn = pd.read_csv(
    "data/processed/churn_predictions.csv"
)

importance = pd.read_csv(
    "data/processed/feature_importance.csv"
)

# KPIs

total_customers = len(churn)

high_risk = len(
    churn[churn["churn_probability"] > 0.7]
)

avg_risk = churn[
    "churn_probability"
].mean()

col1,col2,col3 = st.columns(3)

col1.metric(
    "Customers Analyzed",
    total_customers
)

col2.metric(
    "High Risk Customers",
    high_risk
)

col3.metric(
    "Average Churn Risk",
    f"{avg_risk:.2%}"
)

st.markdown("---")

# Risk Distribution

st.subheader("Churn Probability Distribution")

fig = px.histogram(
    churn,
    x="churn_probability",
    nbins=20,
    title="Customer Churn Risk"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Feature Importance

st.subheader("Feature Importance")

importance = (
    importance
    .sort_values(
        "importance",
        ascending=False
    )
)

fig2 = px.bar(
    importance.head(10),
    x="importance",
    y="feature",
    orientation="h",
    title="Top Drivers of Churn"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# High Risk Customers

st.subheader("High Risk Customers")

risk_table = churn.sort_values(
    "churn_probability",
    ascending=False
)

st.dataframe(
    risk_table.head(20)
)

csv = churn.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Churn Report",
    csv,
    "churn_report.csv",
    "text/csv"
)