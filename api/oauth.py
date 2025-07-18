from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            # Configurações OAuth
            client_id = os.getenv("GMAIL_CLIENT_ID", "test-client-id.apps.googleusercontent.com")
            redirect_uri = "https://vercel-test.vercel.app/api/callback"
            
            # URL OAuth do Google
            base_url = "https://accounts.google.com/o/oauth2/v2/auth"
            params = {
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "scope": "email profile",
                "state": "test-state-123456"
            }
            
            # Construir URL completa
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            google_oauth_url = f"{base_url}?{query_string}"
            
            # LinkedIn OAuth
            linkedin_oauth_url = f"https://www.linkedin.com/oauth/v2/authorization?client_id=test-linkedin-client&redirect_uri={redirect_uri}&response_type=code&scope=r_liteprofile%20r_emailaddress&state=test-state-123456"
            
            response = {
                "message": "✅ URLs OAuth geradas com sucesso no Vercel",
                "google_oauth": google_oauth_url,
                "linkedin_oauth": linkedin_oauth_url,
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "state": "test-state-123456"
            }
            
        except Exception as e:
            response = {
                "message": "❌ Erro ao gerar OAuth URLs",
                "error": str(e),
                "type": type(e).__name__
            }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return