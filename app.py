import streamlit as st
import pandas as pd
import pdfplumber
import re
from io import BytesIO

def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def split_blocks(full_text):
    blocks = re.split(r'(?=Cardholder\s+Name\s*:)', full_text, flags=re.IGNORECASE)
    blocks = [b.strip() for b in blocks if len(b.strip()) > 30]
    return blocks


def parse_block(block):
    data = {}

    name = re.search(r'Cardholder\s+Name\s*:\s*(.*)', block)
    data["Cardholder Name"] = name.group(1).strip() if name else "Not found"

    card = re.search(r'XXXX[-\s]*\d{4}', block)
    if card:
        data["Last 4 Digits"] = re.search(r'(\d{4})$', card.group(0)).group(1)
    else:
        data["Last 4 Digits"] = "Not found"

    period = re.search(r'(Statement\s+Period|Billing\s+Cycle)\s*:\s*(.*)', block)
    data["Statement Period"] = period.group(2).strip() if period else "Not found"

    due = re.search(r'(Payment\s+Due\s+Date|Payment\s+Due)\s*:\s*(\d{1,2}-[A-Za-z]{3}-\d{4})', block)
    data["Payment Due Date"] = due.group(2).strip() if due else "Not found"

    total = re.search(r'Total\s+Amount\s+Due\s*[:₹\s\.]*([\d,]+(?:\.\d{2})?)', block)
    data["Total Amount Due"] = total.group(1).replace(",", "") if total else "Not found"

    return data


def process_pdf(uploaded_file):
    text = extract_text(uploaded_file)
    blocks = split_blocks(text)
    results = []

    for i, blk in enumerate(blocks, 1):
        record = parse_block(blk)
        record["Record #"] = i
        results.append(record)

    if not results:
        return None

    df = pd.DataFrame(results)
    return df



st.title("📄 Credit Card Statement Parser")
st.write("Upload a credit card statement PDF to extract details like cardholder name, due date, and total amount due.")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    st.info("Processing your PDF...")
    df = process_pdf(uploaded_file)

    if df is not None:
        st.success(f"✅ Extracted {len(df)} records successfully!")
        st.dataframe(df)

        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        st.download_button(
            label="📥 Download CSV File",
            data=csv_buffer,
            file_name="parsed_results.csv",
            mime="text/csv"
        )
    else:
        st.error("❌ No valid records found. Please check if 'Cardholder Name:' exists in your PDF.")