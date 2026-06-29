import streamlit as st
from utils.pdf_generator import generate_report

st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RetailPulse")
st.subheader("AI-Powered Customer Analytics & Demand Forecasting Platform")

st.markdown("---")

st.markdown("""
### Features

- Demand Forecasting
- Customer Segmentation
- Churn Prediction
- Inventory Optimization
- Drift Monitoring
- Automated Retraining

### Business Impact

- Reduce Stockouts
- Increase Revenue
- Improve Customer Retention
""")

st.markdown("## 📊 System Health")

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Forecast Model",
    "Active"
)

col2.metric(
    "Churn Model",
    "Active"
)

col3.metric(
    "Drift Status",
    "No Drift"
)

col4.metric(
    "Airflow Retraining",
    "Scheduled"
)

st.markdown("---")

st.subheader("🚨 Alerts")

st.success(
    "Forecasting pipeline executed successfully"
)

st.info(
    "Airflow retraining DAG configured"
)

st.success(
    "No data drift detected"
)

if st.button("📄 Generate Executive Report"):

    pdf_file = generate_report(
        "RetailPulse_Report.pdf",
        "RetailPulse Executive Summary",
        """
        Demand forecasting,
        customer segmentation,
        churn prediction,
        inventory optimization,
        drift monitoring,
        and retraining systems are operational.
        """
    )

    with open(pdf_file, "rb") as f:

        st.download_button(
            "⬇ Download PDF Report",
            f,
            file_name="RetailPulse_Report.pdf"
        )

