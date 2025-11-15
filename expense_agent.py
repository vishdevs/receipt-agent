# src/expense_agent.py

import re
import pandas as pd
from .ocr_preprocess import ocr_from_bytes

# Categories and keyword rules
CATEGORIES = {
    "Groceries": ["grocery","supermarket","kirana","veg","vegetable","bread","dairy","milk"],
    "Food": ["restaurant","hotel","dine","cafe","pizza","food","snack"],
    "Bills": ["electricity","water bill","phone bill","utility","bill","gst","invoice"],
    "Transport": ["taxi","auto","uber","ola","bus","fuel","petrol","diesel"],
    "Shopping": ["shop","clothes","mall","fashion","store","shopping"],
    "Health": ["pharmacy","hospital","clinic","medicine","drug"],
}

# Extract amount
def extract_amount(text):
    m = re.search(r'₹\s*([\d,]+\.?\d{0,2})', text)
    if not m:
        m = re.search(r'Rs\.?\s*([\d,]+\.?\d{0,2})', text, flags=re.IGNORECASE)

    if not m:
        nums = re.findall(r'([\d,]+\.\d{1,2})', text)
        if nums:
            return nums[-1].replace(',', '')

        nums2 = re.findall(r'\b([\d,]{2,}\b)', text)
        if nums2:
            return nums2[-1].replace(',', '')

        return ""

    return m.group(1).replace(',', '')

# Extract date
def extract_date(text):
    m = re.search(r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})', text)
    if m:
        return m.group(1)

    m2 = re.search(r'Date[:\s]+([A-Za-z0-9, \-\/]+)', text)
    if m2:
        s = m2.group(1).splitlines()[0].strip()
        return " ".join(s.split()[0:4])

    return ""

# Extract vendor
def extract_vendor(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return ""

    for ln in lines[:4]:
        if re.search(r'[A-Za-z]', ln) and not re.search(r'Invoice|Tax|Total|GST|Bill|Amount', ln, flags=re.IGNORECASE):
            return ln

    return lines[0]

# Category classification
def categorize(text):
    t = text.lower()
    for cat, keys in CATEGORIES.items():
        for k in keys:
            if k in t:
                return cat
    return "Other"

# Process one uploaded image
def process_image_bytes(img_bytes, filename="image"):
    text = ocr_from_bytes(img_bytes)

    return {
        "filename": filename,
        "vendor": extract_vendor(text),
        "date": extract_date(text),
        "amount": extract_amount(text),
        "category": categorize(text),
        "raw_text": text
    }

# Convert list of dicts → clean DataFrame
def records_to_df(records):
    df = pd.DataFrame(records)

    def to_float(a):
        try:
            return float(str(a).replace(',', '').replace('₹', '').strip())
        except:
            return None

    df["amount_val"] = df["amount"].apply(to_float)
    df["date_parsed"] = df["date"].apply(lambda x: x or "")

    return df[[
        "filename",
        "vendor",
        "date_parsed",
        "amount",
        "amount_val",
        "category",
        "raw_text"
    ]]
