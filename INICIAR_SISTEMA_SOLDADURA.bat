@echo off
echo ========================================
echo    SISTEMA INTEGRADO SINES v5.0
echo    CON SEGUIMIENTO DE SOLDADURA
echo ========================================
echo.
echo Iniciando servidor seguro en puerto 8000...
echo.
echo Funcionalidades disponibles:
echo - Soportes Agrupados con Variables de Plantilla
echo - Isometricos con Prefabricados
echo - Relaciones Soportes-Isometricos
echo - NUEVO: Seguimiento de Soldadura
echo - Instalaciones con Control de Estado
echo.
echo Credenciales de acceso:
echo - admin / sines2024 (Administrador)
echo - supervisor / super2024 (Supervisor)
echo - operador / op2024 (Operador)
echo - sines / sines123 (Usuario)
echo.
echo Presiona Ctrl+C para detener el servidor
echo ========================================
echo.

python server_secure_complete.py

pause 