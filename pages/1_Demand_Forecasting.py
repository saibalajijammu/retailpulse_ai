import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Demand Forecasting Dashboard")

forecast = pd.read_csv("data/processed/hybrid_forecast.csv")

forecast["date"] = pd.to_datetime(forecast["date"])

st.markdown("## Forecast KPIs")

col1,col2,col3=st.columns(3)

col1.metric(
    "Total Forecast Demand",
    f"{forecast['hybrid_prediction'].sum():,.0f}"
)

col2.metric(
    "Average Daily Demand",
    f"{forecast['hybrid_prediction'].mean():.2f}"
)

col3.metric(
    "Peak Demand",
    f"{forecast['hybrid_prediction'].max():.2f}"
)

st.markdown("---")

st.subheader("Hybrid Forecast Comparison")

fig = px.line(
    forecast,
    x="date",
    y=[
        "prophet_prediction",
        "lstm_prediction",
        "hybrid_prediction"
    ],
    title="Prophet vs LSTM vs Hybrid Forecast"
)

st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

st.subheader("What-If Analysis")

promotion = st.slider(
    "Promotion Impact (%)",
    -50,
    50,
    0
)

forecast["adjusted_forecast"] = (
    forecast["hybrid_prediction"]
    *
    (1 + promotion/100)
)

fig2 = px.line(
    forecast,
    x="date",
    y=[
        "hybrid_prediction",
        "adjusted_forecast"
    ],
    title="Demand Scenario Simulation"
)

st.plotly_chart(fig2,use_container_width=True)

st.markdown("---")

st.subheader("Forecast Dataset")

st.dataframe(forecast)
csv = forecast.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Forecast CSV",
    data=csv,
    file_name="forecast_report.csv",
    mime="text/csv"
)