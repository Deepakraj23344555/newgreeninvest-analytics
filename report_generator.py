from fpdf import FPDF
import os

def generate_pdf_report(user_name, portfolio_df, performance):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(0, 10, f"Green Portfolio Report for {user_name}", ln=True, align="C")
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Expected Return: {performance['return']:.2f}%", ln=True)
    pdf.cell(0, 10, f"Total Carbon Impact: {performance['carbon']:.2f} kg CO₂", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 10, "Portfolio Details:", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    line_height = pdf.font_size * 2
    col_widths = [30, 25, 25, 40, 40]  # customize widths for columns
    
    # Header row
    headers = ["Ticker", "Weight", "ESG Score", "Carbon Footprint", "Sector"]
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], line_height, header, border=1)
    pdf.ln(line_height)
    
    # Portfolio rows
    for _, row in portfolio_df.iterrows():
        pdf.cell(col_widths[0], line_height, row['Ticker'], border=1)
        pdf.cell(col_widths[1], line_height, f"{row['Weight']:.2%}", border=1)
        pdf.cell(col_widths[2], line_height, f"{row['ESG Score']}", border=1)
        pdf.cell(col_widths[3], line_height, f"{row['Carbon Footprint']}", border=1)
        pdf.cell(col_widths[4], line_height, row['Sector'], border=1)
        pdf.ln(line_height)
    
    # Save PDF
    os.makedirs("reports", exist_ok=True)
    file_path = f"reports/{user_name}_green_portfolio_report.pdf"
    pdf.output(file_path)
    return file_path
