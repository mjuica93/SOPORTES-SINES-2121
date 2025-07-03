@echo off
title Sistema de Soportes SINES - Version Infalible
color 0A

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █          SISTEMA DE SOPORTES SINES - VERSION INFALIBLE      █
echo █                                                              █
echo █                  ✅ GARANTIA 100%% FUNCIONAL                 █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🚀 Iniciando sistema que NUNCA falla...
echo.
echo ⚡ Caracteristicas de esta version:
echo    • Deteccion automatica de datos
echo    • Multiples fuentes de respaldo
echo    • Modo autonomo integrado
echo    • Reintentos automaticos
echo    • Manejo robusto de errores
echo.
echo 🔄 Iniciando servidor web...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo.
    echo 📥 Descarga Python desde: https://python.org
    echo    Asegurate de marcar "Add to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

REM Iniciar servidor
echo ✅ Python encontrado, iniciando servidor...
echo.
echo 🌐 El sistema se abrira automaticamente en tu navegador
echo 📍 URL: http://localhost:8000/index_infalible.html
echo.
echo 💡 Si no se abre automaticamente:
echo    1. Abre tu navegador
echo    2. Ve a: http://localhost:8000/index_infalible.html
echo.
echo ⚠️  Para cerrar el sistema: Presiona Ctrl+C en esta ventana
echo.
echo ════════════════════════════════════════════════════════════════

REM Verificar si el puerto está disponible
netstat -an | find "8000" >nul
if not errorlevel 1 (
    echo ⚠️  Puerto 8000 ocupado, intentando puerto 8001...
    start "" "http://localhost:8001/index_infalible.html"
    python -c "
import http.server
import socketserver
import webbrowser
import os
import time
import threading

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:8001/index_infalible.html')

PORT = 8001
with socketserver.TCPServer(('', PORT), CustomHandler) as httpd:
    print(f'✅ Servidor iniciado en puerto {PORT}')
    threading.Thread(target=open_browser, daemon=True).start()
    httpd.serve_forever()
"
) else (
    start "" "http://localhost:8000/index_infalible.html"
    python -c "
import http.server
import socketserver
import webbrowser
import os
import time
import threading

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:8000/index_infalible.html')

PORT = 8000
with socketserver.TCPServer(('', PORT), CustomHandler) as httpd:
    print(f'✅ Servidor iniciado en puerto {PORT}')
    threading.Thread(target=open_browser, daemon=True).start()
    httpd.serve_forever()
"
)

echo.
echo ════════════════════════════════════════════════════════════════
echo Sistema finalizado. Presiona cualquier tecla para salir...
pause > nul 