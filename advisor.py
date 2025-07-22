def generate_advice(score):
    if score >= 75:
        return "Great ESG performance. Consider increasing exposure to green bonds or clean energy ETFs."
    elif score >= 50:
        return "Moderate ESG score. Review your holdings for ESG laggards."
    else:
        return "Low ESG score. Divest from fossil fuels and invest in ESG leaders."
