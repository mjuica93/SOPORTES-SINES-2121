import os
import http.server
import socketserver
import webbrowser
import threading
import time
import json
import hashlib
import secrets
import markdown
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlparse

# Configuración de usuarios
USERS = {
    'admin': {'password': 'sines2024', 'role': 'Administrador'},
    'supervisor': {'password': 'super2024', 'role': 'Supervisor'},
    'operador': {'password': 'op2024', 'role': 'Operador'},
    'sines': {'password': 'sines123', 'role': 'Usuario'}
}

# Almacenamiento de sesiones en memoria
sessions = {}
failed_attempts = {}

def hash_password(password):
    """Hash de contraseña usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_token():
    """Generar token de sesión único"""
    return secrets.token_urlsafe(32)

def log_event(event_type, ip, details=""):
    """Registrar eventos de seguridad"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {event_type} - IP: {ip} - {details}")

class SecureHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Headers de seguridad
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Rutas públicas (no requieren autenticación)
        public_routes = ['/login.html', '/api/status', '/health', '/favicon.ico', '/docs']
        
        # Permitir acceso a documentación sin autenticación
        if path.startswith('/docs/') or path.endswith('.md'):
            return self.handle_documentation(path)
        
        if path in public_routes:
            return self.handle_public_route(path)
        
        # API endpoints
        if path.startswith('/api/'):
            return self.handle_api_request(path)
        
        # Todas las demás rutas requieren autenticación
        if not self.is_authenticated():
            return self.redirect_to_login()
        
        # Redirigir rutas principales
        if path == '/':
            self.path = '/index_isometricos_integrado_final.html'
        elif path == '/sistema-integrado':
            self.path = '/index_isometricos_integrado_final.html'
        elif path == '/mobile':
            self.path = '/index_mobile.html'
        elif path == '/basico':
            self.path = '/index.html'
        
        return super().do_GET()

    def handle_documentation(self, path):
        """Manejar archivos de documentación"""
        try:
            # Mapear rutas de documentación
            doc_mapping = {
                '/docs/': '/LANZAMIENTO_FINAL_v4.1.md',
                '/docs/mejoras': '/MEJORAS_MODAL_COSTURAS.md',
                '/docs/testing': '/TESTING_MODAL_MEJORADO_v4.1.md',
                '/docs/railway': '/GUIA_DESPLIEGUE_RAILWAY_MODAL_v4.1.md',
                '/docs/github': '/RESUMEN_MODAL_COSTURAS_GITHUB.md'
            }
            
            # Si es una ruta de documentación mapeada
            if path in doc_mapping:
                file_path = doc_mapping[path]
            elif path.endswith('.md'):
                file_path = path
            else:
                file_path = '/LANZAMIENTO_FINAL_v4.1.md'  # Default
            
            # Leer archivo markdown
            full_path = os.path.join(os.getcwd(), file_path.lstrip('/'))
            
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                
                # Convertir a HTML
                try:
                    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
                except:
                    # Fallback sin markdown
                    html_content = f"<pre>{md_content}</pre>"
                
                # Crear página HTML completa
                full_html = f"""
                <!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>SINES v4.1 - Documentación</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
                    <style>
                        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
                        .container {{ max-width: 1200px; margin: 20px auto; padding: 20px; }}
                        .nav-docs {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
                        .nav-docs a {{ margin-right: 15px; text-decoration: none; }}
                        pre {{ background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                        code {{ background: #f8f9fa; padding: 2px 4px; border-radius: 3px; }}
                        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                        th {{ background-color: #f8f9fa; }}
                        .back-btn {{ position: fixed; bottom: 20px; right: 20px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="nav-docs">
                            <h5><i class="fas fa-book me-2"></i>Documentación SINES v4.1</h5>
                            <a href="/docs/" class="btn btn-sm btn-outline-primary">📋 Lanzamiento</a>
                            <a href="/docs/mejoras" class="btn btn-sm btn-outline-info">🔧 Mejoras</a>
                            <a href="/docs/testing" class="btn btn-sm btn-outline-success">🧪 Testing</a>
                            <a href="/docs/railway" class="btn btn-sm btn-outline-warning">🚀 Railway</a>
                            <a href="/docs/github" class="btn btn-sm btn-outline-secondary">📦 GitHub</a>
                        </div>
                        <div class="content">
                            {html_content}
                        </div>
                        <a href="/" class="btn btn-primary back-btn">
                            <i class="fas fa-arrow-left me-2"></i>Volver al Sistema
                        </a>
                    </div>
                </body>
                </html>
                """
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(full_html.encode('utf-8'))
                return
            else:
                # Archivo no encontrado
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                error_html = """
                <html><body>
                <h1>Documentación no encontrada</h1>
                <p>El archivo solicitado no existe.</p>
                <a href="/docs/">Volver a la documentación</a>
                </body></html>
                """
                self.wfile.write(error_html.encode('utf-8'))
                return
                
        except Exception as e:
            print(f"Error sirviendo documentación: {e}")
            self.send_response(500)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/login':
            return self.handle_login()
        elif self.path == '/api/logout':
            return self.handle_logout()
        else:
            self.send_response(404)
            self.end_headers()

    def handle_public_route(self, path):
        if path == '/login.html':
            return self.serve_login_page()
        elif path == '/api/status':
            return self.send_json_response({'status': 'ok', 'system': 'SINES v4.1', 'modal': 'mejorado'})
        elif path == '/health':
            return self.send_json_response({'status': 'healthy', 'version': '4.1'})
        elif path == '/docs':
            return self.handle_documentation('/docs/')
        else:
            return super().do_GET()

    def handle_api_request(self, path):
        if path == '/api/validate_session':
            return self.validate_session()
        elif path == '/api/user-info':
            return self.get_user_info()
        else:
            self.send_response(404)
            self.end_headers()

    def is_authenticated(self):
        """Verificar si el usuario está autenticado"""
        cookies = self.get_cookies()
        session_token = cookies.get('session_token')
        
        if not session_token:
            return False
        
        session = sessions.get(session_token)
        if not session:
            return False
        
        # Verificar si la sesión ha expirado
        if datetime.now() > session['expires']:
            del sessions[session_token]
            return False
        
        return True

    def get_cookies(self):
        """Obtener cookies de la petición"""
        cookies = {}
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            for cookie in cookie_header.split(';'):
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    cookies[key] = value
        return cookies

    def redirect_to_login(self):
        """Redirigir a la página de login"""
        self.send_response(302)
        self.send_header('Location', '/login.html')
        self.end_headers()

    def serve_login_page(self):
        """Servir página de login"""
        login_html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SINES v4.1 - Acceso Seguro</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
                .login-container { min-height: 100vh; display: flex; align-items: center; justify-content: center; }
                .login-card { background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
            </style>
        </head>
        <body>
            <div class="login-container">
                <div class="login-card p-5" style="max-width: 400px; width: 100%;">
                    <div class="text-center mb-4">
                        <i class="fas fa-shield-alt fa-3x text-primary mb-3"></i>
                        <h2 class="fw-bold">SISTEMA SINES v4.1</h2>
                        <p class="text-muted">Modal de Costuras Mejorado</p>
                    </div>
                    <form id="loginForm">
                        <div class="mb-3">
                            <label class="form-label">Usuario</label>
                            <input type="text" class="form-control" id="username" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Contraseña</label>
                            <input type="password" class="form-control" id="password" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">
                            <i class="fas fa-sign-in-alt me-2"></i>Acceder
                        </button>
                    </form>
                    <div class="mt-3 text-center">
                        <small class="text-muted">Modal responsivo implementado</small>
                        <br>
                        <a href="/docs/" class="btn btn-sm btn-outline-info mt-2">
                            <i class="fas fa-book me-1"></i>Ver Documentación
                        </a>
                    </div>
                </div>
            </div>
            <script>
                document.getElementById('loginForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const username = document.getElementById('username').value;
                    const password = document.getElementById('password').value;
                    
                    try {
                        const response = await fetch('/api/login', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ username, password })
                        });
                        
                        const data = await response.json();
                        if (data.success) {
                            document.cookie = `session_token=${data.token}; path=/; max-age=1800`;
                            window.location.href = '/';
                        } else {
                            alert('Credenciales incorrectas');
                        }
                    } catch (error) {
                        alert('Error de conexión');
                    }
                });
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(login_html.encode('utf-8'))

    def handle_login(self):
        """Manejar solicitud de login"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            username = data.get('username')
            password = data.get('password')
            client_ip = self.client_address[0]
            
            # Verificar intentos fallidos
            if client_ip in failed_attempts:
                if failed_attempts[client_ip]['count'] >= 5:
                    if datetime.now() < failed_attempts[client_ip]['blocked_until']:
                        return self.send_json_response({
                            'success': False,
                            'error': 'IP bloqueada temporalmente'
                        })
            
            # Verificar credenciales
            if username in USERS and USERS[username]['password'] == password:
                # Login exitoso
                session_token = generate_session_token()
                sessions[session_token] = {
                    'username': username,
                    'role': USERS[username]['role'],
                    'created': datetime.now(),
                    'expires': datetime.now() + timedelta(minutes=30),
                    'ip': client_ip
                }
                
                # Limpiar intentos fallidos
                if client_ip in failed_attempts:
                    del failed_attempts[client_ip]
                
                log_event('LOGIN_SUCCESS', client_ip, f'Usuario: {username} ({USERS[username]["role"]})')
                
                return self.send_json_response({
                    'success': True,
                    'token': session_token,
                    'user': {
                        'username': username,
                        'role': USERS[username]['role']
                    }
                })
            else:
                # Login fallido
                if client_ip not in failed_attempts:
                    failed_attempts[client_ip] = {'count': 0, 'blocked_until': None}
                
                failed_attempts[client_ip]['count'] += 1
                if failed_attempts[client_ip]['count'] >= 5:
                    failed_attempts[client_ip]['blocked_until'] = datetime.now() + timedelta(minutes=15)
                
                log_event('LOGIN_FAILED', client_ip, f'Usuario: {username}')
                
                return self.send_json_response({
                    'success': False,
                    'error': 'Credenciales incorrectas'
                })
                
        except Exception as e:
            log_event('LOGIN_ERROR', self.client_address[0], str(e))
            return self.send_json_response({
                'success': False,
                'error': 'Error interno del servidor'
            })

    def handle_logout(self):
        """Manejar cierre de sesión"""
        cookies = self.get_cookies()
        session_token = cookies.get('session_token')
        
        if session_token and session_token in sessions:
            username = sessions[session_token]['username']
            del sessions[session_token]
            log_event('LOGOUT', self.client_address[0], f'Usuario: {username}')
        
        return self.send_json_response({'success': True})

    def validate_session(self):
        """Validar sesión actual"""
        if self.is_authenticated():
            return self.send_json_response({'valid': True})
        else:
            self.send_response(401)
            self.end_headers()

    def get_user_info(self):
        """Obtener información del usuario actual"""
        cookies = self.get_cookies()
        session_token = cookies.get('session_token')
        
        if session_token and session_token in sessions:
            session = sessions[session_token]
            return self.send_json_response({
                'username': session['username'],
                'role': session['role']
            })
        else:
            self.send_response(401)
            self.end_headers()

    def send_json_response(self, data):
        """Enviar respuesta JSON"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def cleanup_expired_sessions():
    """Limpiar sesiones expiradas"""
    while True:
        time.sleep(300)  # Cada 5 minutos
        current_time = datetime.now()
        expired_sessions = [token for token, session in sessions.items() 
                          if current_time > session['expires']]
        
        for token in expired_sessions:
            username = sessions[token]['username']
            del sessions[token]
            print(f"🕐 Sesión expirada: {username}")

def start_server():
    # Railway proporciona el puerto a través de la variable de entorno PORT
    PORT = int(os.environ.get('PORT', 8000))
    
    try:
        # Iniciar limpieza de sesiones en hilo separado
        cleanup_thread = threading.Thread(target=cleanup_expired_sessions)
        cleanup_thread.daemon = True
        cleanup_thread.start()
        
        with socketserver.TCPServer(("", PORT), SecureHTTPRequestHandler) as httpd:
            print("=" * 60)
            print("🏗️  SISTEMA SINES v4.1 - RAILWAY DEPLOYMENT")
            print("=" * 60)
            print(f"🌐 Servidor iniciado en puerto {PORT}")
            print(f"📂 Sirviendo archivos desde: {os.getcwd()}")
            print("✅ Sistema SINES v4.1 con modal mejorado!")
            print("🔐 Autenticación obligatoria activada")
            print("📋 Documentación pública disponible")
            print("🏭 Funcionalidades:")
            print("   ├─ 🔧 Soportes agrupados con variables de plantilla")
            print("   ├─ 📐 Isométricos y relaciones completas")
            print("   ├─ ⚡ Control de costuras mejorado para campo")
            print("   ├─ 🔗 Instalaciones y trazabilidad")
            print("   └─ 🛡️ Sistema de seguridad completo")
            print(f"🎯 Acceso local: http://localhost:{PORT}")
            print("🌍 URLs Railway:")
            print("   ├─ Sistema: https://tu-proyecto.railway.app/")
            print("   ├─ Móvil: https://tu-proyecto.railway.app/mobile")
            print("   ├─ Integrado: https://tu-proyecto.railway.app/sistema-integrado")
            print("   ├─ Básico: https://tu-proyecto.railway.app/basico")
            print("   └─ Docs: https://tu-proyecto.railway.app/docs/")
            print("🔐 Credenciales:")
            print("   ├─ admin / sines2024 (Administrador)")
            print("   ├─ supervisor / super2024 (Supervisor)")
            print("   ├─ operador / op2024 (Operador)")
            print("   └─ sines / sines123 (Usuario)")
            print("=" * 60)
            
            # En Railway no necesitamos abrir navegador
            if os.environ.get('RAILWAY_ENVIRONMENT') != 'production':
                # Solo abrir navegador en desarrollo local
                def open_browser():
                    time.sleep(1)
                    webbrowser.open(f'http://localhost:{PORT}')
                
                browser_thread = threading.Thread(target=open_browser)
                browser_thread.daemon = True
                browser_thread.start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")
        # En Railway, es importante que el proceso termine con error si no puede iniciar
        exit(1)

if __name__ == "__main__":
    print("=== SISTEMA SINES v4.1 - RAILWAY DEPLOYMENT ===")
    print("🏭 Modal de Costuras Mejorado + Documentación Accesible")
    start_server() 