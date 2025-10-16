

# Credit Card Statement Parser

## 1. Introduction

The **Credit Card Statement Parser** is a Python-based system designed to extract important information automatically from **PDF credit card statements**.
It can handle **multiple banks** and **multiple cardholders within a single PDF**, demonstrating data extraction from real-world unstructured documents.

This project helps automate the tedious task of manually reading and recording data from financial statements by using **text parsing** and **regular expressions**.
The extracted data is structured and displayed neatly on a **web interface** built using **Streamlit**, with an option to download the extracted results in CSV format.

---

## 2. Objective

The main objective of this project is to:

* Parse credit card statement PDFs of different banks.
* Extract key data fields such as:

  * Cardholder Name
  * Last 4 Digits of Card
  * Statement/Billing Period
  * Total Amount Due
  * Payment Due Date
* Display the extracted results in a user-friendly web interface.
* Allow the user to download the extracted data for further analysis.

---

## 3. Tools and Technologies Used

| Category             | Tool/Technology              | Purpose                              |
| -------------------- | ---------------------------- | ------------------------------------ |
| Programming Language | **Python 3.x**               | Core language used for development   |
| PDF Text Extraction  | **pdfplumber**               | Extracts text from PDF statements    |
| Data Handling        | **pandas**                   | Stores and processes extracted data  |
| Pattern Matching     | **re (Regular Expressions)** | Identifies key text patterns in PDF  |
| Frontend Framework   | **Streamlit**                | Builds the interactive web interface |
| Text Editor / IDE    | **VS Code / PyCharm**        | For writing and debugging code       |
| Version Control      | **Git** *(optional)*         | For maintaining version history      |

---

## 4. Installation Steps


### Step 1: Clone or Create the Project Folder

If you have a repository:

```bash
git clone <repository-url>
cd CreditCardParser
```

Or manually create a folder named `CreditCardParser` and place your files inside.

### Step 2: Install Required Libraries

Open a terminal in your project directory and run:

```bash
pip install streamlit pdfplumber pandas reportlab
```

Alternatively, create a **requirements.txt** file:

```
streamlit
pdfplumber
pandas
reportlab
```

Then install all at once:

```bash
pip install -r requirements.txt
```

### Step 3: Add PDF Files

Place all your PDF statements inside the `data/` folder.
You can use your own PDFs or the dummy ones (HDFC, ICICI, SBI, Axis, Amex).

---

## 5. Running the Project

You can run the system in two modes:

### Option A: Web Application Mode (Recommended)

#### Step 1: Run Streamlit App

```bash
streamlit run app.py
```

#### Step 2: Open the Browser

After running the command, Streamlit will automatically open a local web server, usually:

```
http://localhost:8501
```

#### Step 3: Use the Interface

1. Upload any bank’s PDF statement (e.g., `hdfc_multi_cards.pdf`).
2. Wait for the parser to process the file.
3. View the extracted data in a table.
4. Download the results as a CSV.

---

### Option B: Command-Line Mode

If you don’t want to use the web interface, you can run the backend directly:

```bash
python main.py
```

Then:

* Enter the bank name when prompted.
* The extracted results will be saved in `/output/` as a CSV file.

---

## 6. How It Works

### Step 1: PDF Extraction

The system uses `pdfplumber` to read text from each page of the PDF.

### Step 2: Block Splitting

The extracted text is divided into sections using the header **“Cardholder Name:”**, allowing multiple records to be processed from one file.

### Step 3: Regex Matching

Regular expressions identify and extract the following details:

* Cardholder Name
* Last 4 digits of the card number
* Statement/Billing Period
* Payment Due Date
* Total Amount Due

### Step 4: Data Structuring

The parsed data is organized into a pandas DataFrame.

### Step 5: Display & Export

The data is displayed on the Streamlit interface, and users can export it as a CSV file.

---

## 7. Example Output

| Record # | Cardholder Name | Last 4 Digits | Statement Period           | Payment Due Date | Total Amount Due |
| -------- | --------------- | ------------- | -------------------------- | ---------------- | ---------------- |
| 1        | Rahul Sharma    | 5678          | 01-Sep-2025 to 30-Sep-2025 | 15-Oct-2025      | 54750            |
| 2        | Priya Mehta     | 7823          | 03-Sep-2025 to 02-Oct-2025 | 18-Oct-2025      | 31600            |
| 3        | Ankit Verma     | 9821          | 05-Sep-2025 to 04-Oct-2025 | 20-Oct-2025      | 26875            |
| 4        | Sonali Kapoor   | 3345          | 07-Sep-2025 to 06-Oct-2025 | 22-Oct-2025      | 42990            |
| 5        | Ritesh Nair     | 1234          | 10-Sep-2025 to 09-Oct-2025 | 25-Oct-2025      | 61440            |

---

## 8. Future Enhancements

* Add Optical Character Recognition (OCR) for scanned PDFs using `pytesseract`.
* Include dynamic regex templates for different banks.
* Add a summary dashboard to visualize monthly expenses.
* Support JSON and Excel export.
* Deploy the web app using Streamlit Cloud or AWS.

---
