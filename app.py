import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            response_data = {
                "status": "success",
                "message": "Render Server is running successfully!"
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
    print(f"Server started on port {port}")
    server.serve_forever()
