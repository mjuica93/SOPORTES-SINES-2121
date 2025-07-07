@echo off
chcp 65001 > nul
echo.
echo ==========================================
echo 🔒 PRUEBA DE SEGURIDAD - SISTEMA SINES
echo ==========================================
echo.
echo Este script te ayudará a verificar que el sistema
echo de seguridad funciona correctamente.
echo.
echo 📋 PRUEBAS A REALIZAR:
echo.
echo 1. Intenta acceder directamente a:
echo    http://localhost:8002/config_panel.html
echo    (Debe pedir autenticación)
echo.
echo 2. Intenta acceder a archivos JSON sin login:
echo    http://localhost:8002/support_data_enhanced.json
echo    (Debe redirigir al login)
echo.
echo 3. Haz logout y copia el link del panel
echo    (No debe permitir acceso)
echo.
echo 4. Intenta acceder con usuario sin permisos
echo    (Solo admin y supervisor pueden ver configuración)
echo.
echo ⚠️  CREDENCIALES PARA PRUEBAS:
echo    admin / sines2024 (✅ Puede acceder)
echo    supervisor / super2024 (✅ Puede acceder)
echo    operador / op2024 (❌ Sin permisos)
echo    sines / sines123 (❌ Sin permisos)
echo.
echo 🚀 Iniciando servidor seguro...
echo.
py server_secure_simple.py 