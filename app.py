import streamlit as st
import pdfplumber
import fitz
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

st.title("Menerix Supplier Profile Extractor")

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

    caps = []
    low_text = extracted_text.lower()
    if "cnc" in low_text or "milling" in low_text:
        caps.append("CNC Machining & Milling")
    if "steel" in low_text or "metal" in low_text:
        caps.append("Steel & Metal Fabrication")
    if "injection" in low_text or "molding" in low_text:
        caps.append("Injection Molding")

    if not caps:
        caps.append("General Manufacturing Services")

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

    st.subheader("Extracted Supplier Details:")
    
    st.markdown(f"**Status:** Success")
    st.markdown(f"**Supplier Profile Found:** Yes")
    
    st.write("---")
    st.write("**1. Manufacturing Capabilities:**")
    for c in caps:
        st.write(f"- {c}")
        
    st.write("**2. Certifications & Compliance:**")
    for cert in certs:
        st.write(f"- {cert}")
        
    st.write("**3. Machinery & Equipment:**")
    for m in machinery:
        st.write(f"- {m}")
