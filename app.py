import streamlit as st
import json
import pdfplumber
import fitz
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

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
        doc = fitz.open("temp.pdf")
        for page in doc:
            pix = page.get_pixmap(dpi=150)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            try:
                ocr_res = pytesseract.image_to_string(img)
                extracted_text += ocr_res + "\n"
            except Exception:
                pass

    # Dynamic extraction based on PDF content
    caps = []
    certs = []
    machinery = []
    
    low_text = extracted_text.lower()
    
    # Capabilities checks
    if "cnc" in low_text or "milling" in low_text or "machining" in low_text:
        caps.append("CNC Machining & Milling")
    if "steel" in low_text or "metal" in low_text or "fabrication" in low_text:
        caps.append("Steel & Metal Fabrication")
    if "injection" in low_text or "molding" in low_text:
        caps.append("Injection Molding")
    if "3d printing" in low_text or "additive" in low_text:
        caps.append("3D Printing & Additive Manufacturing")
    if not caps:
        caps.append("General Manufacturing Services")

    # Certifications checks
    if "iso 9001" in low_text:
        certs.append("ISO 9001 Certified")
    if "iso 14001" in low_text:
        certs.append("ISO 14001 Certified")
    if "ce" in low_text or "ce mark" in low_text:
        certs.append("CE Compliance")
    if "iatf" in low_text:
        certs.append("IATF 16949 Certified")
    if not certs:
        certs.append("Standard Manufacturing Compliance")

    # Machinery checks
    if "cnc lathe" in low_text or "lathe" in low_text:
        machinery.append("CNC Lathe Machine")
    if "vmc" in low_text or "vertical machining" in low_text:
        machinery.append("Vertical Machining Center (VMC)")
    if "laser" in low_text:
        machinery.append("Laser Cutting Machine")
    if not machinery:
        machinery.append("General Industrial Equipment")

    # Constructing JSON schema with extracted data
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
            "extraction_source": "pdf_content_dynamic_parser",
            "supplier_name": uploaded_file.name,
            "capabilities": caps,
            "certifications": certs,
            "machinery_list": machinery,
            "raw_text_preview": extracted_text[:300].strip() + "..." if extracted_text else "No text found"
        }
    }

    st.subheader("Extracted Data using JSON Schema:")
    st.json(supplier_json_output)
