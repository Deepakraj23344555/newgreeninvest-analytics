# app.py

import streamlit as st
from optimizer import optimize_portfolio
from utils import load_esg_data
from analysis import plot_esg_trends, plot_carbon_impact
from report_generator import generate_pdf_report
from esg_news import get_esg_news

st.set_page_config(page_title="GreenInvest Analytics", layout="wide")

# Logo
st.title("GreenInvest Analytics")

# Load ESG data
esg_data = load_esg_data("data/esg_scores.csv")

# Sidebar inputs
st.sidebar.header("Filter Portfolio")
esg_min = st.sidebar.slider("Minimum ESG Score", min_value=0, max_value=100, value=50)
max_carbon = st.sidebar.slider("Maximum Carbon Footprint", min_value=0, max_value=200, value=100)
risk_appetite = st.sidebar.selectbox("Risk Appetite", options=["Low", "Medium", "High"])

# Optimize portfolio with error handling
try:
    weights, performance, portfolio_df = optimize_portfolio(esg_data, esg_min, max_carbon, risk_appetite)
except ValueError as e:
    st.warning(str(e))
    st.stop()

# Unpack performance tuple
exp_return, volatility, sharpe = performance

# Show performance metrics
col1, col2, col3 = st.columns(3)
col1.metric("Expected Return", f"{exp_return * 100:.2f}%")
col2.metric("Volatility", f"{volatility * 100:.2f}%")
col3.metric("Sharpe Ratio", f"{sharpe:.2f}")

# ESG Trend plot
st.subheader("ESG Score Trends")
st.pyplot(plot_esg_trends(esg_data))

# Carbon Impact plot
st.subheader("Portfolio Carbon Impact")
st.pyplot(plot_carbon_impact(portfolio_df))

# Portfolio table
st.subheader("Optimized Portfolio")
st.dataframe(portfolio_df)

# Download report button
if st.button("Download Portfolio Report (PDF)"):
    pdf_path = generate_pdf_report(portfolio_df, exp_return, volatility, sharpe)
    with open(pdf_path, "rb") as f:
        st.download_button(label="Download PDF", data=f, file_name="GreenInvest_Portfolio_Report.pdf")

# ESG News Section
st.subheader("Latest ESG News")
news_articles = get_esg_news()
for article in news_articles:
    st.markdown(f"**[{article['title']}]({article['link']})**  \nPublished on: {article['published']}")

