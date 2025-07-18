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
        
        try:
            # Importar JWT (PyJWT)
            import jwt
            
            # Configurações JWT
            secret = os.getenv("JWT_SECRET_KEY", "vercel-secret-key-123")
            
            # Payload do token
            payload = {
                "sub": "test-user-123",
                "email": "test@example.com",
                "name": "Test User",
                "workspace_id": "test-workspace-456",
                "role": "admin",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                "iat": datetime.datetime.utcnow()
            }
            
            # Criar token
            token = jwt.encode(payload, secret, algorithm="HS256")
            
            # Verificar token
            decoded = jwt.decode(token, secret, algorithms=["HS256"])
            
            response = {
                "message": "✅ JWT token criado com sucesso no Vercel",
                "token": token,
                "payload": payload,
                "decoded": decoded,
                "token_length": len(token),
                "secret_used": "vercel-secret-key-123",
                "dependencies_working": True
            }
            
        except ImportError as e:
            response = {
                "message": "❌ PyJWT não está instalado no Vercel",
                "error": str(e),
                "solution": "Vercel needs to install PyJWT from requirements.txt",
                "requirements_file": "requirements.txt exists with PyJWT==2.8.0",
                "dependencies_working": False
            }
        except Exception as e:
            response = {
                "message": "❌ Erro ao criar JWT",
                "error": str(e),
                "type": type(e).__name__
            }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return