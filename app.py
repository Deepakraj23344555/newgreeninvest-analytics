import streamlit as st
from optimizer import optimize_portfolio
from analysis import plot_esg_trends, plot_carbon_impact
from report_generator import generate_pdf_report
from database import save_portfolio
from utils import load_esg_data

st.set_page_config(page_title="GreenInvest Analytics", layout="wide")

# --- Header
st.image("assets/logo.png", width=60)
st.title("🌱 GreenInvest Analytics")
st.markdown("Smart Investing. Sustainable Future.")

# --- Sidebar Inputs
with st.sidebar:
    st.header("Build Your Portfolio")
    esg_min = st.slider("Minimum ESG Score", 0, 100, 70)
    max_carbon = st.slider("Max Carbon Impact (kg CO₂)", 0, 500, 200)
    risk_appetite = st.selectbox("Risk Profile", ["Low", "Moderate", "High"])
    user_name = st.text_input("Investor Name")
    optimize_btn = st.button("Optimize Portfolio")

# --- Load ESG Data
esg_data = load_esg_data("data/esg_scores.csv")

# --- Optimization and Output
if optimize_btn and user_name:
    weights, performance, portfolio_df = optimize_portfolio(esg_data, esg_min, max_carbon, risk_appetite)

    st.subheader("📊 Optimized Portfolio")
    st.dataframe(portfolio_df)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Expected Return", f"{performance['return']:.2f}%")
    with col2:
        st.metric("Carbon Impact", f"{performance['carbon']} kg CO₂")

    st.subheader("📉 ESG Trend Chart")
    st.pyplot(plot_esg_trends(esg_data))

    st.subheader("🌿 Carbon Footprint Chart")
    st.pyplot(plot_carbon_impact(portfolio_df))

    st.subheader("💡 Recommendations")
    st.info("Consider rebalancing every 3–6 months to maintain ESG alignment and risk balance.")

    if st.button("📥 Download PDF Report"):
        report_path = generate_pdf_report(user_name, portfolio_df, performance)
        with open(report_path, "rb") as file:
            st.download_button(label="Download Report", data=file, file_name="GreenPortfolio_Report.pdf", mime="application/pdf")

    save_portfolio(user_name, portfolio_df, performance)
