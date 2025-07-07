@echo off
title Sistema SINES - Servidor Seguro Simple
color 0A

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █          SISTEMA SINES - SERVIDOR SEGURO SIMPLE            █
echo █                                                              █
echo █                  🔒 VERSION FUNCIONAL                       █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🔐 Iniciando servidor seguro simplificado...
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
echo 🚀 Iniciando servidor en puerto 8002...
echo.
echo 🔑 CREDENCIALES:
echo ┌─────────────┬──────────────┐
echo │ Usuario     │ Contraseña   │
echo ├─────────────┼──────────────┤
echo │ admin       │ sines2024    │
echo │ supervisor  │ super2024    │
echo │ operador    │ op2024       │
echo │ sines       │ sines123     │
echo └─────────────┴──────────────┘
echo.
echo 💡 URL: http://localhost:8002/index_secure_simple.html
echo.
echo ⚠️  Para cerrar: Presiona Ctrl+C
echo.
echo ════════════════════════════════════════════════════════════════

py server_secure_simple.py

echo.
echo 🔒 Servidor detenido. Presiona cualquier tecla para salir...
pause > nul 