@echo off
title Sistema de Soportes SINES - Servidor Seguro
color 0A

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █          SISTEMA DE SOPORTES SINES - SERVIDOR SEGURO        █
echo █                                                              █
echo █                  🔒 ACCESO PROTEGIDO CON LOGIN              █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🔐 Iniciando servidor con sistema de seguridad...
echo.
echo 🛡️  Características de seguridad:
echo    • Autenticación de usuarios requerida
echo    • Sesiones con timeout automático
echo    • Bloqueo tras intentos fallidos
echo    • Registro de eventos de seguridad
echo    • Headers de seguridad HTTP
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

echo ✅ Python encontrado, iniciando servidor seguro...
echo.
echo 🌐 El sistema se abrira automaticamente en tu navegador
echo 📍 URL: http://localhost:8001/index_isometricos_secure.html
echo.
echo 🔑 CREDENCIALES DE ACCESO:
echo ┌─────────────┬──────────────┬───────────────┐
echo │ Usuario     │ Contraseña   │ Rol           │
echo ├─────────────┼──────────────┼───────────────┤
echo │ admin       │ sines2024    │ Administrador │
echo │ supervisor  │ super2024    │ Supervisor    │
echo │ operador    │ op2024       │ Operador      │
echo │ sines       │ sines123     │ Usuario       │
echo └─────────────┴──────────────┴───────────────┘
echo.
echo 💡 Si no se abre automaticamente:
echo    1. Abre tu navegador
echo    2. Ve a: http://localhost:8001/index_isometricos_secure.html
echo.
echo ⚠️  Para cerrar el sistema: Presiona Ctrl+C en esta ventana
echo.
echo ════════════════════════════════════════════════════════════════

REM Verificar si el puerto está disponible
netstat -an | find "8001" >nul
if not errorlevel 1 (
    echo ⚠️  Puerto 8001 ocupado, intentando puerto 8002...
    py server_secure.py --port 8002
) else (
    py server_secure.py
)

echo.
echo ════════════════════════════════════════════════════════════════
echo 🔒 Servidor seguro finalizado. Presiona cualquier tecla para salir...
pause > nul 