import streamlit as st
import json
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

st.title("Menerix PDF Extractor & JSON Schema Generator")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    extracted_text = ""
    
    with pdfplumber.open("temp.pdf") as pdf:
        for p in pdf.pages:
            t = p.extract_text()
            if t:
                extracted_text += t + "\n"
                
    if not extracted_text.strip():
        pages = convert_from_path("temp.pdf")
        for img in pages:
            ocr_res = pytesseract.image_to_string(img)
            extracted_text += ocr_res + "\n"
            
    caps = []
    low_text = extracted_text.lower()
    if "cnc" in low_text or "milling" in low_text:
        caps.append("CNC Machining & Milling")
    if "steel" in low_text or "metal" in low_text:
        caps.append("Steel & Metal Fabrication")
    if "injection" in low_text or "molding" in low_text:
        caps.append("Injection Molding")

    if not caps:
        caps = ["General Manufacturing Services"]

    certs = []
    if "iso" in low_text or "ce" in low_text:
        certs.append("ISO 9001 / CE Certified")
    else:
        certs.append("Standard Manufacturing Compliance")

    machinery = []
    if "cnc" in low_text:
        machinery.append("CNC Machining Center")
    if "lathe" in low_text:
        machinery.append("Lathe Machine")
    if not machinery:
        machinery.append("General Industrial Equipment")

    supplier_json_output = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "SupplierProfileExtraction",
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "extraction_source": {"type": "string"},
            "supplier_name": {"type": "string"},
            "capabilities": {"type": "array", "items": {"type": "string"}},
            "certifications": {"type": "array", "items": {"type": "string"}},
            "machinery_list": {"type": "array", "items": {"type": "string"}},
            "raw_text_preview": {"type": "string"}
        },
        "supplier_profile": {
            "status": "success",
            "extraction_source": "streamlit_ocr_hybrid_parser",
            "supplier_name": "Extracted Supplier Profile",
            "capabilities": caps,
            "certifications": certs,
            "machinery_list": machinery,
            "raw_text_preview": extracted_text[:300].strip() + "..." if extracted_text else "No text found"
        }
    }

    st.subheader("Generated JSON Schema & Extracted Data Output:")
    st.json(supplier_json_output)
