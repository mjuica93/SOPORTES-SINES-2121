#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Seguro Híbrido para Sistema SINES
Versión que funciona correctamente con ventanas múltiples
"""

import http.server
import socketserver
import webbrowser
import os
import threading
import time
import json
import hashlib
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta

class HybridSecureHandler(http.server.SimpleHTTPRequestHandler):
    # Usuarios del sistema
    USERS = {
        'admin': {'password': 'sines2024', 'name': 'Administrador'},
        'supervisor': {'password': 'super2024', 'name': 'Supervisor'},
        'operador': {'password': 'op2024', 'name': 'Operador'},
        'sines': {'password': 'sines123', 'name': 'Usuario SINES'}
    }
    
    # Sesiones activas (en memoria)
    active_sessions = {}
    failed_attempts = {}
    
    def end_headers(self):
        # Headers básicos de seguridad
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('X-Content-Type-Options', 'nosniff')
        
        # Cache control
        if self.path.endswith(('.js', '.css', '.json', '.pdf')):
            self.send_header('Cache-Control', 'public, max-age=3600')
        else:
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        
        super().end_headers()
    
    def do_OPTIONS(self):
        """Manejar preflight requests"""
        self.send_response(200)
        self.end_headers()
    
    def do_POST(self):
        """Manejar autenticación"""
        if self.path == '/api/login':
            self.handle_login()
        elif self.path == '/api/logout':
            self.handle_logout()
        elif self.path == '/api/validate_admin':
            self.handle_validate_admin()
        elif self.path == '/api/validate_session':
            self.handle_validate_session()
        else:
            self.send_error(404, "Endpoint no encontrado")
    
    def handle_login(self):
        """Procesar login"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
            else:
                data = {}
            
            username = data.get('username', '').strip().lower()
            password = data.get('password', '')
            
            # Verificar credenciales
            if username in self.USERS and self.USERS[username]['password'] == password:
                # Login exitoso
                session_id = hashlib.md5(f"{username}_{time.time()}".encode()).hexdigest()
                self.active_sessions[session_id] = {
                    'username': username,
                    'name': self.USERS[username]['name'],
                    'login_time': datetime.now(),
                    'last_activity': datetime.now()
                }
                
                # Limpiar intentos fallidos
                if username in self.failed_attempts:
                    del self.failed_attempts[username]
                
                # Establecer cookie Y enviar token
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.set_session_cookie(session_id)
                
                response_data = {
                    'success': True,
                    'message': 'Login exitoso',
                    'session_id': session_id,  # Para uso en JavaScript
                    'user': {
                        'username': username,
                        'name': self.USERS[username]['name']
                    }
                }
                
                response = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
                self.send_header('Content-Length', str(len(response)))
                self.end_headers()
                self.wfile.write(response)
                
                print(f"✅ Login exitoso: {username} ({self.USERS[username]['name']})")
                
            else:
                # Login fallido
                self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
                
                self.send_json_response({
                    'success': False,
                    'message': 'Credenciales incorrectas',
                    'attempts': self.failed_attempts[username]
                }, 401)
                
                print(f"❌ Login fallido: {username} (Intentos: {self.failed_attempts[username]})")
                
        except Exception as e:
            print(f"Error en login: {e}")
            self.send_json_response({
                'success': False,
                'message': 'Error interno del servidor'
            }, 500)
    
    def handle_logout(self):
        """Procesar logout"""
        try:
            # Intentar obtener sesión desde cookies o header
            session = self.validate_session_from_cookies()
            if not session:
                session = self.validate_session_from_header()
            
            if session:
                username = session['username']
                # Buscar y eliminar la sesión
                for session_id, sess_data in list(self.active_sessions.items()):
                    if sess_data['username'] == username:
                        del self.active_sessions[session_id]
                        break
                print(f"🚪 Logout: {username}")
            
            # Limpiar cookie y enviar respuesta
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.clear_session_cookie()
            
            response_data = {
                'success': True,
                'message': 'Logout exitoso'
            }
            
            response = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
            self.send_header('Content-Length', str(len(response)))
            self.end_headers()
            self.wfile.write(response)
            
        except Exception as e:
            print(f"Error en logout: {e}")
            self.send_json_response({
                'success': False,
                'message': 'Error en logout'
            }, 500)
    
    def handle_validate_admin(self):
        """Validar permisos de administrador"""
        try:
            # Intentar obtener sesión desde cookies o header
            session = self.validate_session_from_cookies()
            if not session:
                session = self.validate_session_from_header()
            
            if not session:
                self.send_json_response({
                    'success': False,
                    'message': 'Sesión inválida o expirada'
                }, 401)
                return
            
            username = session['username']
            
            # Verificar permisos de administrador
            if username in ['admin', 'supervisor']:
                self.send_json_response({
                    'success': True,
                    'user': {
                        'username': username,
                        'name': self.USERS[username]['name']
                    }
                })
                print(f"✅ Acceso autorizado al panel: {username} ({self.USERS[username]['name']})")
            else:
                self.send_json_response({
                    'success': False,
                    'message': 'Permisos insuficientes'
                }, 403)
                print(f"❌ Acceso denegado al panel: {username} (sin permisos de administrador)")
                
        except Exception as e:
            print(f"Error validando admin: {e}")
            self.send_json_response({
                'success': False,
                'message': 'Error interno'
            }, 500)

    def handle_validate_session(self):
        """Validar si hay una sesión activa"""
        try:
            # Intentar obtener sesión desde cookies o header
            session = self.validate_session_from_cookies()
            if not session:
                session = self.validate_session_from_header()
            
            if session:
                self.send_json_response({
                    'success': True,
                    'user': {
                        'username': session['username'],
                        'name': self.USERS[session['username']]['name']
                    }
                })
            else:
                self.send_json_response({
                    'success': False,
                    'message': 'No hay sesión activa'
                }, 401)
                
        except Exception as e:
            print(f"Error validando sesión: {e}")
            self.send_json_response({
                'success': False,
                'message': 'Error interno'
            }, 500)

    def send_json_response(self, data, status_code=200):
        """Enviar respuesta JSON"""
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)
    
    def validate_session_from_cookies(self):
        """Validar sesión desde cookies"""
        cookies = self.headers.get('Cookie', '')
        session_id = None
        
        # Extraer session_id de las cookies
        for cookie in cookies.split(';'):
            if 'sines_session=' in cookie:
                session_id = cookie.split('sines_session=')[1].strip()
                break
        
        if session_id and session_id in self.active_sessions:
            # Verificar timeout de sesión
            session = self.active_sessions[session_id]
            if datetime.now() - session['last_activity'] < timedelta(minutes=30):
                session['last_activity'] = datetime.now()
                return session
            else:
                # Sesión expirada
                del self.active_sessions[session_id]
        
        return None

    def validate_session_from_header(self):
        """Validar sesión desde Authorization header"""
        auth_header = self.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        session_id = auth_header[7:]
        if session_id and session_id in self.active_sessions:
            # Verificar timeout de sesión
            session = self.active_sessions[session_id]
            if datetime.now() - session['last_activity'] < timedelta(minutes=30):
                session['last_activity'] = datetime.now()
                return session
            else:
                # Sesión expirada
                del self.active_sessions[session_id]
        
        return None

    def set_session_cookie(self, session_id):
        """Establecer cookie de sesión"""
        self.send_header('Set-Cookie', f'sines_session={session_id}; Path=/; SameSite=Lax')

    def clear_session_cookie(self):
        """Limpiar cookie de sesión"""
        self.send_header('Set-Cookie', 'sines_session=; Path=/; SameSite=Lax; Expires=Thu, 01 Jan 1970 00:00:00 GMT')

    def do_GET(self):
        """Manejar GET requests con seguridad mejorada"""
        
        # Rutas completamente públicas
        public_files = [
            '/index_secure_simple.html',
            '/index_secure_hybrid.html',
            '/favicon.ico'
        ]
        
        # Archivos estáticos básicos
        static_files = ['.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico']
        
        # Permitir solo archivos públicos básicos
        if any(self.path == path for path in public_files) or \
           any(self.path.endswith(ext) for ext in static_files):
            super().do_GET()
            return
        
        # API de estado público
        if self.path == '/api/status':
            self.send_json_response({
                'status': 'running',
                'timestamp': datetime.now().isoformat(),
                'server': 'SINES Secure Server',
                'active_sessions': len(self.active_sessions)
            })
            return
        
        # TODAS las demás rutas requieren autenticación
        session = self.validate_session_from_cookies()
        if not session:
            session = self.validate_session_from_header()
        
        if not session:
            # No hay sesión válida - redirigir al login
            self.send_response(302)
            self.send_header('Location', '/index_secure_hybrid.html?error=session_required')
            self.end_headers()
            return
        
        # Rutas que requieren permisos de administrador
        admin_paths = ['/config_panel.html']
        
        if any(self.path.startswith(path) for path in admin_paths):
            if session['username'] not in ['admin', 'supervisor']:
                # Sin permisos de administrador
                self.send_response(403)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(f"""
                <!DOCTYPE html>
                <html>
                <head><title>Acceso Denegado</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1>🚫 Acceso Denegado</h1>
                    <p>No tiene permisos para acceder a esta página.</p>
                    <p>Solo administradores y supervisores pueden acceder al panel de configuración.</p>
                    <p>Usuario actual: {session['name']}</p>
                    <button onclick="window.close()">Cerrar</button>
                    <button onclick="window.location.href='/index_secure_hybrid.html'">Volver al Dashboard</button>
                </body>
                </html>
                """.encode('utf-8'))
                return
        
        # Usuario autenticado y con permisos - permitir acceso
        super().do_GET()

def start_secure_server():
    PORT = 8003  # Puerto diferente para evitar conflictos
    
    try:
        with socketserver.TCPServer(("", PORT), HybridSecureHandler) as httpd:
            print("🔒 SERVIDOR SEGURO HÍBRIDO SINES")
            print("=" * 50)
            print(f"🌐 URL: http://localhost:{PORT}")
            print(f"🔐 Página de acceso: http://localhost:{PORT}/index_secure_hybrid.html")
            print(f"📂 Directorio: {os.getcwd()}")
            print("\n🔑 CREDENCIALES:")
            print("┌─────────────┬──────────────┬───────────────┐")
            print("│ Usuario     │ Contraseña   │ Nombre        │")
            print("├─────────────┼──────────────┼───────────────┤")
            print("│ admin       │ sines2024    │ Administrador │")
            print("│ supervisor  │ super2024    │ Supervisor    │")
            print("│ operador    │ op2024       │ Operador      │")
            print("│ sines       │ sines123     │ Usuario SINES │")
            print("└─────────────┴──────────────┴───────────────┘")
            print("\n🛡️ CARACTERÍSTICAS:")
            print("• Autenticación dual (cookies + tokens)")
            print("• Compatible con ventanas múltiples")
            print("• Sesiones con timeout (30 min)")
            print("• Control de acceso por roles")
            print("\n🚀 Abriendo navegador...")
            
            # Abrir navegador
            def open_browser():
                time.sleep(2)
                webbrowser.open(f'http://localhost:{PORT}/index_secure_hybrid.html')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.start()
            
            print("\n⚠️  Para detener: Presiona Ctrl+C")
            print("=" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Puerto {PORT} ocupado. Cierra otros servidores.")
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_secure_server() 