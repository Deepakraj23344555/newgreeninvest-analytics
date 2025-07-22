
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from optimizer import optimize_portfolio
from analysis import plot_esg_trends, plot_carbon_impact, plot_sector_esg_breakdown
from report_generator import generate_pdf_report
from utils import load_esg_data
from advisor import generate_advice
from scenario import simulate_fossil_divestment
from esg_news import get_esg_news
from database import save_history
from datetime import datetime

st.set_page_config(page_title="GreenInvest Analytics", layout="wide")

st.title("🌱 GreenInvest Analytics: ESG-Aware Portfolio Optimizer")

# Sidebar
st.sidebar.header("🔧 Portfolio Settings")
esg_min = st.sidebar.slider("Minimum ESG Score", 0, 100, 50)
max_carbon = st.sidebar.slider("Max Carbon Footprint (tCO₂e)", 0, 100, 50)
risk_appetite = st.sidebar.selectbox("Risk Appetite", ["Low", "Medium", "High"])

apply_scenario = st.sidebar.checkbox("🔁 Simulate Fossil-Fuel Divestment")
show_news = st.sidebar.checkbox("📰 Show ESG News", value=True)
upload = st.sidebar.file_uploader("📂 Upload Your Portfolio CSV", type=["csv"])

# Load ESG data
esg_data = load_esg_data("data/esg_scores.csv")
if apply_scenario:
    esg_data = simulate_fossil_divestment(esg_data)

# Optimization
weights, performance, portfolio_df = optimize_portfolio(esg_data, esg_min, max_carbon, risk_appetite)

# Portfolio Display
st.subheader("📊 Optimized Portfolio")
st.dataframe(portfolio_df)

st.metric("Expected Return", f"{performance['return']*100:.2f}%")
st.metric("Volatility", f"{performance['volatility']*100:.2f}%")
st.metric("Sharpe Ratio", f"{performance['sharpe']:.2f}")

# ESG Insights
st.subheader("📈 ESG Trend Analysis")
st.pyplot(plot_esg_trends(esg_data))

st.subheader("🌍 Carbon Impact of Portfolio")
st.pyplot(plot_carbon_impact(portfolio_df))

st.subheader("🏭 Sector-Wise ESG Breakdown")
st.pyplot(plot_sector_esg_breakdown(esg_data))

# Advisor Section
avg_score = portfolio_df['ESG Score'].mean()
st.subheader("🤖 ESG Strategy Recommendation")
st.info(generate_advice(avg_score))

# Save Report
if st.button("🧾 Export PDF Report"):
    generate_pdf_report(portfolio_df, performance, "reports/portfolio_report.pdf")
    st.success("PDF Report saved to reports/portfolio_report.pdf")

# Save to DB
save_history("user1", weights, avg_score, portfolio_df['Carbon Footprint'].sum(), str(datetime.now().date()))

# News Section
if show_news:
    st.subheader("📰 Latest ESG Investing News")
    for title, link in get_esg_news():
        st.markdown(f"🔗 [{title}]({link})")

# Upload Option (display uploaded file)
if upload:
    st.subheader("📄 Uploaded Portfolio")
    uploaded_df = pd.read_csv(upload)
    st.dataframe(uploaded_df)
