@echo off
title SINES Soportes - Acceso Mundial
color 0A

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █              SINES SOPORTES - ACCESO MUNDIAL                █
echo █                                                              █
echo █                  🌐 DISPONIBLE EN TODO EL MUNDO              █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🚀 Configurando acceso mundial con Ngrok...
echo.

REM Verificar si Ngrok está instalado
ngrok version >nul 2>&1
if errorlevel 1 (
    echo ❌ Ngrok no encontrado
    echo.
    echo 📥 Para instalar Ngrok:
    echo    1. Ve a: https://ngrok.com/download
    echo    2. Descarga ngrok.exe
    echo    3. Coloca ngrok.exe en esta carpeta
    echo    4. Ejecuta este script nuevamente
    echo.
    echo 💡 Alternativamente, usa: winget install ngrok
    echo.
    pause
    exit /b 1
)

echo ✅ Ngrok encontrado
echo.
echo 🔄 Iniciando servidor local en puerto 8000...

REM Iniciar servidor en segundo plano
start /B python -c "
import http.server
import socketserver
import threading
import time

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

PORT = 8000
with socketserver.TCPServer(('', PORT), CustomHandler) as httpd:
    print(f'✅ Servidor local iniciado en puerto {PORT}')
    httpd.serve_forever()
"

REM Esperar un momento para que el servidor inicie
timeout /t 3 >nul

echo 🌐 Creando túnel público con Ngrok...
echo.
echo ⚡ Tu sistema estará disponible en una URL pública
echo 📱 Podrás acceder desde cualquier dispositivo móvil
echo 🔒 La conexión es segura (HTTPS)
echo.
echo ⚠️  IMPORTANTE: 
echo    • Mantén esta ventana abierta
echo    • La URL pública se mostrará a continuación
echo    • Copia la URL para acceder desde tu móvil
echo.
echo ════════════════════════════════════════════════════════════════

ngrok http 8000
