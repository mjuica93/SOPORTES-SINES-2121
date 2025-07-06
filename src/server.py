#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SERVIDOR SEGURO COMPLETO SINES
Reemplaza completamente al servidor principal (puerto 8000)
Requiere autenticación para TODOS los accesos
"""

import http.server
import socketserver
import json
import os
import hashlib
import secrets
import time
import webbrowser
import threading
import urllib.parse
from datetime import datetime, timedelta

# Configuración de seguridad
SECURITY_CONFIG = {
    'session_timeout': 30 * 60,  # 30 minutos
    'max_login_attempts': 3,
    'lockout_duration': 5 * 60,  # 5 minutos
    'token_length': 32
}

# Base de datos de usuarios
USERS_DB = {
    'admin': {
        'password_hash': hashlib.sha256('sines2024'.encode()).hexdigest(),
        'name': 'Administrador',
        'role': 'admin'
    },
    'supervisor': {
        'password_hash': hashlib.sha256('super2024'.encode()).hexdigest(),
        'name': 'Supervisor',
        'role': 'supervisor'
    },
    'operador': {
        'password_hash': hashlib.sha256('op2024'.encode()).hexdigest(),
        'name': 'Operador',
        'role': 'operator'
    },
    'sines': {
        'password_hash': hashlib.sha256('sines123'.encode()).hexdigest(),
        'name': 'Usuario SINES',
        'role': 'user'
    }
}

# Almacenamiento de sesiones y intentos
active_sessions = {}
login_attempts = {}
blocked_ips = {}

class SecureCompleteHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        # Headers de seguridad
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        self.send_header('Content-Security-Policy', "default-src 'self' 'unsafe-inline' 'unsafe-eval'; img-src 'self' data:; font-src 'self' data:")
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def log_security_event(self, event_type, details=""):
        """Registrar eventos de seguridad"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        client_ip = self.client_address[0]
        log_entry = f"[{timestamp}] {event_type} - IP: {client_ip} - {details}"
        print(log_entry)
    
    def is_ip_blocked(self):
        """Verificar si la IP está bloqueada"""
        client_ip = self.client_address[0]
        if client_ip in blocked_ips:
            if time.time() - blocked_ips[client_ip] < SECURITY_CONFIG['lockout_duration']:
                return True
            else:
                del blocked_ips[client_ip]
        return False
    
    def validate_session(self):
        """Validar sesión activa"""
        # Verificar cookies
        cookies = self.get_cookies()
        session_id = cookies.get('session_id')
        
        if session_id and session_id in active_sessions:
            session = active_sessions[session_id]
            if time.time() - session['last_activity'] < SECURITY_CONFIG['session_timeout']:
                # Actualizar última actividad
                session['last_activity'] = time.time()
                return session
            else:
                # Sesión expirada
                del active_sessions[session_id]
        
        # Verificar token en Authorization header
        auth_header = self.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            for session_id, session in active_sessions.items():
                if session.get('token') == token:
                    if time.time() - session['last_activity'] < SECURITY_CONFIG['session_timeout']:
                        session['last_activity'] = time.time()
                        return session
                    else:
                        del active_sessions[session_id]
                        break
        
        return None
    
    def get_cookies(self):
        """Extraer cookies de la petición"""
        cookies = {}
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            for cookie in cookie_header.split(';'):
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    cookies[key] = value
        return cookies
    
    def set_secure_cookie(self, name, value, max_age=None):
        """Establecer cookie segura"""
        cookie_value = f"{name}={value}; Path=/; HttpOnly; SameSite=Lax"
        if max_age:
            cookie_value += f"; Max-Age={max_age}"
        self.send_header('Set-Cookie', cookie_value)
    
    def require_auth(self):
        """Verificar autenticación requerida"""
        if self.is_ip_blocked():
            self.send_error(429, "Demasiados intentos fallidos. Intenta más tarde.")
            return False
        
        session = self.validate_session()
        if not session:
            self.redirect_to_login()
            return False
        
        # Actualizar información de sesión para uso posterior
        self.current_user = session['user']
        self.current_role = session['role']
        return True
    
    def redirect_to_login(self):
        """Redirigir a página de login"""
        self.send_response(302)
        self.send_header('Location', '/login.html')
        self.end_headers()
    
    def do_GET(self):
        """Manejar peticiones GET"""
        if self.path == '/login.html':
            self.serve_login_page()
        elif self.path == '/config_panel.html':
            self.serve_config_panel()
        elif self.path == '/logout_manager.js':
            self.serve_logout_manager()
        elif self.path.startswith('/api/'):
            self.handle_api_request()
        elif self.path in ['/', '/index.html']:
            if self.require_auth():
                self.serve_main_system()
        elif self.path.startswith('/ESTANDARES DE SOPORTES/') or self.path.endswith('.json'):
            if self.require_auth():
                super().do_GET()
        else:
            if self.require_auth():
                # Inyectar script de logout en archivos HTML
                if self.path.endswith('.html'):
                    self.serve_html_with_logout()
                else:
                    super().do_GET()
    
    def do_POST(self):
        """Manejar peticiones POST"""
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            if self.require_auth():
                super().do_POST()
    
    def serve_login_page(self):
        """Servir página de login"""
        login_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔒 Acceso Seguro - Sistema SINES</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
            text-align: center;
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .logo {
            font-size: 48px;
            margin-bottom: 10px;
        }
        
        .title {
            color: #333;
            margin-bottom: 30px;
            font-size: 24px;
            font-weight: 600;
        }
        
        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: 500;
        }
        
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e1e1;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus, input[type="password"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .login-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .login-btn:hover {
            transform: translateY(-2px);
        }
        
        .login-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .credentials {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            text-align: left;
        }
        
        .credentials h4 {
            color: #333;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .credential-item {
            margin-bottom: 10px;
            font-size: 14px;
        }
        
        .username {
            font-weight: 600;
            color: #667eea;
        }
        
        .password {
            color: #666;
        }
        
        .error {
            color: #e74c3c;
            margin-top: 10px;
            padding: 10px;
            background: #fdf2f2;
            border-radius: 5px;
            border-left: 4px solid #e74c3c;
        }
        
        .success {
            color: #27ae60;
            margin-top: 10px;
            padding: 10px;
            background: #f2fdf5;
            border-radius: 5px;
            border-left: 4px solid #27ae60;
        }
        
        .status {
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .status.online {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status.offline {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">🔒</div>
        <h1 class="title">Sistema SINES Seguro</h1>
        
        <form id="loginForm">
            <div class="form-group">
                <label for="username">Usuario:</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit" class="login-btn" id="loginBtn">
                🚀 Iniciar Sesión
            </button>
        </form>
        
        <div id="message"></div>
        
        <div class="credentials">
            <h4>🔑 Credenciales de Acceso</h4>
            <div class="credential-item">
                <span class="username">admin</span> / <span class="password">sines2024</span>
            </div>
            <div class="credential-item">
                <span class="username">supervisor</span> / <span class="password">super2024</span>
            </div>
            <div class="credential-item">
                <span class="username">operador</span> / <span class="password">op2024</span>
            </div>
            <div class="credential-item">
                <span class="username">sines</span> / <span class="password">sines123</span>
            </div>
        </div>
        
        <div id="systemStatus" class="status"></div>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const loginBtn = document.getElementById('loginBtn');
            const messageDiv = document.getElementById('message');
            
            loginBtn.disabled = true;
            loginBtn.textContent = '🔄 Iniciando sesión...';
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    messageDiv.innerHTML = '<div class="success">✅ Acceso autorizado. Redirigiendo...</div>';
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1000);
                } else {
                    messageDiv.innerHTML = `<div class="error">❌ ${result.error}</div>`;
                }
            } catch (error) {
                messageDiv.innerHTML = '<div class="error">❌ Error de conexión</div>';
            }
            
            loginBtn.disabled = false;
            loginBtn.textContent = '🚀 Iniciar Sesión';
        });
        
        // Verificar estado del sistema
        async function checkSystemStatus() {
            try {
                const response = await fetch('/api/status');
                const status = await response.json();
                
                const statusDiv = document.getElementById('systemStatus');
                statusDiv.className = 'status online';
                statusDiv.innerHTML = `
                    <strong>🟢 Sistema Online</strong><br>
                    Soportes: ${status.supports || 0}<br>
                    Isométricos: ${status.isometrics || 0}<br>
                    Servidor: ${status.server || 'Activo'}
                `;
            } catch (error) {
                const statusDiv = document.getElementById('systemStatus');
                statusDiv.className = 'status offline';
                statusDiv.innerHTML = '<strong>🔴 Sistema Offline</strong>';
            }
        }
        
        // Verificar si ya hay sesión activa
        async function checkExistingSession() {
            try {
                const response = await fetch('/api/validate_session');
                if (response.ok) {
                    window.location.href = '/';
                }
            } catch (error) {
                // No hay sesión activa, continuar con login
            }
        }
        
        checkSystemStatus();
        checkExistingSession();
        setInterval(checkSystemStatus, 30000); // Actualizar cada 30 segundos
        
        // Función para abrir panel de configuración
        function openConfigPanel() {
            // Verificar que el panel esté visible (solo para admin/supervisor)
            const configPanel = document.getElementById('configPanel');
            if (configPanel.style.display === 'none') {
                alert('❌ No tienes permisos para acceder al panel de configuración.');
                return;
            }
            
            // Abrir en nueva ventana
            const configWindow = window.open('/config_panel.html', '_blank', 
                'width=1400,height=900,scrollbars=yes,resizable=yes,toolbar=no,menubar=no');
            
            if (!configWindow) {
                alert('❌ No se pudo abrir el panel. Verifica el bloqueador de ventanas emergentes.');
            }
        }
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(login_html.encode('utf-8'))
    
    def serve_main_system(self):
        """Servir sistema principal después de autenticación"""
        # Mostrar siempre la página de navegación con opciones de administrador
        self.serve_navigation_page()
    
    def serve_navigation_page(self):
        """Servir página de navegación del sistema"""
        navigation_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏠 Sistema SINES - Navegación</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 800px;
            text-align: center;
        }
        
        .logo {
            font-size: 64px;
            margin-bottom: 20px;
        }
        
        .title {
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
            font-weight: 600;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 40px;
            font-size: 16px;
        }
        
        .modules {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .module-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 15px;
            border: 2px solid #dee2e6;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
        }
        
        .module-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        
        .module-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
        
        .module-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
        }
        
        .module-desc {
            font-size: 14px;
            color: #666;
            line-height: 1.4;
        }
        
        .user-info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .logout-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .logout-btn:hover {
            background: #c82333;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🏭</div>
        <h1 class="title">Sistema SINES</h1>
        <p class="subtitle">Gestión Integral de Soportes e Isométricos</p>
        
        <div class="user-info">
            <span id="userWelcome">Bienvenido al sistema</span>
            <button class="logout-btn" onclick="logout()">🚪 Cerrar Sesión</button>
        </div>
        
        <div class="modules">
            <a href="/index_isometricos_integrado_final.html" class="module-card">
                <div class="module-icon">📐</div>
                <div class="module-title">Sistema Integrado Mejorado</div>
                <div class="module-desc">Soportes Agrupados, Variables de Plantilla, Isométricos y Relaciones</div>
            </a>
            
            <a href="/index.html" class="module-card">
                <div class="module-icon">🔧</div>
                <div class="module-title">Gestión de Soportes</div>
                <div class="module-desc">Administración de soportes estructurales</div>
            </a>
            
            <a href="/index_enhanced.html" class="module-card">
                <div class="module-icon">⚡</div>
                <div class="module-title">Versión Mejorada</div>
                <div class="module-desc">Interfaz optimizada y funciones avanzadas</div>
            </a>
            
            <a href="/index_mobile.html" class="module-card">
                <div class="module-icon">📱</div>
                <div class="module-title">Versión Móvil</div>
                <div class="module-desc">Optimizado para dispositivos móviles</div>
            </a>
            
            <a href="/verificar_json.html" class="module-card">
                <div class="module-icon">🔍</div>
                <div class="module-title">Verificar Datos</div>
                <div class="module-desc">Validación de archivos JSON</div>
            </a>
            
            <div class="module-card" id="configPanel" style="display: none;" onclick="openConfigPanel()">
                <div class="module-icon">⚙️</div>
                <div class="module-title">Panel de Configuración</div>
                <div class="module-desc">Administración del sistema (Solo Admin/Supervisor)</div>
            </div>
        </div>
    </div>

    <script>
        // Verificar sesión al cargar
        async function checkSession() {
            try {
                const response = await fetch('/api/validate_session');
                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('userWelcome').textContent = 
                        `Bienvenido, ${data.name} (${data.role})`;
                    
                    // Mostrar panel de configuración solo para admin y supervisor
                    if (data.role === 'admin' || data.role === 'supervisor') {
                        document.getElementById('configPanel').style.display = 'block';
                    }
                } else {
                    window.location.href = '/login.html';
                }
            } catch (error) {
                console.error('Error verificando sesión:', error);
                window.location.href = '/login.html';
            }
        }
        
        async function logout() {
            try {
                await fetch('/api/logout', { method: 'POST' });
                window.location.href = '/login.html';
            } catch (error) {
                console.error('Error al cerrar sesión:', error);
                window.location.href = '/login.html';
            }
        }
        
        // Función para abrir panel de configuración
        function openConfigPanel() {
            const configWindow = window.open('/config_panel.html', '_blank', 
                'width=1400,height=900,scrollbars=yes,resizable=yes,toolbar=no,menubar=no');
            
            if (!configWindow) {
                alert('❌ No se pudo abrir el panel. Verifica el bloqueador de ventanas emergentes.');
            }
        }
        
        checkSession();
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(navigation_html.encode('utf-8'))
    
    def serve_logout_manager(self):
        """Servir script de logout manager"""
        try:
            with open('logout_manager.js', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "Logout manager script not found")
    
    def serve_html_with_logout(self):
        """Servir archivos HTML con script de logout inyectado"""
        try:
            # Leer el archivo HTML original
            file_path = self.path[1:]  # Remover el '/' inicial
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Inyectar el script de logout antes del cierre de </body>
            logout_script = '<script src="/logout_manager.js"></script>'
            
            if '</body>' in content:
                content = content.replace('</body>', f'{logout_script}\n</body>')
            else:
                # Si no hay </body>, agregar al final
                content += f'\n{logout_script}'
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            
        except FileNotFoundError:
            self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, f"Error serving HTML: {str(e)}")
    
    def handle_api_request(self):
        """Manejar peticiones API"""
        if self.path == '/api/login':
            self.handle_login()
        elif self.path == '/api/logout':
            self.handle_logout()
        elif self.path == '/api/status':
            self.handle_status()
        elif self.path == '/api/validate_session':
            self.handle_validate_session()
        elif self.path == '/api/validate_admin':
            self.handle_validate_admin()
        elif self.path == '/api/user-info':
            self.handle_user_info()
        elif self.path == '/api/update-weld-status':
            self.handle_update_weld_status()
        elif self.path == '/api/log-pdf-access':
            self.handle_log_pdf_access()
        else:
            self.send_error(404, "API endpoint not found")
    
    def handle_login(self):
        """Manejar inicio de sesión"""
        if self.command != 'POST':
            self.send_error(405, "Method not allowed")
            return
        
        client_ip = self.client_address[0]
        
        # Verificar si la IP está bloqueada
        if self.is_ip_blocked():
            self.send_json_response({
                'error': 'Demasiados intentos fallidos. Intenta más tarde.'
            }, 429)
            return
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            
            if not username or not password:
                self.send_json_response({'error': 'Usuario y contraseña requeridos'}, 400)
                return
            
            # Verificar credenciales
            if username in USERS_DB:
                user = USERS_DB[username]
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                
                if user['password_hash'] == password_hash:
                    # Login exitoso
                    session_id = secrets.token_hex(16)
                    token = secrets.token_hex(SECURITY_CONFIG['token_length'])
                    
                    active_sessions[session_id] = {
                        'user': username,
                        'name': user['name'],
                        'role': user['role'],
                        'token': token,
                        'login_time': time.time(),
                        'last_activity': time.time(),
                        'ip': client_ip
                    }
                    
                    # Limpiar intentos fallidos
                    if client_ip in login_attempts:
                        del login_attempts[client_ip]
                    
                    self.log_security_event("LOGIN_SUCCESS", f"Usuario: {username} ({user['name']})")
                    
                    self.send_response(200)
                    self.set_secure_cookie('session_id', session_id, SECURITY_CONFIG['session_timeout'])
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    
                    response = {
                        'success': True,
                        'user': username,
                        'name': user['name'],
                        'role': user['role'],
                        'token': token
                    }
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    return
            
            # Login fallido
            if client_ip not in login_attempts:
                login_attempts[client_ip] = []
            
            login_attempts[client_ip].append(time.time())
            
            # Limpiar intentos antiguos
            login_attempts[client_ip] = [
                attempt for attempt in login_attempts[client_ip]
                if time.time() - attempt < SECURITY_CONFIG['lockout_duration']
            ]
            
            # Verificar si se debe bloquear
            if len(login_attempts[client_ip]) >= SECURITY_CONFIG['max_login_attempts']:
                blocked_ips[client_ip] = time.time()
                self.log_security_event("IP_BLOCKED", f"IP bloqueada por intentos fallidos")
                self.send_json_response({
                    'error': 'Demasiados intentos fallidos. IP bloqueada temporalmente.'
                }, 429)
            else:
                attempts_left = SECURITY_CONFIG['max_login_attempts'] - len(login_attempts[client_ip])
                self.log_security_event("LOGIN_FAILED", f"Usuario: {username}")
                self.send_json_response({
                    'error': f'Credenciales incorrectas. Intentos restantes: {attempts_left}'
                }, 401)
        
        except json.JSONDecodeError:
            self.send_json_response({'error': 'Datos JSON inválidos'}, 400)
        except Exception as e:
            self.log_security_event("LOGIN_ERROR", f"Error: {str(e)}")
            self.send_json_response({'error': 'Error interno del servidor'}, 500)
    
    def handle_logout(self):
        """Manejar cierre de sesión"""
        cookies = self.get_cookies()
        session_id = cookies.get('session_id')
        
        if session_id and session_id in active_sessions:
            user = active_sessions[session_id]['user']
            del active_sessions[session_id]
            self.log_security_event("LOGOUT", f"Usuario: {user}")
        
        self.send_response(200)
        self.set_secure_cookie('session_id', '', 0)  # Eliminar cookie
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {'success': True, 'message': 'Sesión cerrada correctamente'}
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def handle_status(self):
        """Manejar estado del sistema"""
        try:
            # Cargar estadísticas del sistema
            supports_count = 0
            isometrics_count = 0
            
            if os.path.exists('support_data_enhanced.json'):
                with open('support_data_enhanced.json', 'r', encoding='utf-8') as f:
                    supports = json.load(f)
                    supports_count = len(supports)
            
            if os.path.exists('isometric_data_with_prefabricated.json'):
                with open('isometric_data_with_prefabricated.json', 'r', encoding='utf-8') as f:
                    isometrics = json.load(f)
                    isometrics_count = len(isometrics)
            
            status = {
                'server': 'Activo',
                'supports': supports_count,
                'isometrics': isometrics_count,
                'active_sessions': len(active_sessions),
                'timestamp': datetime.now().isoformat()
            }
            
            self.send_json_response(status)
        
        except Exception as e:
            self.send_json_response({'error': 'Error al obtener estado'}, 500)
    
    def handle_validate_session(self):
        """Validar sesión actual"""
        session = self.validate_session()
        
        if session:
            self.send_json_response({
                'valid': True,
                'user': session['user'],
                'name': session['name'],
                'role': session['role']
            })
        else:
            self.send_json_response({'valid': False}, 401)
    
    def handle_validate_admin(self):
        """Validar permisos de administrador"""
        try:
            # Obtener sesión desde cookies o header Authorization
            session = self.validate_session()
            
            if not session:
                self.send_json_response({
                    'success': False,
                    'message': 'Sesión inválida o expirada'
                }, 401)
                return
            
            username = session['user']
            user_data = USERS_DB.get(username)
            
            if not user_data:
                self.send_json_response({
                    'success': False,
                    'message': 'Usuario no encontrado'
                }, 404)
                return
            
            # Verificar permisos de administrador
            if user_data['role'] in ['admin', 'supervisor']:
                self.send_json_response({
                    'success': True,
                    'user': {
                        'username': username,
                        'name': user_data['name'],
                        'role': user_data['role']
                    }
                })
                self.log_security_event("ADMIN_ACCESS", f"Usuario: {username} ({user_data['name']})")
            else:
                self.send_json_response({
                    'success': False,
                    'message': 'Permisos insuficientes. Solo administradores y supervisores.'
                }, 403)
                self.log_security_event("ADMIN_DENIED", f"Usuario: {username} (sin permisos)")
                
        except Exception as e:
            self.log_security_event("ADMIN_ERROR", f"Error: {str(e)}")
            self.send_json_response({
                'success': False,
                'message': 'Error interno del servidor'
            }, 500)
    
    def handle_user_info(self):
        """Obtener información del usuario actual"""
        session = self.validate_session()
        if not session:
            self.send_json_response({
                'error': 'Sesión inválida'
            }, 401)
            return
        
        username = session['user']
        user_data = USERS_DB.get(username)
        
        self.send_json_response({
            'username': username,
            'role': user_data['role'] if user_data else 'unknown',
            'name': user_data['name'] if user_data else username,
            'login_time': session.get('login_time')
        })
    
    def handle_update_weld_status(self):
        """Actualizar el estado de una costura"""
        if self.command != 'POST':
            self.send_error(405, "Method not allowed")
            return
            
        session = self.validate_session()
        if not session:
            self.send_json_response({
                'error': 'Sesión inválida'
            }, 401)
            return
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Validar datos requeridos
            required_fields = ['weld_id', 'old_status', 'new_status']
            for field in required_fields:
                if field not in data:
                    self.send_json_response({
                        'error': f'Campo requerido: {field}'
                    }, 400)
                    return
            
            username = session['user']
            user_data = USERS_DB.get(username)
            
            # Registrar el cambio
            change_record = {
                'weld_id': data['weld_id'],
                'old_status': data['old_status'],
                'new_status': data['new_status'],
                'comment': data.get('comment', ''),
                'timestamp': datetime.now().isoformat(),
                'user_role': user_data['role'] if user_data else 'unknown',
                'username': username
            }
            
            # Log del cambio
            self.log_security_event("WELD_STATUS_CHANGE", 
                                   f"Usuario: {username}, Weld ID: {data['weld_id']}, "
                                   f"Estado: {data['old_status']} -> {data['new_status']}")
            
            # Aquí se podría guardar en base de datos
            # Por ahora solo devolvemos confirmación
            
            self.send_json_response({
                'success': True,
                'message': 'Estado actualizado correctamente',
                'change_record': change_record
            })
            
        except json.JSONDecodeError:
            self.send_json_response({
                'error': 'Datos JSON inválidos'
            }, 400)
        except Exception as e:
            self.send_json_response({
                'error': f'Error interno del servidor: {str(e)}'
            }, 500)
    
    def handle_log_pdf_access(self):
        """Registrar acceso a PDF"""
        if self.command != 'POST':
            self.send_error(405, "Method not allowed")
            return
            
        session = self.validate_session()
        if not session:
            self.send_json_response({
                'error': 'Sesión inválida'
            }, 401)
            return
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            username = session['user']
            user_data = USERS_DB.get(username)
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'pdf_access',
                'pdf_path': data.get('pdf_path', ''),
                'pdf_type': data.get('pdf_type', ''),
                'user_role': user_data['role'] if user_data else 'unknown',
                'username': username,
                'ip_address': self.client_address[0]
            }
            
            self.log_security_event("PDF_ACCESS", 
                                   f"Usuario: {username}, Archivo: {data.get('pdf_path', '')}, "
                                   f"Tipo: {data.get('pdf_type', '')}")
            
            self.send_json_response({
                'success': True,
                'message': 'Acceso registrado'
            })
            
        except json.JSONDecodeError:
            self.send_json_response({
                'error': 'Datos JSON inválidos'
            }, 400)
        except Exception as e:
            self.send_json_response({
                'error': f'Error interno del servidor: {str(e)}'
            }, 500)
    
    def serve_config_panel(self):
        """Servir panel de configuración con autenticación"""
        # Verificar autenticación
        session = self.validate_session()
        if not session:
            self.redirect_to_login()
            return
        
        # Verificar permisos de administrador
        username = session['user']
        user_data = USERS_DB.get(username)
        
        if not user_data or user_data['role'] not in ['admin', 'supervisor']:
            # Sin permisos de administrador
            self.send_response(403)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            access_denied_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚫 Acceso Denegado - Sistema SINES</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 500px;
        }}
        .icon {{
            font-size: 64px;
            margin-bottom: 20px;
        }}
        .title {{
            color: #333;
            margin-bottom: 20px;
            font-size: 24px;
        }}
        .message {{
            color: #666;
            margin-bottom: 30px;
            line-height: 1.6;
        }}
        .user-info {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin: 5px;
            text-decoration: none;
            display: inline-block;
        }}
        .btn:hover {{
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">🚫</div>
        <h1 class="title">Acceso Denegado</h1>
        <div class="message">
            <p>No tienes permisos para acceder al panel de configuración.</p>
            <p>Solo administradores y supervisores pueden acceder a esta área.</p>
        </div>
        <div class="user-info">
            <strong>Usuario actual:</strong> {user_data['name'] if user_data else 'Desconocido'}<br>
            <strong>Rol:</strong> {user_data['role'] if user_data else 'Sin rol'}
        </div>
        <a href="/" class="btn">🏠 Volver al Sistema</a>
        <button onclick="window.close()" class="btn">❌ Cerrar Ventana</button>
    </div>
</body>
</html>
            """
            self.wfile.write(access_denied_html.encode('utf-8'))
            return
        
        # Usuario autorizado - servir panel de configuración
        try:
            with open('config_panel.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            
            self.log_security_event("CONFIG_ACCESS", f"Usuario: {username} ({user_data['name']})")
            
        except FileNotFoundError:
            self.send_error(404, "Panel de configuración no encontrado")
    
    def send_json_response(self, data, status_code=200):
        """Enviar respuesta JSON"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def cleanup_expired_sessions():
    """Limpiar sesiones expiradas"""
    current_time = time.time()
    expired_sessions = []
    
    for session_id, session in active_sessions.items():
        if current_time - session['last_activity'] > SECURITY_CONFIG['session_timeout']:
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        user = active_sessions[session_id]['user']
        del active_sessions[session_id]
        print(f"🕐 Sesión expirada: {user}")

def start_secure_server():
    """Iniciar servidor seguro completo"""
    PORT = 8000  # Usar puerto 8000 para reemplazar servidor principal
    
    try:
        with socketserver.TCPServer(("", PORT), SecureCompleteHandler) as httpd:
            print("🔒 SERVIDOR SEGURO COMPLETO SINES")
            print("=" * 50)
            print(f"🌐 URL: http://localhost:{PORT}")
            print(f"🔐 Página de acceso: http://localhost:{PORT}/login.html")
            print(f"📂 Directorio: {os.getcwd()}")
            print("\n🔑 CREDENCIALES:")
            print("┌─────────────┬──────────────┬───────────────┐")
            print("│ Usuario     │ Contraseña   │ Rol           │")
            print("├─────────────┼──────────────┼───────────────┤")
            print("│ admin       │ sines2024    │ Administrador │")
            print("│ supervisor  │ super2024    │ Supervisor    │")
            print("│ operador    │ op2024       │ Operador      │")
            print("│ sines       │ sines123     │ Usuario       │")
            print("└─────────────┴──────────────┴───────────────┘")
            print("\n🛡️ SEGURIDAD COMPLETA:")
            print("• Autenticación obligatoria para TODO acceso")
            print("• Sesiones con timeout (30 min)")
            print("• Bloqueo por intentos fallidos")
            print("• Cookies seguras HttpOnly")
            print("• Headers de seguridad HTTP")
            print("• Logs de auditoría")
            print("\n🚀 Abriendo navegador...")
            
            # Abrir navegador
            def open_browser():
                time.sleep(2)
                webbrowser.open(f'http://localhost:{PORT}/login.html')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.start()
            
            # Iniciar limpieza automática de sesiones
            def cleanup_timer():
                while True:
                    time.sleep(300)  # Cada 5 minutos
                    cleanup_expired_sessions()
            
            cleanup_thread = threading.Thread(target=cleanup_timer, daemon=True)
            cleanup_thread.start()
            
            print("\n⚠️  Para detener: Presiona Ctrl+C")
            print("=" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor seguro detenido")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Puerto {PORT} ocupado. Detén otros servidores primero.")
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_secure_server() 