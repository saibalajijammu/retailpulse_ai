import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📦 Inventory Optimization Dashboard")

df = pd.read_csv(
    "data/processed/inventory_optimization.csv"
)

row = df.iloc[0]

# KPIs

col1, col2, col3 = st.columns(3)

col1.metric(
    "Forecast Demand",
    f"{row['forecast_demand']:,.0f}"
)

col2.metric(
    "Current Stock",
    f"{row['current_stock']:,.0f}"
)

col3.metric(
    "Recommended Order",
    f"{row['recommended_order_qty']:,.0f}"
)

st.markdown("---")

# Inventory Metrics

st.subheader("Inventory Planning Metrics")

metrics = pd.DataFrame({
    "Metric":[
        "Forecast Demand",
        "Current Stock",
        "Safety Stock",
        "Reorder Point",
        "Recommended Order Qty"
    ],
    "Value":[
        row["forecast_demand"],
        row["current_stock"],
        row["safety_stock"],
        row["reorder_point"],
        row["recommended_order_qty"]
    ]
})

fig = px.bar(
    metrics,
    x="Metric",
    y="Value",
    title="Inventory Metrics Overview"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Status

st.subheader("Inventory Status")

status = str(row["inventory_status"])

if "critical" in status.lower():
    st.error(f"🔴 {status}")

elif "reorder" in status.lower():
    st.warning(f"🟡 {status}")

else:
    st.success(f"🟢 {status}")

st.markdown("---")

# Lead Time

st.subheader("Supply Chain Metrics")

col1, col2 = st.columns(2)

col1.metric(
    "Lead Time (Days)",
    row["lead_time_days"]
)

col2.metric(
    "Safety Stock",
    f"{row['safety_stock']:,.0f}"
)

st.markdown("---")

# Recommendation

st.subheader("Inventory Recommendation")

st.info(
    f"""
    Forecast demand is projected at
    {row['forecast_demand']:,.0f} units.

    Current inventory is
    {row['current_stock']:,.0f} units.

    Recommended replenishment quantity:
    {row['recommended_order_qty']:,.0f} units.
    """
)

st.dataframe(df)