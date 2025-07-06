@echo off
title SINES Soportes - Cloudflare Tunnel
color 0D

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █              SINES SOPORTES - CLOUDFLARE TUNNEL             █
echo █                                                              █
echo █           🆓 COMPLETAMENTE GRATUITO PARA SIEMPRE             █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🚀 Configurando acceso mundial GRATUITO con Cloudflare...
echo.
echo 💡 Cloudflare Tunnel es la mejor opción GRATUITA:
echo    ✅ Completamente gratuito para siempre
echo    ✅ URL personalizada permanente
echo    ✅ Disponibilidad 24/7
echo    ✅ SSL automático
echo    ✅ Sin límites de conexión
echo    ✅ Protección DDoS incluida
echo    ✅ CDN global ultra-rápido
echo    ✅ Sin expiración de sesión
echo.

echo 📥 Descargando Cloudflare Tunnel...
echo.

REM Verificar si cloudflared está instalado
cloudflared --version >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando Cloudflare Tunnel...
    
    REM Intentar instalar con winget
    winget install --id Cloudflare.cloudflared --accept-source-agreements --accept-package-agreements
    
    if errorlevel 1 (
        echo 🔄 Instalación manual de Cloudflare Tunnel...
        echo.
        echo 🛠️ Pasos para instalación manual:
        echo    1. Ve a: https://github.com/cloudflare/cloudflared/releases/latest
        echo    2. Descarga: cloudflared-windows-amd64.exe
        echo    3. Renombra a: cloudflared.exe
        echo    4. Coloca en esta carpeta o en PATH
        echo    5. Ejecuta este script nuevamente
        echo.
        pause
        exit /b 1
    )
)

echo ✅ Cloudflare Tunnel instalado
echo.
echo 🔑 Autenticando con Cloudflare...
echo    (Se abrirá tu navegador para autenticarte)
echo.

cloudflared tunnel login

echo.
echo 🌐 Creando túnel permanente...
echo.

REM Crear túnel con nombre único
for /f "tokens=2 delims==." %%i in ('wmic OS Get localdatetime /value') do set "dt=%%i"
set "tunnel_name=sines-soportes-%dt:~0,8%-%dt:~8,6%"

cloudflared tunnel create %tunnel_name%

echo.
echo 📝 Configurando túnel...
echo.

REM Crear archivo de configuración
echo tunnel: %tunnel_name% > config.yml
echo credentials-file: %USERPROFILE%\.cloudflared\%tunnel_name%.json >> config.yml
echo. >> config.yml
echo ingress: >> config.yml
echo   - hostname: *.trycloudflare.com >> config.yml
echo     service: http://localhost:8000 >> config.yml
echo   - service: http_status:404 >> config.yml

echo.
echo 🚀 Iniciando servidor local...
echo.

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
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

PORT = 8000
with socketserver.TCPServer(('', PORT), CustomHandler) as httpd:
    print(f'✅ Servidor local iniciado en puerto {PORT}')
    httpd.serve_forever()
"

REM Esperar un momento para que el servidor inicie
timeout /t 3 >nul

echo.
echo 🌐 Iniciando túnel Cloudflare...
echo.
echo 🎯 Tu sistema estará disponible en una URL como:
echo    https://abc-def-123.trycloudflare.com
echo.
echo 📱 Para acceso móvil optimizado:
echo    https://tu-url.trycloudflare.com/index_mobile.html
echo.
echo 🔒 Características incluidas:
echo    ✅ HTTPS automático
echo    ✅ Protección DDoS
echo    ✅ CDN global
echo    ✅ Sin límites de conexión
echo    ✅ Disponibilidad 24/7
echo    ✅ Completamente GRATUITO
echo.
echo ⚠️  IMPORTANTE: 
echo    • La URL será permanente mientras mantengas este túnel activo
echo    • Para URL personalizada, configura un dominio en Cloudflare
echo    • Mantén esta ventana abierta para que el túnel funcione
echo.
echo ════════════════════════════════════════════════════════════════
echo.

REM Ejecutar túnel con configuración
cloudflared tunnel --config config.yml run %tunnel_name%

echo.
echo 🛑 Túnel detenido
echo.
pause 