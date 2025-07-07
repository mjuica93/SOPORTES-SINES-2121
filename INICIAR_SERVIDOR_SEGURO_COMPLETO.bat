@echo off
chcp 65001 > nul
title Sistema SINES - Servidor Seguro Completo
color 0C

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █           🔒 SERVIDOR SEGURO COMPLETO SINES                 █
echo █                                                              █
echo █        ⚠️  REEMPLAZA AL SERVIDOR PRINCIPAL (8000)          █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

REM Verificar si Python está instalado
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo.
    echo 📥 Descarga Python desde: https://python.org
    echo    Asegurate de marcar "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Detener cualquier servidor existente en el puerto 8000
echo 🔄 Deteniendo servidores existentes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    taskkill /F /PID %%a >nul 2>&1
)

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
echo 🛡️ CARACTERÍSTICAS DE SEGURIDAD:
echo • ✅ Autenticación obligatoria para TODOS los accesos
echo • ✅ Sesiones seguras con cookies HttpOnly
echo • ✅ Bloqueo automático tras 3 intentos fallidos
echo • ✅ Timeout de sesión (30 minutos)
echo • ✅ Logs de auditoría de seguridad
echo • ✅ Headers de seguridad HTTP
echo • ✅ Botón de cerrar sesión en TODAS las páginas
echo.
echo 👥 OPCIONES DE ADMINISTRADOR:
echo • ⚙️ Panel de configuración (solo admin/supervisor)
echo • 👤 Gestión de usuarios y roles
echo • 📊 Monitoreo del sistema en tiempo real
echo • 🔍 Logs de auditoría y eventos
echo • 🛠️ Herramientas de mantenimiento
echo.
echo 🚪 CERRAR SESIÓN:
echo • 🖱️ Botón "Cerrar Sesión" (esquina superior derecha)
echo • ⌨️ Atajo de teclado: Ctrl+Shift+L
echo • 🔄 Verificación automática de sesión cada minuto
echo • ⚠️ Redirección automática si la sesión expira
echo.
echo 🚀 Iniciando servidor seguro completo...
echo.

REM Iniciar servidor
py server_secure_complete.py

echo.
echo ⚠️  El servidor se ha detenido
echo.
pause 