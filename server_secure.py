import http.server
import socketserver
import webbrowser
import os
import threading
import time
import json
import hashlib
import secrets
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta

class SecureHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Configuración de seguridad
        self.SECURITY_CONFIG = {
            'max_attempts': 3,
            'lockout_time': 300,  # 5 minutos
            'session_timeout': 1800,  # 30 minutos
            'users': {
                'admin': {
                    'password_hash': self.hash_password('sines2024'),
                    'role': 'administrator',
                    'name': 'Administrador'
                },
                'supervisor': {
                    'password_hash': self.hash_password('super2024'),
                    'role': 'supervisor', 
                    'name': 'Supervisor'
                },
                'operador': {
                    'password_hash': self.hash_password('op2024'),
                    'role': 'operator',
                    'name': 'Operador'
                },
                'sines': {
                    'password_hash': self.hash_password('sines123'),
                    'role': 'user',
                    'name': 'Usuario SINES'
                }
            }
        }
        
        # Estado de seguridad
        self.failed_attempts = {}
        self.lockout_times = {}
        self.active_sessions = {}
        
        super().__init__(*args, **kwargs)
    
    def hash_password(self, password):
        """Hash de contraseña con salt"""
        salt = "sines_salt_2024"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def generate_session_token(self):
        """Generar token de sesión seguro"""
        return secrets.token_urlsafe(32)
    
    def log_security_event(self, event_type, username=None, ip=None, details=None):
        """Registrar eventos de seguridad"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'username': username,
            'ip': ip or self.client_address[0],
            'details': details
        }
        
        # En producción, esto iría a un archivo de log o base de datos
        print(f"🔒 SECURITY LOG: {log_entry}")
    
    def is_locked_out(self, username):
        """Verificar si el usuario está bloqueado"""
        if username in self.lockout_times:
            if datetime.now() < self.lockout_times[username]:
                return True
            else:
                # Bloqueo expirado
                del self.lockout_times[username]
                if username in self.failed_attempts:
                    del self.failed_attempts[username]
        return False
    
    def authenticate_user(self, username, password):
        """Autenticar usuario"""
        if self.is_locked_out(username):
            return False, "Usuario bloqueado"
        
        user = self.SECURITY_CONFIG['users'].get(username.lower())
        if not user:
            return False, "Usuario no encontrado"
        
        password_hash = self.hash_password(password)
        if user['password_hash'] == password_hash:
            # Login exitoso - limpiar intentos fallidos
            if username in self.failed_attempts:
                del self.failed_attempts[username]
            return True, "Autenticación exitosa"
        else:
            # Login fallido
            self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
            
            if self.failed_attempts[username] >= self.SECURITY_CONFIG['max_attempts']:
                # Bloquear usuario
                self.lockout_times[username] = datetime.now() + timedelta(seconds=self.SECURITY_CONFIG['lockout_time'])
                self.log_security_event('USER_LOCKED', username, details=f"Intentos fallidos: {self.failed_attempts[username]}")
                return False, f"Usuario bloqueado por {self.SECURITY_CONFIG['lockout_time']//60} minutos"
            
            remaining = self.SECURITY_CONFIG['max_attempts'] - self.failed_attempts[username]
            return False, f"Contraseña incorrecta. {remaining} intentos restantes"
    
    def create_session(self, username):
        """Crear sesión de usuario"""
        token = self.generate_session_token()
        user = self.SECURITY_CONFIG['users'][username.lower()]
        
        session = {
            'token': token,
            'username': username,
            'role': user['role'],
            'name': user['name'],
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'ip': self.client_address[0]
        }
        
        self.active_sessions[token] = session
        self.log_security_event('SESSION_CREATED', username)
        return token, session
    
    def validate_session(self, token):
        """Validar sesión"""
        if not token or token not in self.active_sessions:
            return False, None
        
        session = self.active_sessions[token]
        
        # Verificar timeout
        if datetime.now() - session['last_activity'] > timedelta(seconds=self.SECURITY_CONFIG['session_timeout']):
            del self.active_sessions[token]
            self.log_security_event('SESSION_EXPIRED', session['username'])
            return False, None
        
        # Actualizar actividad
        session['last_activity'] = datetime.now()
        return True, session
    
    def destroy_session(self, token):
        """Destruir sesión"""
        if token in self.active_sessions:
            username = self.active_sessions[token]['username']
            del self.active_sessions[token]
            self.log_security_event('SESSION_DESTROYED', username)
    
    def end_headers(self):
        """Headers de seguridad"""
        # Headers de seguridad
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        
        # CORS para desarrollo local
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        
        # Cache control
        if self.path.endswith(('.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf')):
            self.send_header('Cache-Control', 'public, max-age=3600')
        else:
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        
        super().end_headers()
    
    def do_POST(self):
        """Manejar requests POST para autenticación"""
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/api/login':
            self.handle_login()
        elif parsed_url.path == '/api/logout':
            self.handle_logout()
        elif parsed_url.path == '/api/validate':
            self.handle_validate()
        else:
            self.send_error(404, "Endpoint not found")
    
    def handle_login(self):
        """Manejar login"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            if not username or not password:
                self.send_json_response({
                    'success': False,
                    'message': 'Usuario y contraseña requeridos'
                }, 400)
                return
            
            # Intentar autenticación
            success, message = self.authenticate_user(username, password)
            
            if success:
                token, session = self.create_session(username)
                self.log_security_event('LOGIN_SUCCESS', username)
                
                self.send_json_response({
                    'success': True,
                    'message': 'Login exitoso',
                    'token': token,
                    'user': {
                        'username': session['username'],
                        'name': session['name'],
                        'role': session['role']
                    }
                })
            else:
                self.log_security_event('LOGIN_FAILED', username, details=message)
                self.send_json_response({
                    'success': False,
                    'message': message
                }, 401)
                
        except Exception as e:
            self.log_security_event('LOGIN_ERROR', details=str(e))
            self.send_json_response({
                'success': False,
                'message': 'Error interno del servidor'
            }, 500)
    
    def handle_logout(self):
        """Manejar logout"""
        try:
            # Obtener token del header Authorization
            auth_header = self.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
                self.destroy_session(token)
            
            self.send_json_response({
                'success': True,
                'message': 'Logout exitoso'
            })
            
        except Exception as e:
            self.log_security_event('LOGOUT_ERROR', details=str(e))
            self.send_json_response({
                'success': False,
                'message': 'Error en logout'
            }, 500)
    
    def handle_validate(self):
        """Validar sesión"""
        try:
            auth_header = self.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                self.send_json_response({
                    'success': False,
                    'message': 'Token no proporcionado'
                }, 401)
                return
            
            token = auth_header[7:]
            valid, session = self.validate_session(token)
            
            if valid:
                self.send_json_response({
                    'success': True,
                    'user': {
                        'username': session['username'],
                        'name': session['name'],
                        'role': session['role']
                    }
                })
            else:
                self.send_json_response({
                    'success': False,
                    'message': 'Sesión inválida o expirada'
                }, 401)
                
        except Exception as e:
            self.log_security_event('VALIDATION_ERROR', details=str(e))
            self.send_json_response({
                'success': False,
                'message': 'Error de validación'
            }, 500)
    
    def send_json_response(self, data, status_code=200):
        """Enviar respuesta JSON"""
        response = json.dumps(data).encode('utf-8')
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)
    
    def do_GET(self):
        """Manejar requests GET con verificación de seguridad"""
        parsed_url = urlparse(self.path)
        
        # Rutas públicas (no requieren autenticación)
        public_paths = [
            '/index_isometricos_secure.html',
            '/favicon.ico'
        ]
        
        # Archivos estáticos públicos
        if any(self.path.startswith(path) for path in public_paths) or \
           self.path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico')):
            super().do_GET()
            return
        
        # API endpoints de estado
        if parsed_url.path == '/api/status':
            self.send_json_response({
                'status': 'running',
                'security': 'enabled',
                'active_sessions': len(self.active_sessions)
            })
            return
        
        # Verificar autenticación para rutas protegidas
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            valid, session = self.validate_session(token)
            
            if valid:
                # Usuario autenticado, permitir acceso
                super().do_GET()
                return
        
        # Redirigir a página de login para rutas protegidas
        if self.path == '/' or not self.path.startswith('/index_isometricos_secure.html'):
            self.send_response(302)
            self.send_header('Location', '/index_isometricos_secure.html')
            self.end_headers()
        else:
            super().do_GET()

def start_secure_server():
    PORT = 8001
    
    try:
        with socketserver.TCPServer(("", PORT), SecureHTTPRequestHandler) as httpd:
            print("🔒 SERVIDOR SEGURO SINES INICIADO")
            print("=" * 50)
            print(f"🌐 URL: http://localhost:{PORT}")
            print(f"🔐 Página de acceso: http://localhost:{PORT}/index_isometricos_secure.html")
            print(f"📂 Directorio: {os.getcwd()}")
            print("\n🔑 CREDENCIALES DE ACCESO:")
            print("┌─────────────┬──────────────┬───────────────┐")
            print("│ Usuario     │ Contraseña   │ Rol           │")
            print("├─────────────┼──────────────┼───────────────┤")
            print("│ admin       │ sines2024    │ Administrador │")
            print("│ supervisor  │ super2024    │ Supervisor    │")
            print("│ operador    │ op2024       │ Operador      │")
            print("│ sines       │ sines123     │ Usuario       │")
            print("└─────────────┴──────────────┴───────────────┘")
            print("\n🛡️ CARACTERÍSTICAS DE SEGURIDAD:")
            print("• Autenticación de usuarios")
            print("• Sesiones con timeout (30 min)")
            print("• Bloqueo tras 3 intentos fallidos")
            print("• Registro de eventos de seguridad")
            print("• Headers de seguridad HTTP")
            print("\n🚀 Abriendo navegador...")
            
            # Abrir navegador después de un breve delay
            def open_browser():
                time.sleep(2)
                webbrowser.open(f'http://localhost:{PORT}/index_isometricos_secure.html')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.start()
            
            print("\n⚠️  Para detener el servidor: Presiona Ctrl+C")
            print("=" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor seguro detenido")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ El puerto {PORT} ya está en uso.")
            print("💡 Cierra otros servidores o usa otro puerto.")
        else:
            print(f"❌ Error al iniciar servidor: {e}")

if __name__ == "__main__":
    start_secure_server() 