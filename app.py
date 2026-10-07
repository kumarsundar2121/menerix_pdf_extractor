import os
import json
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            pdf_file = os.path.join(os.path.dirname(__file__), "sample.pdf")
            extracted_text = ""

            if os.path.exists(pdf_file):
                with pdfplumber.open(pdf_file) as pdf:
                    for p in pdf.pages:
                        t = p.extract_text()
                        if t:
                            extracted_text += t + "\n"

                if not extracted_text.strip():
                    pages = convert_from_path(pdf_file)
                    for img in pages:
                        ocr_res = pytesseract.image_to_string(img)
                        extracted_text += ocr_res + "\n"
            else:
                extracted_text = "Error: sample.pdf file not found in root directory."

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
                    "extraction_source": "render_ocr_hybrid_parser",
                    "supplier_name": "Extracted Supplier Profile",
                    "capabilities": caps,
                    "certifications": certs,
                    "machinery_list": machinery,
                    "raw_text_preview": extracted_text[:300].strip() + "..." if extracted_text else "No text found"
                }
            }

            output = json.dumps(response_data, indent=4).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Length', str(len(output)))
            self.end_headers()
            self.wfile.write(output)

        except Exception as e:
            err_output = json.dumps({"status": "error", "message": str(e)}).encode('utf-8')
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(err_output)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()
