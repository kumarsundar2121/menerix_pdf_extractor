import json
import pdfplumber
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            pdf_path = "sample.pdf"
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"

            found_capabilities = []
            if "cnc" in full_text.lower() or "milling" in full_text.lower():
                found_capabilities.append("CNC Machining & Milling")
            if "steel" in full_text.lower() or "metal" in full_text.lower():
                found_capabilities.append("Steel & Metal Fabrication")
            if "injection" in full_text.lower() or "molding" in full_text.lower():
                found_capabilities.append("Injection Molding")

            if not found_capabilities:
                found_capabilities = ["General Manufacturing Services"]

            supplier_json_schema = {
                "supplier_profile": {
                    "status": "success",
                    "extraction_source": "brochure_pdf",
                    "capabilities": found_capabilities,
                    "raw_text_preview": full_text[:300].strip() + "..." if full_text else "No text found"
                }
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(supplier_json_schema, indent=4).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
