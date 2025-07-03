@echo off
title SINES Soportes - Version Movil
color 0B

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █              SINES SOPORTES - VERSION MOVIL                 █
echo █                                                              █
echo █                  📱 OPTIMIZADO PARA MOVILES                  █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 📱 Iniciando version optimizada para moviles...
echo.
echo ⚡ Caracteristicas de esta version:
echo    • Interfaz tactil optimizada
echo    • Carga rapida en moviles
echo    • Busqueda instantanea
echo    • Visualizacion compacta
echo    • Compatible con todos los dispositivos
echo.
echo 🔄 Iniciando servidor web...
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo.
    echo 📥 Descarga Python desde: https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado, iniciando servidor...
echo.
echo 🌐 URLs disponibles:
echo    📱 Movil: http://localhost:8000/index_mobile.html
echo    💻 Completa: http://localhost:8000/index_enhanced_with_templates.html
echo.
echo 💡 Para acceso mundial:
echo    1. Ejecuta ACCESO_MUNDIAL.bat
echo    2. Copia la URL publica que aparece
echo    3. Abre esa URL en tu movil
echo.
echo ⚠️  Para cerrar: Presiona Ctrl+C
echo.
echo ════════════════════════════════════════════════════════════════

start "" "http://localhost:8000/index_mobile.html"

python -c "
import http.server
import socketserver
import webbrowser
import time
import threading

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

PORT = 8000
with socketserver.TCPServer(('', PORT), CustomHandler) as httpd:
    print(f'✅ Servidor movil iniciado en puerto {PORT}')
    httpd.serve_forever()
"

echo.
echo ════════════════════════════════════════════════════════════════
echo Sistema finalizado. Presiona cualquier tecla para salir...
pause > nul
