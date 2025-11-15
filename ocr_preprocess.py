# src/ocr_preprocess.py

import io
from PIL import Image
import cv2
import numpy as np
import pytesseract

def preprocess_bytes(img_bytes):
    """
    Converts uploaded image bytes into a clean preprocessed image
    ready for OCR.
    """
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    arr = np.array(img)[:, :, ::-1]  # RGB → BGR for OpenCV
    gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)
    
    # Adaptive threshold for clean text
    processed = cv2.adaptiveThreshold(
        blur, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 2
    )
    return processed

def ocr_from_bytes(img_bytes, lang='eng'):
    """
    Runs OCR on preprocessed image bytes and returns extracted text.
    """
    processed_img = preprocess_bytes(img_bytes)
    pil_img = Image.fromarray(processed_img)
    text = pytesseract.image_to_string(pil_img, lang=lang)
    return text
