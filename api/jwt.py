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
        
        # Teste simples sem dependências primeiro
        response = {
            "message": "✅ JWT endpoint funcionando no Vercel",
            "status": "testing",
            "timestamp": datetime.datetime.now().isoformat(),
            "test_mode": True
        }
        
        try:
            # Tentar importar JWT
            import jwt
            
            # Se chegou aqui, PyJWT está disponível
            secret = os.getenv("JWT_SECRET_KEY", "vercel-secret-key-123")
            
            payload = {
                "sub": "test-user-123",
                "email": "test@example.com",
                "name": "Test User",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                "iat": datetime.datetime.utcnow()
            }
            
            token = jwt.encode(payload, secret, algorithm="HS256")
            decoded = jwt.decode(token, secret, algorithms=["HS256"])
            
            response.update({
                "message": "✅ JWT token criado com sucesso no Vercel",
                "token": token,
                "payload": payload,
                "decoded": decoded,
                "dependencies_working": True,
                "test_mode": False
            })
            
        except ImportError:
            response.update({
                "message": "❌ PyJWT não disponível",
                "dependencies_working": False,
                "import_error": "PyJWT module not found"
            })
        except Exception as e:
            response.update({
                "message": "❌ Erro no JWT",
                "error": str(e),
                "error_type": type(e).__name__
            })
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return