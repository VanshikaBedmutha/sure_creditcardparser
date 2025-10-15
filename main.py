import pdfplumber
import re
import pandas as pd
from pathlib import Path


def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def split_blocks(full_text):
    # Split by repeating header "Cardholder Name:"
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

def process_bank(bank_name):
    pdf_path = f"data/{bank_name.lower()}.pdf"

    if bank_name.lower() == "hdfc_multi_cards":
        pdf_path = f"data/{bank_name.lower()}.pdf"

    try:
        text = extract_text(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return

    blocks = split_blocks(text)
    results = []
    for i, blk in enumerate(blocks, 1):
        record = parse_block(blk)
        record["Record #"] = i
        results.append(record)

    if not results:
        print("No cardholder details found. Check if 'Cardholder Name:' is present.")
        return

    Path("output").mkdir(exist_ok=True)
    output_path = f"output/{bank_name.lower()}_results.csv"
    pd.DataFrame(results).to_csv(output_path, index=False)
    print(f"Extracted {len(results)} records for {bank_name}.")
    print(f"Results saved at: {output_path}\n")
    print(pd.DataFrame(results))

if __name__ == "__main__":
    print("Credit Card Statement Parser")
    print("Available banks: HDFC, ICICI, SBI, AXIS,KOTAK\n")
    bank_name = input("Enter the bank name to process: ").strip()
    process_bank(bank_name)