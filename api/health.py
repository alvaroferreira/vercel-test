from http.server import BaseHTTPRequestHandler
import json
import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "healthy",
            "service": "LinkedIn Content Platform API",
            "version": "1.0.0",
            "environment": "production",
            "platform": "vercel",
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return