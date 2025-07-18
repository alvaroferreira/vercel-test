from http.server import BaseHTTPRequestHandler
import json
import datetime
import os
import base64
import hmac
import hashlib

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            # Criar JWT simples sem dependências externas
            secret = os.getenv("JWT_SECRET_KEY", "vercel-secret-key-123")
            
            # Header JWT
            header = {
                "alg": "HS256",
                "typ": "JWT"
            }
            
            # Payload JWT
            payload = {
                "sub": "test-user-123",
                "email": "test@example.com",
                "name": "Test User",
                "workspace_id": "test-workspace-456",
                "role": "admin",
                "exp": int((datetime.datetime.utcnow() + datetime.timedelta(hours=1)).timestamp()),
                "iat": int(datetime.datetime.utcnow().timestamp())
            }
            
            # Codificar em base64
            header_b64 = base64.urlsafe_b64encode(
                json.dumps(header, separators=(',', ':')).encode()
            ).decode().rstrip('=')
            
            payload_b64 = base64.urlsafe_b64encode(
                json.dumps(payload, separators=(',', ':')).encode()
            ).decode().rstrip('=')
            
            # Criar assinatura
            message = f"{header_b64}.{payload_b64}"
            signature = hmac.new(
                secret.encode(),
                message.encode(),
                hashlib.sha256
            ).digest()
            
            signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
            
            # Token JWT completo
            token = f"{header_b64}.{payload_b64}.{signature_b64}"
            
            response = {
                "message": "✅ JWT token criado com sucesso no Vercel (sem dependências)",
                "token": token,
                "payload": payload,
                "header": header,
                "token_length": len(token),
                "method": "native_python",
                "dependencies_working": True,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            response = {
                "message": "❌ Erro ao criar JWT",
                "error": str(e),
                "error_type": type(e).__name__,
                "timestamp": datetime.datetime.now().isoformat()
            }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return