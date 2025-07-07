@echo off
echo ===========================================
echo   SISTEMA SINES - MODAL COSTURAS MEJORADO
echo ===========================================
echo.
echo Iniciando servidor con modal mejorado...
echo.
echo ACCESO LOCAL: http://localhost:8000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
python -m http.server 8000 --bind 127.0.0.1 --directory .
pause 