# Receipt Agent (Offline)

This is an offline AI agent that scans any receipt image, extracts text using Tesseract OCR, finds the vendor/date/amount, categorizes the expense, and exports a clean CSV file.

## Features
- 100% Offline (No API keys, No cloud)
- Works on mobile using Google Colab
- Tesseract OCR for reading text from receipts
- Auto vendor, date, amount extraction
- Auto category detection (Food, Bills, Transport, etc.)
- CSV export + optional charts

## How to Run (Google Colab)
1. Open `notebooks/Receipt_Agent_Colab.ipynb` in Google Colab.
2. Run all cells in order.
3. Upload receipt images when asked.
4. Download the generated `expenses.csv`.

## Files
- src/ocr_preprocess.py
- src/expense_agent.py
- requirements.txt
- notebooks/Receipt_Agent_Colab.ipynb

## Tech Used
- Python
- Tesseract OCR
- OpenCV
- Pandas
- Matplotlib
