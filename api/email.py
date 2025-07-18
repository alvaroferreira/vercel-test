from http.server import BaseHTTPRequestHandler
import json
import datetime
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Simulação de integração de email
        response = {
            "message": "✅ Email integration funcionando no Vercel",
            "service": "Gmail API",
            "status": "connected",
            "timestamp": datetime.datetime.now().isoformat(),
            "features": {
                "email_fetch": True,
                "content_extraction": True,
                "ai_processing": True,
                "linkedin_publishing": True
            },
            "test_emails": [
                {
                    "id": "email-123",
                    "subject": "LinkedIn Content Ideas",
                    "from": "test@example.com",
                    "content": "Here are some content ideas for LinkedIn...",
                    "ai_processed": True,
                    "linkedin_ready": True
                },
                {
                    "id": "email-456", 
                    "subject": "Industry Update",
                    "from": "newsletter@industry.com",
                    "content": "Latest industry trends and insights...",
                    "ai_processed": True,
                    "linkedin_ready": True
                }
            ],
            "platform": "vercel"
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return