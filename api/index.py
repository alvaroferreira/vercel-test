from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "message": "🚀 LinkedIn Content Platform API está funcionando!",
            "version": "1.0.0",
            "status": "healthy",
            "platform": "vercel",
            "endpoints": {
                "health": "/api/health",
                "jwt_test": "/api/jwt",
                "oauth_test": "/api/oauth",
                "full_auth": "/api/auth",
                "email_integration": "/api/email",
                "linkedin_publishing": "/api/linkedin",
                "ai_processing": "/api/ai"
            }
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return