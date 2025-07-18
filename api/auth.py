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
            # Importar dependências
            import jwt
            import bcrypt
            
            # 1. Criar usuário
            password = "test-password-123"
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            user = {
                "id": "user-123",
                "email": "test@example.com",
                "full_name": "Test User",
                "password_hash": hashed_password.decode('utf-8'),
                "created_at": datetime.datetime.now().isoformat()
            }
            
            # 2. Verificar senha
            password_valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
            
            # 3. Criar JWT token
            secret = os.getenv("JWT_SECRET_KEY", "vercel-secret-key-123")
            jwt_payload = {
                "sub": user["id"],
                "email": user["email"],
                "name": user["full_name"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            
            access_token = jwt.encode(jwt_payload, secret, algorithm="HS256")
            
            # 4. Criar workspace
            workspace = {
                "id": "workspace-123",
                "name": "Test Workspace",
                "slug": "test-workspace",
                "owner_id": user["id"],
                "created_at": datetime.datetime.now().isoformat()
            }
            
            response = {
                "message": "✅ Fluxo completo de autenticação testado com sucesso no Vercel",
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "full_name": user["full_name"]
                },
                "password_validation": password_valid,
                "access_token": access_token,
                "workspace": workspace,
                "flow_steps": [
                    "1. ✅ Usuário criado",
                    "2. ✅ Senha hasheada",
                    "3. ✅ Senha verificada",
                    "4. ✅ JWT token gerado",
                    "5. ✅ Workspace criado"
                ],
                "platform": "vercel",
                "success": True
            }
            
        except ImportError as e:
            response = {
                "message": "❌ Dependência não encontrada",
                "error": str(e),
                "missing_modules": ["PyJWT", "bcrypt"],
                "solution": "Adicionar dependências ao requirements.txt"
            }
        except Exception as e:
            response = {
                "message": "❌ Erro no fluxo de autenticação",
                "error": str(e),
                "type": type(e).__name__
            }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return