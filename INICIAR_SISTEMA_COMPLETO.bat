@echo off
title Sistema SINES - Iniciador Completo
color 0A

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █               SISTEMA SINES - INICIADOR COMPLETO            █
echo █                                                              █
echo █              🚀 SERVIDOR PRINCIPAL + SEGURIDAD              █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

REM Verificar si Python está instalado
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo.
    echo 📥 Descarga Python desde: https://python.org
    echo    Asegurate de marcar "Add to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.
echo 🔄 Iniciando servidores...
echo.

REM Verificar puertos disponibles
netstat -an | find "8000" >nul
if not errorlevel 1 (
    echo ⚠️  Puerto 8000 ocupado, terminando proceso...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %%a >nul 2>&1
    timeout /t 2 >nul
)

netstat -an | find "8002" >nul
if not errorlevel 1 (
    echo ⚠️  Puerto 8002 ocupado, terminando proceso...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8002') do taskkill /F /PID %%a >nul 2>&1
    timeout /t 2 >nul
)

echo.
echo 🌐 Iniciando servidor principal (puerto 8000)...
start "Servidor Principal SINES" /min cmd /c "py server.py"

echo 🔒 Iniciando servidor seguro (puerto 8002)...
timeout /t 3 >nul
start "Servidor Seguro SINES" /min cmd /c "py server_secure_simple.py"

echo.
echo ✅ SERVIDORES INICIADOS
echo.
echo 🌐 ACCESOS DISPONIBLES:
echo ┌─────────────────────────────────────────────────────────────┐
echo │ 📂 Sistema Principal (Sin Login):                          │
echo │    http://localhost:8000/index.html                        │
echo │    http://localhost:8000/index_isometricos_github.html     │
echo │                                                             │
echo │ 🔒 Sistema Seguro (Con Login):                             │
echo │    http://localhost:8002/index_secure_simple.html          │
echo └─────────────────────────────────────────────────────────────┘
echo.
echo 🔑 CREDENCIALES PARA ACCESO SEGURO:
echo ┌─────────────┬──────────────┐
echo │ Usuario     │ Contraseña   │
echo ├─────────────┼──────────────┤
echo │ admin       │ sines2024    │
echo │ supervisor  │ super2024    │
echo │ operador    │ op2024       │
echo │ sines       │ sines123     │
echo └─────────────┴──────────────┘
echo.
echo 🚀 Abriendo sistema seguro en navegador...
timeout /t 5 >nul
start http://localhost:8002/index_secure_simple.html

echo.
echo 💡 INSTRUCCIONES:
echo • El sistema principal funciona sin login
echo • El sistema seguro requiere credenciales
echo • Ambos servidores se ejecutan en segundo plano
echo • Para cerrar todo, cierra esta ventana
echo.
echo ⚠️  Presiona cualquier tecla para cerrar ambos servidores...
pause >nul

echo.
echo 🛑 Cerrando servidores...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Servidor Principal SINES" >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Servidor Seguro SINES" >nul 2>&1

REM Terminar por puerto si es necesario
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8002') do taskkill /F /PID %%a >nul 2>&1

echo ✅ Servidores cerrados
echo.
echo 👋 ¡Gracias por usar el Sistema SINES!
timeout /t 3 >nul 