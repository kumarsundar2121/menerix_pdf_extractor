import json
import fitz
from http.server import BaseHTTPRequestHandler

def extract_logic():
    try:
        pdf_file = "sample.pdf"
        extracted_text = ""
        
        doc = fitz.open(pdf_file)
        for page in doc:
            extracted_text += page.get_text() + "\n"

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

        response_data = {
            "supplier_profile": {
                "status": "success",
                "extraction_source": "pymupdf_parser",
                "supplier_name": "Extracted Supplier Profile",
                "capabilities": caps,
                "certifications": certs,
                "machinery_list": machinery,
                "raw_text_preview": extracted_text[:300].strip() + "..." if extracted_text else "No text found"
            }
        }
        return response_data
    except Exception as err:
        return {"status": "error", "message": str(err)}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        result = extract_logic()
        self.send_response(200 if "supplier_profile" in result else 500)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result, indent=4).encode('utf-8'))

if __name__ == '__main__':
    print(json.dumps(extract_logic(), indent=4))
